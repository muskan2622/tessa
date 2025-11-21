"""
Title search API endpoints
Handles automated title searches, property record retrieval, and lien detection
"""
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum

from backend.services.title_search_service import TitleSearchService
from backend.api.auth import get_current_user, User

router = APIRouter()


class SearchType(str, Enum):
    """Types of title searches"""
    FULL = "full"
    QUICK = "quick"
    LIEN_ONLY = "lien_only"
    ENCUMBRANCE_ONLY = "encumbrance_only"


class PropertyAddress(BaseModel):
    """Property address model"""
    street: str
    city: str
    state: str
    zip_code: str
    county: Optional[str] = None
    parcel_number: Optional[str] = None


class TitleSearchRequest(BaseModel):
    """Request model for title search"""
    property_address: PropertyAddress
    search_type: SearchType = SearchType.FULL
    include_historical: bool = False
    jurisdiction: Optional[str] = None


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


class TitleSearchResult(BaseModel):
    """Title search result"""
    search_id: str
    property_address: PropertyAddress
    status: str
    deeds: List[Deed] = []
    liens: List[Lien] = []
    encumbrances: List[Encumbrance] = []
    created_at: datetime
    completed_at: Optional[datetime] = None
    risk_score: Optional[float] = None


@router.post("/search", response_model=TitleSearchResult)
async def create_title_search(
    request: TitleSearchRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user)
):
    """Initiate a new title search"""
    service = TitleSearchService()
    
    # Start search in background
    search_result = await service.initiate_search(
        property_address=request.property_address,
        search_type=request.search_type,
        include_historical=request.include_historical,
        jurisdiction=request.jurisdiction,
        user_id=current_user.username
    )
    
    # Process search asynchronously
    background_tasks.add_task(
        service.process_search,
        search_result.search_id
    )
    
    return search_result


@router.get("/search/{search_id}", response_model=TitleSearchResult)
async def get_title_search(
    search_id: str,
    current_user: User = Depends(get_current_user)
):
    """Get title search results by ID"""
    service = TitleSearchService()
    result = await service.get_search_result(search_id)
    
    if not result:
        raise HTTPException(status_code=404, detail="Title search not found")
    
    return result


@router.get("/searches", response_model=List[TitleSearchResult])
async def list_title_searches(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user)
):
    """List all title searches for the current user"""
    service = TitleSearchService()
    results = await service.list_searches(
        user_id=current_user.username,
        skip=skip,
        limit=limit
    )
    return results

