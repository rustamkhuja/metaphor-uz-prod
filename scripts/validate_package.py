from __future__ import annotations

import csv
from pathlib import Path
import py_compile
import sys
import tempfile
import re

import yaml

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "VERSION",
    "README.md",
    "START_HERE.md",
    "BUILD_MANIFEST.md",
    "ACCEPTANCE_REPORT.md",
    "RELEASE_NOTES.md",
    "SECURITY.md",
    ".gitattributes",
    "FULL_LAUNCH_GUIDE_RU.md",
    "scripts/configure_env.sh",
    "scripts/set_operator_chat_id.sh",
    "scripts/promote_to_production.sh",
    "scripts/production_check.sh",
    ".github/workflows/ci.yml",
    ".env.example",
    "docker-compose.yml",
    "Dockerfile",
    "app/main.py",
    "app/services/llm.py",
    "app/agents/orchestrator.py",
    "docs/00_EXECUTIVE_BLUEPRINT.md",
    "docs/08_OPERATOR_RUNBOOK.md",
    "docs/09_OWNER_ACTIONS.md",
    "docs/17_HANDOVER.md",
    "docs/19_EXTERNAL_ACTION_TICKETS.md",
    "docs/20_PRODUCTION_GAP_REGISTER.md",
    "evaluation/test_cases.csv",
]


def main() -> None:
    missing = [name for name in REQUIRED if not (ROOT / name).exists()]
    if missing:
        raise SystemExit(f"Missing required files: {missing}")

    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    if version != "0.2.1":
        raise SystemExit(f"Unexpected VERSION: {version!r}")

    compose = yaml.safe_load((ROOT / "docker-compose.yml").read_text(encoding="utf-8"))
    services = set((compose or {}).get("services", {}))
    expected_services = {"db", "app", "worker", "backup", "caddy"}
    if not expected_services.issubset(services):
        raise SystemExit(f"Compose services missing: {expected_services - services}")

    python_files = list((ROOT / "app").rglob("*.py")) + list((ROOT / "scripts").glob("*.py"))
    with tempfile.TemporaryDirectory(prefix="metaphor-compile-") as tmp:
        target_root = Path(tmp)
        for index, path in enumerate(python_files):
            py_compile.compile(str(path), cfile=str(target_root / f"{index}.pyc"), doraise=True)

    with (ROOT / "evaluation" / "test_cases.csv").open(encoding="utf-8") as handle:
        cases = list(csv.DictReader(handle))
    if len(cases) < 40:
        raise SystemExit("Evaluation set is unexpectedly small")
    languages = {row.get("language") for row in cases}
    if not {"ru", "uz", "en"}.issubset(languages):
        raise SystemExit(f"Evaluation languages incomplete: {languages}")

    secret_pattern = re.compile(r"xai-[A-Za-z0-9_-]{20,}")
    secret_hits: list[str] = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.name == "FILE_HASHES.sha256":
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        if secret_pattern.search(content):
            secret_hits.append(str(path.relative_to(ROOT)))
    if secret_hits:
        raise SystemExit(f"Potential xAI API key found in release files: {secret_hits}")

    forbidden_exact = ["metaphor.db", "test_metaphor.db", "smoke_metaphor.db", ".env"]
    present = [name for name in forbidden_exact if (ROOT / name).exists()]
    forbidden_dirs = [".pytest_cache", "runtime"]
    present += [name for name in forbidden_dirs if (ROOT / name).exists()]
    pycache = list(ROOT.rglob("__pycache__"))
    bytecode = list(ROOT.rglob("*.pyc"))
    generated_media = [p for p in (ROOT / "exports").glob("*") if p.is_file()] if (ROOT / "exports").exists() else []
    benchmark_outputs = list((ROOT / "evaluation" / "results").glob("*")) if (ROOT / "evaluation" / "results").exists() else []
    if present or pycache or bytecode or generated_media or benchmark_outputs:
        raise SystemExit(
            "Remove runtime artefacts before packaging: "
            f"present={present}, pycache={len(pycache)}, bytecode={len(bytecode)}, "
            f"media={len(generated_media)}, benchmark_outputs={len(benchmark_outputs)}"
        )

    print(
        f"Package validation passed: version={version}, cases={len(cases)}, "
        f"languages={sorted(languages)}, services={sorted(services)}"
    )


if __name__ == "__main__":
    sys.path.insert(0, str(ROOT))
    main()
