// Временное хранилище IP-адресов и их активности для Rate Limiting
const rateLimitMap = new Map();

/**
 * Функция проверки лимита запросов (Rate Limit)
 * @param {string} ip - IP-адрес пользователя
 * @param {number} limit - Максимум запросов за окно времени (по умолчанию 5)
 * @param {number} windowMs - Окно времени в миллисекундах (по умолчанию 1 минута)
 */
function checkRateLimit(ip, limit = 5, windowMs = 60 * 1000) {
    const now = Date.now();
    const record = rateLimitMap.get(ip) || { count: 0, resetTime: now + windowMs };

    // Если время окна истекло, сбрасываем счетчик
    if (now > record.resetTime) {
        record.count = 1;
        record.resetTime = now + windowMs;
    } else {
        record.count += 1;
    }

    rateLimitMap.set(ip, record);

    // Очистка устаревших IP-адресов из памяти при разрастании Map
    if (rateLimitMap.size > 5000) {
        for (const [key, value] of rateLimitMap.entries()) {
            if (now > value.resetTime) rateLimitMap.delete(key);
        }
    }

    if (record.count > limit) {
        const retryAfterSeconds = Math.ceil((record.resetTime - now) / 1000);
        return { limited: true, retryAfterSeconds };
    }

    return { limited: false };
}

export default async function handler(req, res) {
    if (req.method !== 'POST') {
        return res.status(405).json({ error: 'Method Not Allowed' });
    }

    // Определяем IP-адрес клиента (с учетом прокси Vercel / Cloudflare)
    const clientIp = 
        req.headers['x-forwarded-for']?.split(',')[0] || 
        req.headers['x-real-ip'] || 
        req.socket.remoteAddress || 
        '127.0.0.1';

    // Проверяем лимит: максимум 5 запросов в 1 минуту с одного IP
    const { limited, retryAfterSeconds } = checkRateLimit(clientIp, 5, 60 * 1000);

    if (limited) {
        return res.status(429).json({ 
            text: `Слишком много запросов. Пожалуйста, подождите ${retryAfterSeconds} сек.` 
        });
    }

    const { step1, step2, step3, lang = 'ru' } = req.body;
    const apiKey = process.env.GROQ_API_KEY;

    if (!apiKey) {
        return res.status(500).json({ text: "Ключ GROQ_API_KEY не найден в переменных окружения." });
    }

    // Определение целевого языка
    const languageMap = {
        ru: 'Русский',
        uz: 'Узбекский',
        en: 'Английский'
    };
    const targetLanguage = languageMap[lang] || 'Русский';

    // Системный промпт для строгого соблюдения правил вывода
    const systemPrompt = `Ты — профессиональный писатель и копирайтер. 
Твоя задача — создавать искренние, точно выраженные сообщения строго на указанном языке.

СТРОГИЕ ПРАВИЛА:
1. Выдавай ТОЛЬКО финальный текст сообщения.
2. Не используй приветствия, прощания, подписи и вступления (например, "Вот ваше сообщение:").
3. Ограничение по объему: не более 4 предложений.`;

    const userPrompt = `Сгенерируй текст на языке: ${targetLanguage}.
От кого и кому: ${step1}
Ситуация / Повод: ${step2}
Тон / Тональность: ${step3}`;

    try {
        const response = await fetch("https://api.groq.com/openai/v1/chat/completions", {
            method: "POST",
            headers: {
                "Authorization": `Bearer ${apiKey}`,
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                model: "llama-3.1-8b-instant",
                messages: [
                    { role: "system", content: systemPrompt },
                    { role: "user", content: userPrompt }
                ],
                temperature: 0.7,
                max_tokens: 300
            })
        });

        const data = await response.json();
        
        if (data.choices && data.choices.length > 0) {
            res.status(200).json({ text: data.choices[0].message.content.trim() });
        } else if (data.error && data.error.message) {
            res.status(500).json({ text: `Ошибка Groq: ${data.error.message}` });
        } else {
            res.status(500).json({ text: "Ошибка при генерации текста. Попробуйте еще раз." });
        }
    } catch (error) {
        res.status(500).json({ text: "Слова потерялись в пути. Ошибка сервера." });
    }
}
