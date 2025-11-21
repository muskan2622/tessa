# Quick Start Guide

## Prerequisites

Before starting, ensure you have:
- **Python 3.11+** installed
- **Node.js 18+** installed
- **PostgreSQL 15+** running (or use Docker)
- **Redis** running (or use Docker)
- **OpenAI API Key** (for AI features)

## Option 1: Quick Start with Docker (Recommended)

This is the fastest way to get everything running:

### Step 1: Start Services
```bash
cd infrastructure/docker
docker-compose up -d
```

This will start:
- PostgreSQL database (port 5432)
- Redis cache (port 6379)
- Backend API (port 8000)
- Frontend (port 3000)

### Step 2: Set Environment Variables
```bash
# Copy example environment file
cp .env.example .env

# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=your-api-key-here
```

### Step 3: Run Database Migrations
```bash
# Activate virtual environment (if using local Python)
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Run migrations
cd backend
alembic upgrade head
```

### Step 4: Access the Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/api/docs

## Option 2: Manual Setup

### Step 1: Backend Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
cd backend
pip install -r requirements.txt

# Set up environment variables
cp ../.env.example ../.env
# Edit ../.env with your configuration

# Run database migrations
alembic upgrade head

# Start backend server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Step 2: Frontend Setup

```bash
# In a new terminal
cd frontend

# Install dependencies
npm install

# Set up environment variables
cp .env.example .env.local
# Edit .env.local: NEXT_PUBLIC_API_URL=http://localhost:8000

# Start frontend server
npm run dev
```

### Step 3: Start Database & Redis

If not using Docker, start PostgreSQL and Redis manually:

**PostgreSQL:**
```bash
# macOS (Homebrew)
brew services start postgresql@15

# Linux
sudo systemctl start postgresql

# Windows
# Start PostgreSQL service from Services panel
```

**Redis:**
```bash
# macOS (Homebrew)
brew services start redis

# Linux
sudo systemctl start redis

# Windows
# Download and run Redis from https://redis.io/download
```

## Verify Installation

### Test Backend API
```bash
# Health check
curl http://localhost:8000/api/health

# Should return: {"status":"healthy","version":"1.0.0","service":"Real Estate TC Agent API"}
```

### Test Frontend
Open http://localhost:3000 in your browser. You should see the title search form.

## First API Call

### Get Authentication Token
```bash
curl -X POST "http://localhost:8000/api/auth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=test&password=test"
```

### Create a Title Search
```bash
curl -X POST "http://localhost:8000/api/title-search/search" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "property_address": {
      "street": "123 Main St",
      "city": "Los Angeles",
      "state": "CA",
      "zip_code": "90001"
    },
    "search_type": "full"
  }'
```

## Troubleshooting

### Backend won't start
- Check if PostgreSQL is running: `pg_isready`
- Check if Redis is running: `redis-cli ping`
- Verify environment variables in `.env`
- Check logs: `logs/app.log`

### Frontend won't connect to backend
- Verify `NEXT_PUBLIC_API_URL` in `frontend/.env.local`
- Check CORS settings in `backend/main.py`
- Ensure backend is running on port 8000

### Database connection errors
- Verify `DATABASE_URL` in `.env`
- Check PostgreSQL is running and accessible
- Run migrations: `alembic upgrade head`

### AI features not working
- Verify `OPENAI_API_KEY` is set in `.env`
- Check API key is valid and has credits
- Review logs for OpenAI API errors

## Next Steps

1. **Configure Integrations**: Set up Salesforce, Qualia, or other integrations in `.env`
2. **Add Data Sources**: Configure county API credentials for data ingestion
3. **Train Models**: Prepare training data and fine-tune models (see `models/fine_tuning/`)
4. **Set Up Webhooks**: Configure webhook endpoints for event notifications
5. **Deploy**: Use Terraform and Kubernetes configs for production deployment

## Development Commands

```bash
# Run tests
make test

# Format code
black backend/
isort backend/

# Run linter
flake8 backend/

# View logs
tail -f logs/app.log

# Stop Docker services
cd infrastructure/docker
docker-compose down
```

