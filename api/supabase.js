/**
 * Вспомогательная функция для прямой работы с Supabase REST API
 * (Без необходимости устанавливать npm пакеты)
 */
export async function supabaseRequest(tableName, method = 'POST', body = null) {
    const SUPABASE_URL = process.env.SUPABASE_URL || "https://brpphigeattisajrgwcg.supabase.co/rest/v1/";
    const SUPABASE_KEY = process.env.SUPABASE_ANON_KEY || "sb_publishable_lysbxoZtXFep_EcqTcMjKg_dNHisG6i";

    if (!SUPABASE_URL || SUPABASE_URL.includes("ВАШ_PROJECT_URL")) {
        console.error("Supabase URL не настроен");
        return null;
    }

    try {
        const options = {
            method: method,
            headers: {
                "apikey": SUPABASE_KEY,
                "Authorization": `Bearer ${SUPABASE_KEY}`,
                "Content-Type": "application/json",
                "Prefer": "return=minimal"
            }
        };

        if (body && (method === 'POST' || method === 'PATCH' || method === 'PUT')) {
            options.body = JSON.stringify(body);
        }

        const response = await fetch(`${SUPABASE_URL}/rest/v1/${tableName}`, options);
        
        if (!response.ok) {
            const errorText = await response.text();
            console.error(`Supabase Error (${tableName}):`, errorText);
            return null;
        }

        if (method === 'GET') {
            return await response.json();
        }

        return true;
    } catch (err) {
        console.error("Supabase Request Failed:", err);
        return null;
    }
}