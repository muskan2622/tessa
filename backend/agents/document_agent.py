"""
Document Agent
AI agent for document understanding, classification, and extraction
"""
from typing import Dict, Any, Optional
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
import os

from backend.models.document import DocumentType


class DocumentAgent:
    """AI agent for document processing"""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model=os.getenv("LLM_MODEL", "gpt-4"),
            temperature=0,
            api_key=os.getenv("OPENAI_API_KEY")
        )
        self.document_chain = self._create_document_chain()
    
    def _create_document_chain(self):
        """Create document processing chain"""
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert document analysis agent for real estate documents.
            Your role is to:
            1. Classify document types (deed, lien, mortgage, title policy, etc.)
            2. Extract structured data from documents
            3. Identify key information (parties, dates, amounts, legal descriptions)
            4. Flag any anomalies or concerns
            
            Always provide accurate, structured output."""),
            ("user", "{input}")
        ])
        
        return LLMChain(llm=self.llm, prompt=prompt)
    
    async def detect_document_type(self, file_content: bytes) -> DocumentType:
        """Detect document type from file content"""
        # TODO: Use OCR + LLM to detect document type
        # For now, return default
        return DocumentType.OTHER
    
    async def extract_document_data(self, document_id: str) -> Dict[str, Any]:
        """Extract structured data from document"""
        # TODO: Load document from storage, perform OCR, extract data
        result = await self.document_chain.ainvoke({
            "input": f"Extract structured data from document ID: {document_id}"
        })
        
        return {
            "document_id": document_id,
            "extracted_data": result["text"],
            "confidence_score": 0.95
        }
    
    async def classify_document(self, file_content: bytes) -> DocumentType:
        """Classify document type"""
        # TODO: Implement document classification
        return DocumentType.OTHER

