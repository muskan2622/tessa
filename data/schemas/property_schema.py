"""
Property Data Schema
Schema definitions for property-related data
"""
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime


class PropertySchema(BaseModel):
    """Property data schema"""
    property_id: Optional[str] = None
    street: str = Field(..., min_length=1, max_length=255)
    city: str = Field(..., min_length=1, max_length=255)
    state: str = Field(..., min_length=2, max_length=2)
    zip_code: str = Field(..., min_length=5, max_length=10)
    county: Optional[str] = None
    parcel_number: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    @validator("state")
    def validate_state(cls, v):
        """Validate US state code"""
        v = v.upper()
        us_states = {
            "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA",
            "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
            "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
            "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
            "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY", "DC"
        }
        if v not in us_states:
            raise ValueError(f"Invalid state code: {v}")
        return v


class DeedSchema(BaseModel):
    """Deed data schema"""
    deed_id: Optional[str] = None
    search_id: str
    deed_type: str
    grantor: str = Field(..., min_length=1)
    grantee: str = Field(..., min_length=1)
    recording_date: datetime
    document_number: str
    book_page: Optional[str] = None


class LienSchema(BaseModel):
    """Lien data schema"""
    lien_id: Optional[str] = None
    search_id: str
    lien_type: str
    creditor: str = Field(..., min_length=1)
    amount: Optional[float] = Field(None, ge=0)
    recording_date: datetime
    document_number: str
    status: str


class EncumbranceSchema(BaseModel):
    """Encumbrance data schema"""
    encumbrance_id: Optional[str] = None
    search_id: str
    encumbrance_type: str
    description: str = Field(..., min_length=1)
    recording_date: datetime
    document_number: str

