"""
Title search data models
"""
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from enum import Enum

from backend.models.property import PropertyAddress


class TitleSearchStatus(str, Enum):
    """Title search status"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class Deed(BaseModel):
    """Deed information"""
    deed_type: str
    grantor: str
    grantee: str
    recording_date: datetime
    document_number: str
    book_page: Optional[str] = None


class Lien(BaseModel):
    """Lien information"""
    lien_type: str
    creditor: str
    amount: Optional[float] = None
    recording_date: datetime
    document_number: str
    status: str


class Encumbrance(BaseModel):
    """Encumbrance information"""
    encumbrance_type: str
    description: str
    recording_date: datetime
    document_number: str


class TitleSearch(BaseModel):
    """Title search model"""
    search_id: str
    property_address: PropertyAddress
    search_type: str
    include_historical: bool
    jurisdiction: str
    user_id: str
    status: TitleSearchStatus
    deeds: List[Deed] = []
    liens: List[Lien] = []
    encumbrances: List[Encumbrance] = []
    created_at: datetime
    completed_at: Optional[datetime] = None
    risk_score: Optional[float] = None

