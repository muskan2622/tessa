"""
MLS (Multiple Listing Service) Data Ingestion
ETL processes for MLS data feeds
"""
import asyncio
import aiohttp
from typing import List, Dict, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class MLSDataIngester:
    """Ingest MLS data"""
    
    def __init__(self, mls_api_config: Dict[str, Any]):
        """
        Initialize MLS data ingester
        
        Args:
            mls_api_config: Configuration for MLS API (RETS, REST API, etc.)
        """
        self.config = mls_api_config
        self.base_url = mls_api_config.get("base_url")
        self.api_key = mls_api_config.get("api_key")
        self.mls_id = mls_api_config.get("mls_id")
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "X-MLS-ID": self.mls_id
        }
    
    async def fetch_listing(
        self,
        mls_number: str = None,
        address: str = None,
        property_id: str = None
    ) -> Dict[str, Any]:
        """
        Fetch MLS listing data
        
        Args:
            mls_number: MLS listing number
            address: Property address
            property_id: Internal property ID
            
        Returns:
            Listing data dictionary
        """
        params = {}
        if mls_number:
            params["mls_number"] = mls_number
        elif address:
            params["address"] = address
        elif property_id:
            params["property_id"] = property_id
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/listings",
                    headers=self.headers,
                    params=params
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get("listing", {})
                    return {}
        except Exception as e:
            logger.error(f"Error fetching MLS listing: {e}")
            return {}
    
    async def fetch_property_history(
        self,
        mls_number: str
    ) -> List[Dict[str, Any]]:
        """Fetch property listing history"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/listings/{mls_number}/history",
                    headers=self.headers
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get("history", [])
                    return []
        except Exception as e:
            logger.error(f"Error fetching property history: {e}")
            return []

