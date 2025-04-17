import httpx
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta

from app.core.config import settings

logger = logging.getLogger(__name__)

class WhaleWisdomService:
    """Service to fetch data from WhaleWisdom API."""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or settings.WHALEWISDOM_API_KEY
        self.base_url = "https://whalewisdom.com/api"
        self.headers = {"Authorization": f"Bearer {self.api_key}"}
        
    async def get_institutional_holdings(
        self, 
        ticker: str
    ) -> List[Dict[Any, Any]]:
        """
        Fetch institutional holdings for a specific ticker from WhaleWisdom API.
        
        Args:
            ticker: Stock ticker symbol
            
        Returns:
            List of institutional holdings
        """
        if not self.api_key:
            logger.warning("WhaleWisdom API key not set, skipping holdings fetch")
            return []
            
        # Build URL
        url = f"{self.base_url}/v1/holdings"
        
        # Set parameters
        params = {
            "ticker": ticker,
            "limit": 20,
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=self.headers, params=params)
                response.raise_for_status()
                data = response.json()
                
                return data.get("data", [])
                    
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error fetching holdings from WhaleWisdom: {str(e)}")
            return []
        except Exception as e:
            logger.error(f"Error fetching holdings from WhaleWisdom: {str(e)}")
            return []
    
    async def get_insider_trading(
        self,
        ticker: str,
        limit: int = 10
    ) -> List[Dict[Any, Any]]:
        """
        Fetch insider trading data for a specific ticker from WhaleWisdom API.
        
        Args:
            ticker: Stock ticker symbol
            limit: Maximum number of transactions to return
            
        Returns:
            List of insider trading transactions
        """
        if not self.api_key:
            logger.warning("WhaleWisdom API key not set, skipping insider trading fetch")
            return []
            
        # Build URL
        url = f"{self.base_url}/v1/insider_trading"
        
        # Set parameters
        params = {
            "ticker": ticker,
            "limit": limit,
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=self.headers, params=params)
                response.raise_for_status()
                data = response.json()
                
                return data.get("data", [])
                    
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error fetching insider trading from WhaleWisdom: {str(e)}")
            return []
        except Exception as e:
            logger.error(f"Error fetching insider trading from WhaleWisdom: {str(e)}")
            return []
