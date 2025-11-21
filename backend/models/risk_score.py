"""
Risk scoring data models
"""
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class RiskLevel(str, Enum):
    """Risk level"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class RiskFactor(BaseModel):
    """Individual risk factor"""
    factor_name: str
    factor_type: str
    severity: str  # low, medium, high, critical
    description: str
    impact_score: float
    evidence: Optional[Dict[str, Any]] = None


class RiskScore(BaseModel):
    """Risk score model"""
    score_id: str
    search_id: Optional[str] = None
    property_address: Optional[Dict[str, str]] = None
    overall_risk_score: float  # 0-100
    risk_level: RiskLevel
    risk_factors: List[RiskFactor]
    recommendations: List[str]
    created_at: datetime
    model_version: str

