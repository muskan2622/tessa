"""
Risk scoring API endpoints
Provides risk assessment and scoring for title searches
"""
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

from backend.services.risk_scoring_service import RiskScoringService
from backend.api.auth import get_current_user, User
from fastapi import HTTPException

router = APIRouter()


class RiskFactor(BaseModel):
    """Individual risk factor"""
    factor_name: str
    factor_type: str
    severity: str  # low, medium, high, critical
    description: str
    impact_score: float
    evidence: Optional[Dict[str, Any]] = None


class RiskScore(BaseModel):
    """Risk score result"""
    score_id: str
    search_id: Optional[str] = None
    property_address: Optional[Dict[str, str]] = None
    overall_risk_score: float  # 0-100
    risk_level: str  # low, medium, high, critical
    risk_factors: List[RiskFactor]
    recommendations: List[str]
    created_at: datetime
    model_version: str


class RiskScoreRequest(BaseModel):
    """Request for risk scoring"""
    search_id: Optional[str] = None
    property_address: Optional[Dict[str, str]] = None
    include_recommendations: bool = True


@router.post("/score", response_model=RiskScore)
async def calculate_risk_score(
    request: RiskScoreRequest,
    current_user: User = Depends(get_current_user)
):
    """Calculate risk score for a property or title search"""
    service = RiskScoringService()
    
    risk_score = await service.calculate_risk_score(
        search_id=request.search_id,
        property_address=request.property_address,
        include_recommendations=request.include_recommendations,
        user_id=current_user.username
    )
    
    return risk_score


@router.get("/score/{score_id}", response_model=RiskScore)
async def get_risk_score(
    score_id: str,
    current_user: User = Depends(get_current_user)
):
    """Get a specific risk score by ID"""
    service = RiskScoringService()
    risk_score = await service.get_risk_score(score_id)
    
    if not risk_score:
        raise HTTPException(status_code=404, detail="Risk score not found")
    
    return risk_score


@router.get("/scores", response_model=List[RiskScore])
async def list_risk_scores(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user)
):
    """List all risk scores for the current user"""
    service = RiskScoringService()
    scores = await service.list_risk_scores(
        user_id=current_user.username,
        skip=skip,
        limit=limit
    )
    return scores

