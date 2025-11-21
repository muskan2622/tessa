"""
Court Records Ingestion
ETL processes for court records and judgments
"""
import asyncio
import aiohttp
from typing import List, Dict, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class CourtRecordsIngester:
    """Ingest court records and judgments"""
    
    def __init__(self, court_api_config: Dict[str, Any]):
        """
        Initialize court records ingester
        
        Args:
            court_api_config: Configuration for court API
        """
        self.config = court_api_config
        self.base_url = court_api_config.get("base_url")
        self.api_key = court_api_config.get("api_key")
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    async def fetch_judgments(
        self,
        party_name: str = None,
        property_address: str = None,
        date_from: datetime = None,
        date_to: datetime = None
    ) -> List[Dict[str, Any]]:
        """
        Fetch court judgments
        
        Args:
            party_name: Name of party to search
            property_address: Property address to search
            date_from: Start date
            date_to: End date
            
        Returns:
            List of judgments
        """
        params = {}
        if party_name:
            params["party"] = party_name
        if property_address:
            params["address"] = property_address
        if date_from:
            params["date_from"] = date_from.isoformat()
        if date_to:
            params["date_to"] = date_to.isoformat()
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/judgments",
                    headers=self.headers,
                    params=params
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get("judgments", [])
                    return []
        except Exception as e:
            logger.error(f"Error fetching judgments: {e}")
            return []
    
    async def fetch_legal_actions(
        self,
        property_address: str = None,
        party_name: str = None
    ) -> List[Dict[str, Any]]:
        """Fetch legal actions related to property or party"""
        params = {}
        if property_address:
            params["address"] = property_address
        if party_name:
            params["party"] = party_name
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/actions",
                    headers=self.headers,
                    params=params
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get("actions", [])
                    return []
        except Exception as e:
            logger.error(f"Error fetching legal actions: {e}")
            return []

