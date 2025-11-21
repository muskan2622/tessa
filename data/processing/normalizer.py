"""
Data Normalization
Clean and normalize data from various sources
"""
from typing import Dict, Any, List
import re
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class DataNormalizer:
    """Normalize data from various sources to common format"""
    
    @staticmethod
    def normalize_address(address: Dict[str, Any]) -> Dict[str, str]:
        """
        Normalize address to standard format
        
        Args:
            address: Address dictionary with various field names
            
        Returns:
            Normalized address dictionary
        """
        normalized = {
            "street": "",
            "city": "",
            "state": "",
            "zip_code": "",
            "county": ""
        }
        
        # Map various field names to standard format
        field_mapping = {
            "street": ["street", "street_address", "address_line_1", "address1"],
            "city": ["city", "municipality"],
            "state": ["state", "province", "state_code"],
            "zip_code": ["zip_code", "zip", "postal_code", "zipcode"],
            "county": ["county", "parish"]
        }
        
        for standard_field, variants in field_mapping.items():
            for variant in variants:
                if variant in address:
                    value = str(address[variant]).strip()
                    if value:
                        normalized[standard_field] = value
                        break
        
        # Normalize state to uppercase 2-letter code
        if normalized["state"]:
            normalized["state"] = normalized["state"].upper()[:2]
        
        # Normalize zip code (remove dashes, ensure 5 or 9 digits)
        if normalized["zip_code"]:
            zip_clean = re.sub(r"[^\d]", "", normalized["zip_code"])
            if len(zip_clean) >= 5:
                normalized["zip_code"] = zip_clean[:5]
                if len(zip_clean) > 5:
                    normalized["zip_code"] += f"-{zip_clean[5:9]}"
        
        return normalized
    
    @staticmethod
    def normalize_date(date_str: Any) -> datetime:
        """
        Normalize date string to datetime object
        
        Args:
            date_str: Date string in various formats
            
        Returns:
            datetime object
        """
        if isinstance(date_str, datetime):
            return date_str
        
        if not date_str:
            return None
        
        # Common date formats
        date_formats = [
            "%Y-%m-%d",
            "%m/%d/%Y",
            "%d/%m/%Y",
            "%Y-%m-%d %H:%M:%S",
            "%m-%d-%Y",
            "%d-%m-%Y"
        ]
        
        for fmt in date_formats:
            try:
                return datetime.strptime(str(date_str).strip(), fmt)
            except ValueError:
                continue
        
        logger.warning(f"Could not parse date: {date_str}")
        return None
    
    @staticmethod
    def normalize_amount(amount: Any) -> float:
        """
        Normalize monetary amount to float
        
        Args:
            amount: Amount in various formats (string, number, etc.)
            
        Returns:
            float amount
        """
        if isinstance(amount, (int, float)):
            return float(amount)
        
        if not amount:
            return 0.0
        
        # Remove currency symbols and commas
        amount_str = re.sub(r"[^\d.]", "", str(amount))
        
        try:
            return float(amount_str)
        except ValueError:
            logger.warning(f"Could not parse amount: {amount}")
            return 0.0
    
    @staticmethod
    def normalize_name(name: str) -> str:
        """
        Normalize person/entity name
        
        Args:
            name: Name string
            
        Returns:
            Normalized name (title case, trimmed)
        """
        if not name:
            return ""
        
        # Trim and title case
        normalized = " ".join(name.strip().split())
        return normalized.title()
    
    @staticmethod
    def normalize_document_number(doc_num: Any) -> str:
        """
        Normalize document number
        
        Args:
            doc_num: Document number in various formats
            
        Returns:
            Normalized document number string
        """
        if not doc_num:
            return ""
        
        # Remove special characters, keep alphanumeric
        normalized = re.sub(r"[^\w]", "", str(doc_num))
        return normalized.upper()

