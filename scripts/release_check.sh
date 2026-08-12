#!/bin/sh
set -eu
pytest -q
python scripts/smoke_test.py
python -m compileall -q app scripts
find . -type d -name __pycache__ -prune -exec rm -rf {} +
find . -type f -name '*.pyc' -delete
rm -rf .pytest_cache
rm -f metaphor.db test_metaphor.db smoke_metaphor.db
find exports -type f -delete 2>/dev/null || true
rm -rf evaluation/results runtime
python scripts/validate_package.py
