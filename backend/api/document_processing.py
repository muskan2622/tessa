"""
Document processing API endpoints
Handles document parsing, classification, and extraction
"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

from backend.services.document_processing_service import DocumentProcessingService
from backend.api.auth import get_current_user, User

router = APIRouter()


class DocumentType(str, Enum):
    """Types of real estate documents"""
    DEED = "deed"
    LIEN = "lien"
    MORTGAGE = "mortgage"
    TITLE_POLICY = "title_policy"
    SURVEY = "survey"
    ENCUMBRANCE = "encumbrance"
    OTHER = "other"


class DocumentStatus(str, Enum):
    """Document processing status"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class DocumentMetadata(BaseModel):
    """Document metadata"""
    document_id: str
    document_type: DocumentType
    file_name: str
    file_size: int
    uploaded_at: datetime
    processed_at: Optional[datetime] = None
    status: DocumentStatus
    extracted_data: Optional[Dict[str, Any]] = None
    confidence_score: Optional[float] = None


class DocumentUploadResponse(BaseModel):
    """Response after document upload"""
    document_id: str
    status: DocumentStatus
    message: str


class DocumentExtractionResult(BaseModel):
    """Document extraction result"""
    document_id: str
    document_type: DocumentType
    extracted_fields: Dict[str, Any]
    confidence_score: float
    processing_time_seconds: float


@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    document_type: Optional[DocumentType] = None,
    current_user: User = Depends(get_current_user)
):
    """Upload and process a document"""
    service = DocumentProcessingService()
    
    # Validate file type
    allowed_extensions = {".pdf", ".tiff", ".tif", ".jpg", ".jpeg", ".png"}
    file_ext = "." + file.filename.split(".")[-1].lower() if "." in file.filename else ""
    
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"File type not supported. Allowed: {allowed_extensions}"
        )
    
    # Read file content
    content = await file.read()
    
    # Upload and process
    document_id = await service.upload_document(
        file_content=content,
        file_name=file.filename,
        document_type=document_type,
        user_id=current_user.username
    )
    
    return DocumentUploadResponse(
        document_id=document_id,
        status=DocumentStatus.PENDING,
        message="Document uploaded successfully"
    )


@router.get("/{document_id}", response_model=DocumentMetadata)
async def get_document(
    document_id: str,
    current_user: User = Depends(get_current_user)
):
    """Get document metadata and extracted data"""
    service = DocumentProcessingService()
    document = await service.get_document(document_id)
    
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    return document


@router.post("/{document_id}/process", response_model=DocumentExtractionResult)
async def process_document(
    document_id: str,
    current_user: User = Depends(get_current_user)
):
    """Process a document and extract structured data"""
    service = DocumentProcessingService()
    
    result = await service.process_document(document_id)
    
    if not result:
        raise HTTPException(
            status_code=404,
            detail="Document not found or processing failed"
        )
    
    return result


@router.get("/", response_model=List[DocumentMetadata])
async def list_documents(
    skip: int = 0,
    limit: int = 100,
    document_type: Optional[DocumentType] = None,
    current_user: User = Depends(get_current_user)
):
    """List all documents for the current user"""
    service = DocumentProcessingService()
    documents = await service.list_documents(
        user_id=current_user.username,
        skip=skip,
        limit=limit,
        document_type=document_type
    )
    return documents

