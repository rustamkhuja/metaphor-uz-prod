export default async function handler(req, res) {
    if (req.method !== 'POST') {
        return res.status(405).json({ error: 'Method Not Allowed' });
    }

    const { step1, step2, step3, lang = 'ru' } = req.body;
    const apiKey = process.env.GROQ_API_KEY;

    if (!apiKey) {
        return res.status(500).json({ text: "Ключ GROQ_API_KEY не найден в переменных окружения." });
    }

    // Определение языка генерации
    const languageMap = {
        ru: 'Русский',
        uz: 'Узбекский',
        en: 'Английский'
    };
    const targetLanguage = languageMap[lang] || 'Русский';

    // Разделение на системную роль и пользовательский ввод для точного соблюдения ограничений
    const systemPrompt = `Ты — профессиональный писатель и копирайтер. 
Твоя задача — создавать искренние, точные сообщения строго на указанном языке.

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
