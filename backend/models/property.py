"""
Property data models
"""
from pydantic import BaseModel
from typing import Optional


class PropertyAddress(BaseModel):
    """Property address model"""
    street: str
    city: str
    state: str
    zip_code: str
    county: Optional[str] = None
    parcel_number: Optional[str] = None
    
    def __str__(self):
        return f"{self.street}, {self.city}, {self.state} {self.zip_code}"

