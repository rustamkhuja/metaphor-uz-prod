from __future__ import annotations

from app.agents.base import AgentResult, BaseAgent


class TrendAgent(BaseAgent):
    name = "trend"

    async def run(self, payload: dict) -> AgentResult:
        date = payload.get("date", "today")
        if not self.settings.llm_enable_web_search:
            return AgentResult(
                success=True,
                data={
                    "signals": [],
                    "note": "Web search disabled; use evergreen calendar and first-party product metrics.",
                    "date": date,
                },
            )
        prompt = (
            "Find only useful, non-political and non-sensitive communication occasions relevant to Uzbekistan "
            f"for {date}: official holidays, school milestones, family occasions and widely observed cultural events. "
            "Return concise JSON with signals, exact dates and source URLs. Do not invent events."
        )
        result = await self.generate_ai(
            "You are a cautious trend researcher for a communication-assistance product.",
            prompt,
            purpose="trend_research",
            web_search=True,
        )
        try:
            data = self.llm.parse_json(result.text)
        except Exception:
            data = {"raw": result.text, "citations": result.citations or []}
        return AgentResult(success=True, data=data)
