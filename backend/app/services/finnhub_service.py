import httpx
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta

from app.core.config import settings

logger = logging.getLogger(__name__)

class FinnhubService:
    """Service to fetch data from Finnhub API."""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or settings.FINNHUB_API_KEY
        self.base_url = "https://finnhub.io/api/v1"
        
    async def get_company_news(
        self, 
        ticker: str, 
        limit: int = 10, 
        published_after: Optional[datetime] = None
    ) -> List[Dict[Any, Any]]:
        """
        Fetch news for a specific ticker from Finnhub API.
        
        Args:
            ticker: Stock ticker symbol
            limit: Maximum number of news items to return
            published_after: Only return news published after this datetime
            
        Returns:
            List of news articles
        """
        if not self.api_key:
            logger.warning("Finnhub API key not set, skipping news fetch")
            return []
            
        # Set default published_after to 7 days ago if not provided
        if published_after is None:
            published_after = datetime.now() - timedelta(days=settings.MAX_NEWS_AGE_DAYS)
            
        # Format dates for API
        from_date = published_after.strftime("%Y-%m-%d")
        to_date = datetime.now().strftime("%Y-%m-%d")
        
        # Build URL
        url = f"{self.base_url}/company-news"
        
        # Set parameters
        params = {
            "symbol": ticker,
            "from": from_date,
            "to": to_date,
            "token": self.api_key
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=params)
                response.raise_for_status()
                data = response.json()
                
                # Limit the number of results
                return data[:limit] if isinstance(data, list) else []
                    
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 429:
                logger.warning("Finnhub API rate limit exceeded")
            logger.error(f"HTTP error fetching news from Finnhub: {str(e)}")
            return []
        except Exception as e:
            logger.error(f"Error fetching news from Finnhub: {str(e)}")
            return []
    
    async def get_company_sentiment(self, ticker: str) -> Dict[str, Any]:
        """
        Fetch social sentiment for a specific ticker from Finnhub API.
        
        Args:
            ticker: Stock ticker symbol
            
        Returns:
            Dictionary with sentiment data
        """
        if not self.api_key:
            logger.warning("Finnhub API key not set, skipping sentiment fetch")
            return {}
            
        # Build URL
        url = f"{self.base_url}/news-sentiment"
        
        # Set parameters
        params = {
            "symbol": ticker,
            "token": self.api_key
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=params)
                response.raise_for_status()
                return response.json()
                    
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error fetching sentiment from Finnhub: {str(e)}")
            return {}
        except Exception as e:
            logger.error(f"Error fetching sentiment from Finnhub: {str(e)}")
            return {}
