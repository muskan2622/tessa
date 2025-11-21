.PHONY: help install-backend install-frontend dev-backend dev-frontend test clean docker-up docker-down migrate

help:
	@echo "Available commands:"
	@echo "  make install-backend    - Install backend dependencies"
	@echo "  make install-frontend   - Install frontend dependencies"
	@echo "  make dev-backend        - Run backend development server"
	@echo "  make dev-frontend       - Run frontend development server"
	@echo "  make test              - Run tests"
	@echo "  make migrate            - Run database migrations"
	@echo "  make docker-up         - Start Docker containers"
	@echo "  make docker-down       - Stop Docker containers"
	@echo "  make clean             - Clean generated files"

install-backend:
	cd backend && pip install -r requirements.txt

install-frontend:
	cd frontend && npm install

dev-backend:
	cd backend && uvicorn main:app --reload --host 0.0.0.0 --port 8000

dev-frontend:
	cd frontend && npm run dev

test:
	cd backend && pytest

migrate:
	cd backend && alembic upgrade head

docker-up:
	cd infrastructure/docker && docker-compose up -d

docker-down:
	cd infrastructure/docker && docker-compose down

clean:
	find . -type d -name __pycache__ -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -r {} +
	rm -rf frontend/.next
	rm -rf frontend/node_modules
	rm -rf .pytest_cache
	rm -rf .mypy_cache

