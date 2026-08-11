export default async function handler(req, res) {
    if (req.method !== 'POST') {
        return res.status(405).json({ error: 'Method Not Allowed' });
    }

    const { step1, step2, step3 } = req.body;
    const apiKey = process.env.GROQ_API_KEY;

    if (!apiKey) {
        return res.status(500).json({ text: "Ключ GROQ_API_KEY не найден в переменных окружения." });
    }

    const prompt = `Действуй как опытный писатель. Напиши искреннее сообщение. 
    От кого и кому: ${step1}. 
    Ситуация: ${step2}. 
    Тон: ${step3}. 
    Текст должен быть без приветствий и прощаний, только суть. Не больше 4 предложений.`;

    try {
        const response = await fetch("https://api.groq.com/openai/v1/chat/completions", {
            method: "POST",
            headers: {
                "Authorization": `Bearer ${apiKey}`,
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                model: "llama-3.1-8b-instant",
                messages: [{ role: "user", content: prompt }]
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
