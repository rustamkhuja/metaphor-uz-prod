import { supabaseRequest } from './supabase.js';

export default async function handler(req, res) {
    if (req.method !== 'POST') {
        return res.status(405).json({ error: 'Method Not Allowed' });
    }

    const { type, eventName, language, tone, rating, comment, contact } = req.body;

    // Определяем браузер и тип девайса из заголовка User-Agent
    const userAgent = req.headers['user-agent'] || '';
    const isMobile = /mobile/i.test(userAgent);
    const isTablet = /ipad|tablet/i.test(userAgent);
    const deviceType = isTablet ? 'tablet' : (isMobile ? 'mobile' : 'desktop');

    // Определяем страну из заголовков Vercel / Cloudflare
    const country = req.headers['x-vercel-ip-country'] || req.headers['cf-ipcountry'] || 'Unknown';

    try {
        // 1. Фиксация визита / девайса
        if (type === 'visit') {
            await supabaseRequest('analytics', 'POST', {
                country: country,
                device_type: deviceType,
                browser: userAgent.substring(0, 50),
                language: language || 'ru'
            });
            return res.status(200).json({ success: true });
        }

        // 2. Фиксация событий (скачивания, клики)
        if (type === 'event') {
            await supabaseRequest('events', 'POST', {
                event_name: eventName,
                language: language,
                tone: tone
            });
            return res.status(200).json({ success: true });
        }

        // 3. Сохранение отзывов
        if (type === 'feedback') {
            await supabaseRequest('feedback', 'POST', {
                rating: parseInt(rating) || 5,
                comment: comment,
                contact: contact || null
            });
            return res.status(200).json({ success: true });
        }

        return res.status(400).json({ error: 'Invalid tracking type' });
    } catch (error) {
        return res.status(500).json({ error: 'Tracking failed' });
    }
}