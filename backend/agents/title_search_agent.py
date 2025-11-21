"""
Title Search Agent
AI agent for automated title searches using RAG and LLM
"""
from typing import Dict, Any, Optional
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.tools import Tool
import os

from backend.models.title_search import TitleSearch


class TitleSearchAgent:
    """AI agent for title search automation"""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model=os.getenv("LLM_MODEL", "gpt-4"),
            temperature=0,
            api_key=os.getenv("OPENAI_API_KEY")
        )
        self.agent = self._create_agent()
    
    def _create_agent(self):
        """Create the title search agent"""
        # Define tools for the agent
        tools = [
            Tool(
                name="search_county_records",
                func=self._search_county_records,
                description="Search county recorder office for property records, deeds, and liens"
            ),
            Tool(
                name="search_court_records",
                func=self._search_court_records,
                description="Search court records for judgments and legal actions"
            ),
            Tool(
                name="check_mls_data",
                func=self._check_mls_data,
                description="Check MLS (Multiple Listing Service) for property listing data"
            ),
            Tool(
                name="analyze_documents",
                func=self._analyze_documents,
                description="Analyze and extract information from property documents"
            )
        ]
        
        # Create prompt template
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert title search agent for real estate transactions.
            Your role is to:
            1. Search county records for property deeds, liens, and encumbrances
            2. Check court records for judgments and legal issues
            3. Verify property information from MLS data
            4. Analyze documents to extract key information
            5. Compile comprehensive title search results
            
            Always be thorough and accurate. Report any issues or concerns you find."""),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ])
        
        # Create agent
        agent = create_openai_functions_agent(self.llm, tools, prompt)
        return AgentExecutor(agent=agent, tools=tools, verbose=True)
    
    async def search_title(self, search_id: str) -> Dict[str, Any]:
        """Execute title search"""
        # TODO: Load search details from database
        # For now, return mock result
        result = await self.agent.ainvoke({
            "input": f"Perform a comprehensive title search for search ID: {search_id}"
        })
        
        return {
            "search_id": search_id,
            "status": "completed",
            "result": result
        }
    
    def _search_county_records(self, query: str) -> str:
        """Search county records (mock implementation)"""
        # TODO: Implement actual county API integration
        return f"County records search for: {query}"
    
    def _search_court_records(self, query: str) -> str:
        """Search court records (mock implementation)"""
        # TODO: Implement actual court records API integration
        return f"Court records search for: {query}"
    
    def _check_mls_data(self, query: str) -> str:
        """Check MLS data (mock implementation)"""
        # TODO: Implement actual MLS API integration
        return f"MLS data check for: {query}"
    
    def _analyze_documents(self, query: str) -> str:
        """Analyze documents (mock implementation)"""
        # TODO: Implement document analysis using document agent
        return f"Document analysis for: {query}"

