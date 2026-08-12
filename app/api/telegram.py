from __future__ import annotations

from fastapi import APIRouter, Depends, Header, HTTPException, Request
from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.config import get_settings
from app.db import get_db
from app.models import Feedback, Generation, TelegramUser
from app.schemas import GenerationRequest
from app.services.generation import GenerationService
from app.services.telegram import TelegramClient

router = APIRouter(prefix="/api/v1/telegram", tags=["telegram"])


MESSAGES = {
    "ru": {
        "start": "Metaphor помогает подобрать слова для важного разговора. Текст будет передан AI-провайдеру для обработки. Не отправляйте лишние конфиденциальные данные. Чтобы продолжить, отправьте /agree. Язык: /ru /uz /en.",
        "agreed": "Готово. Теперь опишите ситуацию одним сообщением. Пример: «Поссорились с другом. Хочу извиниться без лишнего пафоса».",
        "need_agree": "Сначала подтвердите обработку текста командой /agree. Политика: {privacy}",
        "help": "Опишите ситуацию и желаемый результат. Не вводите лишние персональные данные. Команды: /ru /uz /en /delete.",
        "deleted": "Ваши сообщения и настройки в Metaphor удалены.",
        "language": "Язык установлен: русский.",
        "open": "Открыть Metaphor",
    },
    "uz": {
        "start": "Metaphor muhim suhbat uchun kerakli so‘zlarni topishga yordam beradi. Matn qayta ishlash uchun AI-provayderga yuboriladi. Ortiqcha maxfiy ma’lumot kiritmang. Davom etish uchun /agree buyrug‘ini yuboring. Til: /ru /uz /en.",
        "agreed": "Tayyor. Endi vaziyatni bitta xabarda yozing. Masalan: «Do‘stim bilan janjallashdik. Ortiqcha balandparvozliksiz uzr so‘ramoqchiman».",
        "need_agree": "Avval /agree buyrug‘i bilan matnni qayta ishlashga rozilik bildiring. Siyosat: {privacy}",
        "help": "Vaziyat va kerakli natijani yozing. Ortiqcha shaxsiy ma’lumot kiritmang. Buyruqlar: /ru /uz /en /delete.",
        "deleted": "Metaphor’dagi xabarlaringiz va sozlamalaringiz o‘chirildi.",
        "language": "Til o‘rnatildi: o‘zbekcha.",
        "open": "Metaphor’ni ochish",
    },
    "en": {
        "start": "Metaphor helps you find words for an important conversation. Your text will be sent to an AI provider for processing. Do not include unnecessary confidential data. Send /agree to continue. Language: /ru /uz /en.",
        "agreed": "Ready. Describe the situation in one message. Example: “I argued with a friend and want to apologize without sounding dramatic.”",
        "need_agree": "First confirm text processing with /agree. Policy: {privacy}",
        "help": "Describe the situation and desired outcome. Do not include unnecessary personal data. Commands: /ru /uz /en /delete.",
        "deleted": "Your Metaphor messages and settings have been deleted.",
        "language": "Language set to English.",
        "open": "Open Metaphor",
    },
}


def _initial_language(message: dict) -> str:
    code = str((message.get("from") or {}).get("language_code") or "").lower()
    if code.startswith("uz"):
        return "uz"
    if code.startswith("en"):
        return "en"
    return "ru"


def _get_user(db: Session, chat_id: str, message: dict) -> TelegramUser:
    user = db.get(TelegramUser, chat_id)
    if not user:
        user = TelegramUser(chat_id=chat_id, language=_initial_language(message))
        db.add(user)
        db.commit()
        db.refresh(user)
    return user


@router.post("/webhook")
async def telegram_webhook(
    request: Request,
    x_telegram_bot_api_secret_token: str = Header(default=""),
    db: Session = Depends(get_db),
):
    settings = get_settings()
    if settings.telegram_webhook_secret and x_telegram_bot_api_secret_token != settings.telegram_webhook_secret:
        raise HTTPException(status_code=401, detail="Invalid Telegram secret")
    update = await request.json()
    message = update.get("message") or {}
    chat = message.get("chat") or {}
    text = str(message.get("text") or "").strip()
    chat_id = str(chat.get("id") or "")
    if not text or not chat_id:
        return {"ok": True}

    client = TelegramClient(settings)
    user = _get_user(db, chat_id, message)

    if text.startswith("/ru") or text.startswith("/uz") or text.startswith("/en"):
        language = text[1:3]
        user.language = language
        db.commit()
        await client.send_message(chat_id, MESSAGES[language]["language"])
        return {"ok": True}

    m = MESSAGES.get(user.language, MESSAGES["ru"])
    privacy_url = settings.public_base_url.rstrip("/") + "/privacy"

    if text.startswith("/start"):
        await client.send_message(
            chat_id,
            m["start"] + f"\n{privacy_url}",
            reply_markup={
                "inline_keyboard": [[
                    {"text": m["open"], "web_app": {"url": settings.public_base_url.rstrip("/") + "/"}}
                ]]
            },
        )
        return {"ok": True}
    if text.startswith("/agree"):
        user.accepted_terms = True
        user.terms_version = settings.terms_version
        db.commit()
        await client.send_message(chat_id, m["agreed"])
        return {"ok": True}
    if text.startswith("/help"):
        await client.send_message(chat_id, m["help"])
        return {"ok": True}
    if text.startswith("/delete"):
        cid = f"tg:{chat_id}"
        generation_ids = list(db.scalars(select(Generation.id).where(Generation.client_id == cid)).all())
        if generation_ids:
            db.execute(delete(Feedback).where(Feedback.generation_id.in_(generation_ids)))
        db.execute(delete(Generation).where(Generation.client_id == cid))
        db.delete(user)
        db.commit()
        await client.send_message(chat_id, m["deleted"])
        return {"ok": True}

    if not user.accepted_terms or user.terms_version != settings.terms_version:
        user.accepted_terms = False
        db.commit()
        await client.send_message(chat_id, m["need_agree"].format(privacy=privacy_url))
        return {"ok": True}

    payload = GenerationRequest(
        mode="write",
        language=user.language,
        relationship="",
        goal="сформулировать уместное сообщение" if user.language == "ru" else "mos xabar yozish" if user.language == "uz" else "draft an appropriate message",
        tone="warm",
        context=text,
        source="telegram",
        accepted_terms=True,
    )
    try:
        result = await GenerationService(db).create(f"tg:{chat_id}", payload)
        await client.send_message(chat_id, result.variants[0].text)
    except HTTPException as exc:
        await client.send_message(chat_id, str(exc.detail))
    return {"ok": True}
