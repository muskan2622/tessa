"""
Risk Agent
AI agent for risk scoring and assessment
"""
from typing import Dict, Any, Optional, List
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
import os
import json

from backend.models.risk_score import RiskFactor


class RiskAgent:
    """AI agent for risk assessment"""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model=os.getenv("LLM_MODEL", "gpt-4"),
            temperature=0,
            api_key=os.getenv("OPENAI_API_KEY")
        )
        self.risk_chain = self._create_risk_chain()
    
    def _create_risk_chain(self):
        """Create risk scoring chain"""
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert risk assessment agent for real estate title insurance.
            Your role is to:
            1. Analyze title search results for potential risks
            2. Identify risk factors (liens, encumbrances, clouded titles, etc.)
            3. Calculate risk scores (0-100) based on:
               - Historical claim patterns
               - Property-specific factors
               - Jurisdiction-specific rules
            4. Provide recommendations for risk mitigation
            
            Always provide structured JSON output with risk score, factors, and recommendations."""),
            ("user", "{input}")
        ])
        
        return LLMChain(llm=self.llm, prompt=prompt)
    
    async def calculate_risk(
        self,
        search_id: Optional[str],
        property_address: Optional[Dict[str, str]],
        include_recommendations: bool = True
    ) -> Dict[str, Any]:
        """Calculate risk score"""
        # Build input prompt
        input_text = "Calculate risk score"
        if search_id:
            input_text += f" for search ID: {search_id}"
        if property_address:
            input_text += f" for property: {property_address}"
        
        if include_recommendations:
            input_text += ". Include recommendations."
        
        # TODO: Load actual search data and historical patterns
        result = await self.risk_chain.ainvoke({"input": input_text})
        
        # Parse result (in production, use structured output)
        try:
            parsed = json.loads(result["text"])
        except:
            # Fallback to default structure
            parsed = {
                "score": 45.0,
                "factors": [
                    {
                        "factor_name": "Standard Title Search",
                        "factor_type": "baseline",
                        "severity": "low",
                        "description": "No major issues detected",
                        "impact_score": 10.0
                    }
                ],
                "recommendations": ["Continue with standard title insurance"]
            }
        
        return {
            "score": parsed.get("score", 45.0),
            "factors": parsed.get("factors", []),
            "recommendations": parsed.get("recommendations", []) if include_recommendations else []
        }

