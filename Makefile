setup:
	@if [ ! -f .env ]; then cp .env.example .env; fi
	@docker compose pull
	@docker compose build --pull --parallel
	@echo "Setup done."

build:
	docker compose build

up:
	@if [ ! -f .env ]; then cp .env.example .env; fi
	docker compose up -d
	@echo "Waiting for DB..."
	@sleep 5
	docker compose exec backend alembic upgrade head
	docker compose exec backend python -m app.seed.load_demo
	@echo "Stack is up at http://localhost:$${PUBLIC_PORT}"

migrate:
	docker compose exec backend alembic upgrade head

seed:
	docker compose exec backend python /app/seed/load_demo.py

test:
	docker compose exec backend pytest -q
	docker compose exec frontend npm test --silent || true
	docker compose exec frontend npx cypress run || true

down:
	docker compose down -v

fmt:
	docker compose exec backend ruff check . --fix
	docker compose exec backend mypy app || true
	docker compose exec frontend npx prettier --write "src/**/*.{ts,tsx}"

.PHONY: setup build up migrate seed test down fmt
