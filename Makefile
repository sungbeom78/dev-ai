.PHONY: up down logs test

up:
	docker compose up -d

down:
	docker compose down

logs:
	docker compose logs -f

test:
	curl http://localhost:8000/health
