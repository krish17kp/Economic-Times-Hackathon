.PHONY: dev stop test seed migrate lint clean

# Start everything
dev:
	docker-compose up --build -d
	@echo "Backend: http://localhost:8000/docs"
	@echo "Frontend: http://localhost:3000"

# Stop everything
stop:
	docker-compose down

# Run backend tests
test:
	cd backend && python -m pytest -v --tb=short

# Seed database
seed:
	cd backend && python data/seed/seed_db.py

# Run alembic migration
migrate:
	cd backend && alembic upgrade head

# Lint
lint:
	cd backend && python -m flake8 app/ --max-line-length=120
	cd frontend && npm run lint

# Clean everything including volumes
clean:
	docker-compose down -v
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true