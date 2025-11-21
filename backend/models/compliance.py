"""
Compliance data models
"""
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


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
    """Compliance report model"""
    report_id: str
    search_id: Optional[str] = None
    property_address: Optional[Dict[str, Any]] = None
    jurisdiction: str
    checks: List[ComplianceCheck]
    overall_status: ComplianceStatus
    created_at: datetime
    checked_by: str

