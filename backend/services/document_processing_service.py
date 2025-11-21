"""
Document Processing Service
Handles document parsing, classification, and extraction using AI models
"""
import uuid
from datetime import datetime
from typing import Optional, List, Dict, Any
from backend.models.document import Document, DocumentType, DocumentStatus
from backend.agents.document_agent import DocumentAgent
from backend.utils.database import get_db_session


class DocumentProcessingService:
    """Service for processing real estate documents"""
    
    def __init__(self):
        self.agent = DocumentAgent()
    
    async def upload_document(
        self,
        file_content: bytes,
        file_name: str,
        document_type: Optional[DocumentType],
        user_id: str
    ) -> str:
        """Upload a document and create a record"""
        document_id = str(uuid.uuid4())
        
        # Detect document type if not provided
        if not document_type:
            document_type = await self.agent.detect_document_type(file_content)
        
        # Create document record
        document = Document(
            document_id=document_id,
            file_name=file_name,
            file_size=len(file_content),
            document_type=document_type,
            status=DocumentStatus.PENDING,
            uploaded_at=datetime.utcnow(),
            user_id=user_id
        )
        
        # TODO: Save file to S3 and metadata to database
        # await self._save_to_s3(document_id, file_content)
        # async with get_db_session() as session:
        #     session.add(document)
        #     await session.commit()
        
        return document_id
    
    async def process_document(self, document_id: str) -> Optional[Dict[str, Any]]:
        """Process a document and extract structured data"""
        # TODO: Load document from database
        # For now, use agent to process
        result = await self.agent.extract_document_data(document_id)
        
        # TODO: Update document in database with extracted data
        return result
    
    async def get_document(self, document_id: str) -> Optional[Document]:
        """Get document metadata by ID"""
        # TODO: Load from database
        return None
    
    async def list_documents(
        self,
        user_id: str,
        skip: int = 0,
        limit: int = 100,
        document_type: Optional[DocumentType] = None
    ) -> List[Document]:
        """List all documents for a user"""
        # TODO: Query database
        return []

