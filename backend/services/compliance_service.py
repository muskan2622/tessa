"""
Compliance Service
Handles regulatory compliance checks (RESPA, TILA, state-specific rules)
"""
import uuid
from datetime import datetime
from typing import Optional, List, Dict, Any
from backend.models.compliance import ComplianceReport, ComplianceStatus, ComplianceRule
from backend.agents.compliance_agent import ComplianceAgent
from backend.utils.database import get_db_session


class ComplianceService:
    """Service for compliance checking"""
    
    def __init__(self):
        self.agent = ComplianceAgent()
    
    async def run_compliance_check(
        self,
        search_id: Optional[str],
        property_address: Optional[Dict[str, str]],
        jurisdiction: str,
        rules_to_check: Optional[List[ComplianceRule]],
        user_id: str
    ) -> ComplianceReport:
        """Run compliance checks using rule engine and ML"""
        report_id = str(uuid.uuid4())
        
        # Use agent to check compliance
        checks = await self.agent.check_compliance(
            search_id=search_id,
            property_address=property_address,
            jurisdiction=jurisdiction,
            rules_to_check=rules_to_check or list(ComplianceRule)
        )
        
        # Determine overall status
        overall_status = self._determine_overall_status(checks)
        
        # Create compliance report
        report = ComplianceReport(
            report_id=report_id,
            search_id=search_id,
            property_address=property_address,
            jurisdiction=jurisdiction,
            checks=checks,
            overall_status=overall_status,
            created_at=datetime.utcnow(),
            checked_by=user_id
        )
        
        # TODO: Save to database
        # async with get_db_session() as session:
        #     session.add(report)
        #     await session.commit()
        
        return report
    
    def _determine_overall_status(self, checks: List[Any]) -> ComplianceStatus:
        """Determine overall compliance status from checks"""
        if not checks:
            return ComplianceStatus.PENDING
        
        has_failures = any(check.status == ComplianceStatus.FAIL for check in checks)
        has_warnings = any(check.status == ComplianceStatus.WARNING for check in checks)
        
        if has_failures:
            return ComplianceStatus.FAIL
        elif has_warnings:
            return ComplianceStatus.WARNING
        else:
            return ComplianceStatus.PASS
    
    async def get_compliance_report(self, report_id: str) -> Optional[ComplianceReport]:
        """Get compliance report by ID"""
        # TODO: Load from database
        return None
    
    async def list_compliance_reports(
        self,
        user_id: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[ComplianceReport]:
        """List all compliance reports for a user"""
        # TODO: Query database
        return []

