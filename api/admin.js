import { supabaseRequest } from './supabase.js';

export default async function handler(req, res) {
    if (req.method !== 'POST') {
        return res.status(405).json({ error: 'Method Not Allowed' });
    }

    const { password } = req.body;
    const ADMIN_PASSWORD = process.env.ADMIN_PASSWORD || 'admin123'; // Пароль по умолчанию или из переменных

    // Проверка пароля
    if (password !== ADMIN_PASSWORD) {
        return res.status(401).json({ error: 'Неверный пароль' });
    }

    try {
        // Получаем все записи из таблиц
        const visits = await supabaseRequest('analytics', 'GET') || [];
        const events = await supabaseRequest('events', 'GET') || [];
        const feedback = await supabaseRequest('feedback', 'GET') || [];

        // Агрегация по девайсам
        const devices = visits.reduce((acc, item) => {
            const dev = item.device_type || 'desktop';
            acc[dev] = (acc[dev] || 0) + 1;
            return acc;
        }, {});

        // Агрегация по странам
        const countries = visits.reduce((acc, item) => {
            const c = item.country || 'Unknown';
            acc[c] = (acc[c] || 0) + 1;
            return acc;
        }, {});

        // Агрегация по событиям (скачивания, копирования, шеринг)
        const eventCounts = events.reduce((acc, item) => {
            const ev = item.event_name || 'other';
            acc[ev] = (acc[ev] || 0) + 1;
            return acc;
        }, {});

        return res.status(200).json({
            success: true,
            summary: {
                totalVisits: visits.length,
                totalEvents: events.length,
                totalFeedback: feedback.length,
                downloads: eventCounts['download_card_click'] || 0,
                generations: eventCounts['generation_success'] || 0,
            },
            devices,
            countries,
            events: eventCounts,
            feedbackList: feedback.reverse().slice(0, 50) // Последние 50 отзывов
        });
    } catch (error) {
        return res.status(500).json({ error: 'Ошибка загрузки данных админки' });
    }
}