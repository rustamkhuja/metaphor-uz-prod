.PHONY: run test smoke validate benchmark docker-up docker-down seed

run:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

test:
	pytest -q

smoke:
	python scripts/smoke_test.py

validate:
	python scripts/validate_package.py

benchmark:
	python scripts/benchmark_models.py

seed:
	python scripts/seed.py

docker-up:
	docker compose up -d --build

docker-down:
	docker compose down
