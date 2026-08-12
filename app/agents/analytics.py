from __future__ import annotations

from app.agents.base import AgentResult, BaseAgent
from app.services.metrics import dashboard_snapshot


class GrowthAnalystAgent(BaseAgent):
    name = "growth_analyst"

    async def run(self, payload: dict) -> AgentResult:
        snapshot = dashboard_snapshot(self.db, days=int(payload.get("days", 7)))
        prompt = f"""
Review these first-party product metrics: {snapshot}
Return strict JSON with: diagnosis, one bottleneck, one experiment, stop_condition, success_metric.
Do not recommend more content merely because activity is low. Optimize for messages copied/sent, repeat users and revenue readiness.
""".strip()
        result = await self.generate_ai(
            "You are a disciplined product-growth analyst.",
            prompt,
            purpose="growth_analysis",
        )
        try:
            analysis = self.llm.parse_json(result.text)
        except Exception:
            analysis = {"raw": result.text}
        return AgentResult(True, {"snapshot": snapshot, "analysis": analysis}, True, "Operator approves the experiment")
