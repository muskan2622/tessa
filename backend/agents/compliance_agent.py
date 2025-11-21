"""
Compliance Agent
AI agent for regulatory compliance checking
"""
from typing import Dict, Any, Optional, List
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
import os

from backend.models.compliance import ComplianceCheck, ComplianceRule, ComplianceStatus


class ComplianceAgent:
    """AI agent for compliance checking"""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model=os.getenv("LLM_MODEL", "gpt-4"),
            temperature=0,
            api_key=os.getenv("OPENAI_API_KEY")
        )
        self.compliance_chain = self._create_compliance_chain()
    
    def _create_compliance_chain(self):
        """Create compliance checking chain"""
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert compliance agent for real estate transactions.
            Your role is to check compliance with:
            1. RESPA (Real Estate Settlement Procedures Act)
            2. TILA (Truth in Lending Act)
            3. State-specific regulations
            4. Local jurisdiction rules
            
            For each rule, check if the transaction complies and report any violations.
            Provide structured output with status (pass/fail/warning) and recommendations."""),
            ("user", "{input}")
        ])
        
        return LLMChain(llm=self.llm, prompt=prompt)
    
    async def check_compliance(
        self,
        search_id: Optional[str],
        property_address: Optional[Dict[str, str]],
        jurisdiction: str,
        rules_to_check: List[ComplianceRule]
    ) -> List[ComplianceCheck]:
        """Run compliance checks"""
        checks = []
        
        # Build input for each rule
        for rule in rules_to_check:
            input_text = f"Check {rule.value} compliance"
            if search_id:
                input_text += f" for search ID: {search_id}"
            if property_address:
                input_text += f" in {jurisdiction}"
            
            # TODO: Load actual transaction data
            result = await self.compliance_chain.ainvoke({"input": input_text})
            
            # Parse result and create compliance check
            # In production, use structured output or rule engine
            check = ComplianceCheck(
                rule_name=rule.value.upper(),
                rule_type=rule,
                status=ComplianceStatus.PASS,  # Default, should be determined from result
                description=f"Compliance check for {rule.value}",
                violations=[],
                recommendations=[]
            )
            
            checks.append(check)
        
        return checks

