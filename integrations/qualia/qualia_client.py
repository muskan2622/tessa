"""
Qualia Integration Client
Integrates with Qualia title software
"""
import aiohttp
from typing import Dict, Any, Optional, List
import os
import logging

logger = logging.getLogger(__name__)


class QualiaClient:
    """Qualia API client"""
    
    def __init__(self):
        """Initialize Qualia client"""
        self.api_key = os.getenv("QUALIA_API_KEY")
        self.base_url = os.getenv("QUALIA_BASE_URL", "https://api.qualia.com/v1")
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    async def create_title_order(
        self,
        property_address: Dict[str, str],
        borrower_name: str,
        lender_name: str = None
    ) -> Optional[Dict[str, Any]]:
        """
        Create a title order in Qualia
        
        Args:
            property_address: Property address dictionary
            borrower_name: Borrower name
            lender_name: Lender name (optional)
            
        Returns:
            Qualia order data or None
        """
        if not self.api_key:
            logger.error("Qualia API key not configured")
            return None
        
        order_data = {
            "property": {
                "address": {
                    "street": property_address.get("street"),
                    "city": property_address.get("city"),
                    "state": property_address.get("state"),
                    "zip": property_address.get("zip_code")
                }
            },
            "borrower": {
                "name": borrower_name
            }
        }
        
        if lender_name:
            order_data["lender"] = {"name": lender_name}
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/orders",
                    headers=self.headers,
                    json=order_data
                ) as response:
                    if response.status == 201:
                        return await response.json()
                    else:
                        error_text = await response.text()
                        logger.error(f"Qualia API error: {response.status} - {error_text}")
                        return None
        except Exception as e:
            logger.error(f"Error creating Qualia order: {e}")
            return None
    
    async def get_order_status(self, order_id: str) -> Optional[Dict[str, Any]]:
        """Get order status from Qualia"""
        if not self.api_key:
            return None
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/orders/{order_id}",
                    headers=self.headers
                ) as response:
                    if response.status == 200:
                        return await response.json()
                    return None
        except Exception as e:
            logger.error(f"Error fetching Qualia order: {e}")
            return None

