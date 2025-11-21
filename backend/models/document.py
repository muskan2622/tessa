"""
Document data models
"""
from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime
from enum import Enum


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


class Document(BaseModel):
    """Document model"""
    document_id: str
    file_name: str
    file_size: int
    document_type: DocumentType
    status: DocumentStatus
    uploaded_at: datetime
    processed_at: Optional[datetime] = None
    user_id: str
    extracted_data: Optional[Dict[str, Any]] = None
    confidence_score: Optional[float] = None
    s3_key: Optional[str] = None

