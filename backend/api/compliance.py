"""
Compliance checking API endpoints
Handles regulatory compliance checks (RESPA, TILA, state-specific rules)
"""
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

from backend.services.compliance_service import ComplianceService
from backend.api.auth import get_current_user, User
from fastapi import HTTPException

router = APIRouter()


class ComplianceRule(str, Enum):
    """Compliance rule types"""
    RESPA = "respa"
    TILA = "tila"
    STATE_SPECIFIC = "state_specific"
    LOCAL_JURISDICTION = "local_jurisdiction"


class ComplianceStatus(str, Enum):
    """Compliance check status"""
    PASS = "pass"
    FAIL = "fail"
    WARNING = "warning"
    PENDING = "pending"


class ComplianceCheck(BaseModel):
    """Individual compliance check result"""
    rule_name: str
    rule_type: ComplianceRule
    status: ComplianceStatus
    description: str
    details: Optional[Dict[str, Any]] = None
    violations: List[str] = []
    recommendations: List[str] = []


class ComplianceReport(BaseModel):
    """Compliance report"""
    report_id: str
    search_id: Optional[str] = None
    property_address: Optional[Dict[str, str]] = None
    jurisdiction: str
    checks: List[ComplianceCheck]
    overall_status: ComplianceStatus
    created_at: datetime
    checked_by: str


class ComplianceCheckRequest(BaseModel):
    """Request for compliance check"""
    search_id: Optional[str] = None
    property_address: Optional[Dict[str, str]] = None
    jurisdiction: str
    rules_to_check: Optional[List[ComplianceRule]] = None  # None = check all


@router.post("/check", response_model=ComplianceReport)
async def run_compliance_check(
    request: ComplianceCheckRequest,
    current_user: User = Depends(get_current_user)
):
    """Run compliance checks for a property or title search"""
    service = ComplianceService()
    
    report = await service.run_compliance_check(
        search_id=request.search_id,
        property_address=request.property_address,
        jurisdiction=request.jurisdiction,
        rules_to_check=request.rules_to_check,
        user_id=current_user.username
    )
    
    return report


@router.get("/report/{report_id}", response_model=ComplianceReport)
async def get_compliance_report(
    report_id: str,
    current_user: User = Depends(get_current_user)
):
    """Get a specific compliance report by ID"""
    service = ComplianceService()
    report = await service.get_compliance_report(report_id)
    
    if not report:
        raise HTTPException(status_code=404, detail="Compliance report not found")
    
    return report


@router.get("/reports", response_model=List[ComplianceReport])
async def list_compliance_reports(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user)
):
    """List all compliance reports for the current user"""
    service = ComplianceService()
    reports = await service.list_compliance_reports(
        user_id=current_user.username,
        skip=skip,
        limit=limit
    )
    return reports

