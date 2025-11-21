"""
Main FastAPI application entry point for Real Estate TC Agent
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import os

from backend.api import title_search, document_processing, risk_scoring, compliance
from backend.api.auth import router as auth_router
from backend.utils.logging import setup_logging

# Initialize logging
setup_logging()

app = FastAPI(
    title="Real Estate TC Agent API",
    description="AI-powered platform for Real Estate Title Companies",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Trusted host middleware for security
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=os.getenv("ALLOWED_HOSTS", "*").split(",")
)

# Include routers
app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])
app.include_router(title_search.router, prefix="/api/title-search", tags=["Title Search"])
app.include_router(document_processing.router, prefix="/api/documents", tags=["Document Processing"])
app.include_router(risk_scoring.router, prefix="/api/risk", tags=["Risk Scoring"])
app.include_router(compliance.router, prefix="/api/compliance", tags=["Compliance"])


@app.get("/")
async def root():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Real Estate TC Agent API"}


@app.get("/api/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "service": "Real Estate TC Agent API"
    }

