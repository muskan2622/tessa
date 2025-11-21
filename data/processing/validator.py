"""
Data Validation
Validate data quality and completeness
"""
from typing import Dict, Any, List, Tuple
import re
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class DataValidator:
    """Validate data quality and completeness"""
    
    # US state codes
    US_STATES = {
        "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA",
        "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
        "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
        "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
        "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY", "DC"
    }
    
    @staticmethod
    def validate_address(address: Dict[str, str]) -> Tuple[bool, List[str]]:
        """
        Validate address data
        
        Args:
            address: Address dictionary
            
        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []
        
        # Required fields
        required_fields = ["street", "city", "state", "zip_code"]
        for field in required_fields:
            if not address.get(field):
                errors.append(f"Missing required field: {field}")
        
        # Validate state code
        state = address.get("state", "").upper()
        if state and state not in DataValidator.US_STATES:
            errors.append(f"Invalid state code: {state}")
        
        # Validate zip code format
        zip_code = address.get("zip_code", "")
        if zip_code:
            zip_clean = re.sub(r"[^\d]", "", zip_code)
            if len(zip_clean) < 5 or len(zip_clean) > 9:
                errors.append(f"Invalid zip code format: {zip_code}")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def validate_date(date: datetime, min_date: datetime = None, max_date: datetime = None) -> Tuple[bool, str]:
        """
        Validate date
        
        Args:
            date: Date to validate
            min_date: Minimum allowed date
            max_date: Maximum allowed date
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not date:
            return False, "Date is required"
        
        if not isinstance(date, datetime):
            return False, "Date must be a datetime object"
        
        if min_date and date < min_date:
            return False, f"Date is before minimum date: {min_date}"
        
        if max_date and date > max_date:
            return False, f"Date is after maximum date: {max_date}"
        
        return True, ""
    
    @staticmethod
    def validate_amount(amount: float, min_amount: float = None, max_amount: float = None) -> Tuple[bool, str]:
        """
        Validate monetary amount
        
        Args:
            amount: Amount to validate
            min_amount: Minimum allowed amount
            max_amount: Maximum allowed amount
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if amount is None:
            return False, "Amount is required"
        
        if not isinstance(amount, (int, float)):
            return False, "Amount must be a number"
        
        if amount < 0:
            return False, "Amount cannot be negative"
        
        if min_amount is not None and amount < min_amount:
            return False, f"Amount is below minimum: {min_amount}"
        
        if max_amount is not None and amount > max_amount:
            return False, f"Amount is above maximum: {max_amount}"
        
        return True, ""
    
    @staticmethod
    def validate_email(email: str) -> Tuple[bool, str]:
        """
        Validate email address
        
        Args:
            email: Email string
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not email:
            return False, "Email is required"
        
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(pattern, email):
            return False, "Invalid email format"
        
        return True, ""
    
    @staticmethod
    def validate_document_number(doc_num: str) -> Tuple[bool, str]:
        """
        Validate document number
        
        Args:
            doc_num: Document number string
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not doc_num:
            return False, "Document number is required"
        
        if len(doc_num) < 3:
            return False, "Document number is too short"
        
        if len(doc_num) > 100:
            return False, "Document number is too long"
        
        return True, ""

