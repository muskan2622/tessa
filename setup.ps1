# Tessa Setup Script for Windows PowerShell
# This script helps set up the development environment

Write-Host "🚀 Setting up Tessa Development Environment" -ForegroundColor Green

# Check Python version
Write-Host "📋 Checking Python version..." -ForegroundColor Cyan
$pythonVersion = python --version
Write-Host "Python version: $pythonVersion"

# Check Node.js version
Write-Host "📋 Checking Node.js version..." -ForegroundColor Cyan
$nodeVersion = node --version
Write-Host "Node.js version: $nodeVersion"

# Create virtual environment
Write-Host "📦 Creating Python virtual environment..." -ForegroundColor Cyan
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install backend dependencies
Write-Host "📦 Installing backend dependencies..." -ForegroundColor Cyan
Set-Location backend
pip install --upgrade pip
pip install -r requirements.txt
Set-Location ..

# Install frontend dependencies
Write-Host "📦 Installing frontend dependencies..." -ForegroundColor Cyan
Set-Location frontend
npm install
Set-Location ..

# Create .env file if it doesn't exist
if (-Not (Test-Path .env)) {
    Write-Host "📝 Creating .env file from .env.example..." -ForegroundColor Cyan
    Copy-Item .env.example .env
    Write-Host "⚠️  Please edit .env file with your configuration" -ForegroundColor Yellow
}

# Create logs directory
New-Item -ItemType Directory -Force -Path logs | Out-Null

Write-Host "✅ Setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:"
Write-Host "1. Edit .env file with your configuration"
Write-Host "2. Start PostgreSQL and Redis"
Write-Host "3. Run migrations: alembic upgrade head"
Write-Host "4. Start backend: uvicorn main:app --reload"
Write-Host "5. Start frontend: npm run dev"

