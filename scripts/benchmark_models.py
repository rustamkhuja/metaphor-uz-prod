from __future__ import annotations

import argparse
import asyncio
import csv
from datetime import datetime, timezone
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.config import Settings  # noqa: E402
from app.schemas import GenerationRequest  # noqa: E402
from app.services.llm import LLMRouter  # noqa: E402
from app.services.prompts import SYSTEM_PROMPT, build_generation_prompt  # noqa: E402
from app.services.safety import classify  # noqa: E402


async def run(models: list[str], limit: int | None, output_dir: Path) -> None:
    rows = list(csv.DictReader((ROOT / "evaluation" / "test_cases.csv").open(encoding="utf-8")))
    if limit:
        rows = rows[:limit]
    settings = Settings()
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    details: list[dict] = []

    for model in models:
        router = LLMRouter(settings)
        router.primary.model = model
        for case in rows:
            safety = classify(case["input"])
            expects_block = "block" in case["expected_properties"].lower()
            record = {
                "model_requested": model,
                "case_id": case["id"],
                "language": case["language"],
                "mode": case["mode"],
                "expected_properties": case["expected_properties"],
                "forbidden": case["forbidden"],
                "blocked": safety.blocked,
                "block_correct": safety.blocked == expects_block if expects_block or safety.blocked else "",
                "json_valid": "",
                "forbidden_hits": "",
                "provider": "local-safety" if safety.blocked else "",
                "model_returned": "",
                "cost_usd": 0.0,
                "output": safety.message if safety.blocked else "",
                "human_naturalness_1_5": "",
                "human_goal_fit_1_5": "",
                "human_cultural_fit_1_5": "",
                "human_sendable_yes_no": "",
                "human_notes": "",
            }
            if not safety.blocked:
                request = GenerationRequest(
                    mode=case["mode"],
                    language=case["language"],
                    relationship=case["relationship"],
                    goal=case["goal"],
                    tone=case["tone"],
                    context=case["input"] if case["mode"] == "write" else "",
                    source_text="" if case["mode"] == "write" else case["input"],
                    address_form="auto",
                    source="api",
                    accepted_terms=True,
                )
                try:
                    result = await router.generate(
                        SYSTEM_PROMPT,
                        build_generation_prompt(request, 1),
                        json_mode=True,
                    )
                    parsed = router.parse_json(result.text)
                    output = "\n".join(
                        str(item.get("text") or "")
                        for item in parsed.get("variants") or []
                        if isinstance(item, dict)
                    ).strip()
                    forbidden = [x.strip() for x in case["forbidden"].split(";") if x.strip()]
                    hits = [x for x in forbidden if x.lower() in output.lower()]
                    record.update(
                        {
                            "json_valid": True,
                            "forbidden_hits": " | ".join(hits),
                            "provider": result.provider,
                            "model_returned": result.model,
                            "cost_usd": round(result.cost_usd, 8),
                            "output": output,
                        }
                    )
                except Exception as exc:
                    record.update({"json_valid": False, "output": f"ERROR: {type(exc).__name__}: {exc}"})
            details.append(record)

    detail_path = output_dir / f"benchmark_{timestamp}.csv"
    with detail_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(details[0].keys()))
        writer.writeheader()
        writer.writerows(details)

    summary = {}
    for model in models:
        subset = [x for x in details if x["model_requested"] == model]
        summary[model] = {
            "cases": len(subset),
            "json_success_rate": round(sum(x["json_valid"] is True for x in subset) / max(1, sum(not x["blocked"] for x in subset)), 3),
            "forbidden_hit_cases": sum(bool(x["forbidden_hits"]) for x in subset),
            "automated_safety_mismatches": sum(x["block_correct"] is False for x in subset),
            "estimated_or_actual_cost_usd": round(sum(float(x["cost_usd"] or 0) for x in subset), 6),
            "human_review_required": True,
        }
    summary_path = output_dir / f"benchmark_{timestamp}_summary.json"
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(detail_path)
    print(summary_path)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the Metaphor RU/UZ/EN evaluation set against configured models.")
    parser.add_argument("--models", default="", help="Comma-separated model IDs; default is LLM_PRIMARY_MODEL")
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--output-dir", default="evaluation/results")
    args = parser.parse_args()
    settings = Settings()
    models = [x.strip() for x in args.models.split(",") if x.strip()] or [settings.llm_primary_model]
    asyncio.run(run(models, args.limit or None, ROOT / args.output_dir))


if __name__ == "__main__":
    main()
