"""
Title Search Service
Handles automated title searches, property record retrieval, and lien detection
"""
import uuid
from datetime import datetime
from typing import Optional, List
from backend.models.property import PropertyAddress
from backend.models.title_search import TitleSearch, TitleSearchStatus
from backend.agents.title_search_agent import TitleSearchAgent
from backend.utils.database import get_db_session


class TitleSearchService:
    """Service for managing title searches"""
    
    def __init__(self):
        self.agent = TitleSearchAgent()
    
    async def initiate_search(
        self,
        property_address: PropertyAddress,
        search_type: str,
        include_historical: bool,
        jurisdiction: Optional[str],
        user_id: str
    ):
        """Initiate a new title search"""
        search_id = str(uuid.uuid4())
        
        # Create search record
        search = TitleSearch(
            search_id=search_id,
            property_address=property_address,
            search_type=search_type,
            include_historical=include_historical,
            jurisdiction=jurisdiction or property_address.state,
            user_id=user_id,
            status=TitleSearchStatus.PENDING,
            created_at=datetime.utcnow()
        )
        
        # TODO: Save to database
        # async with get_db_session() as session:
        #     session.add(search)
        #     await session.commit()
        
        return search
    
    async def process_search(self, search_id: str):
        """Process a title search using AI agents"""
        # TODO: Load search from database
        # For now, use agent to process
        result = await self.agent.search_title(search_id)
        
        # TODO: Update search in database with results
        return result
    
    async def get_search_result(self, search_id: str) -> Optional[TitleSearch]:
        """Get title search result by ID"""
        # TODO: Load from database
        # For now, return None
        return None
    
    async def list_searches(
        self,
        user_id: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[TitleSearch]:
        """List all title searches for a user"""
        # TODO: Query database
        return []

