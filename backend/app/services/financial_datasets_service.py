import httpx
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta

from app.core.config import settings

logger = logging.getLogger(__name__)

class FinancialDatasetsService:
    """Service to fetch data from Financial Datasets API."""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or settings.FINANCIAL_DATASETS_API_KEY
        self.base_url = "https://api.financialdatasets.ai/v1"
        self.headers = {"Authorization": f"Bearer {self.api_key}"}
        
    async def get_ticker_news(
        self, 
        ticker: str, 
        limit: int = 10, 
        published_after: Optional[datetime] = None
    ) -> List[Dict[Any, Any]]:
        """
        Fetch news for a specific ticker from Financial Datasets API.
        
        Args:
            ticker: Stock ticker symbol
            limit: Maximum number of news items to return
            published_after: Only return news published after this datetime
            
        Returns:
            List of news articles
        """
        if not self.api_key:
            logger.warning("Financial Datasets API key not set, skipping news fetch")
            return []
            
        # Set default published_after to 7 days ago if not provided
        if published_after is None:
            published_after = datetime.now() - timedelta(days=settings.MAX_NEWS_AGE_DAYS)
            
        # Format date for API
        published_after_str = published_after.strftime("%Y-%m-%dT%H:%M:%SZ")
        
        # Build URL
        url = f"{self.base_url}/news"
        
        # Set parameters
        params = {
            "symbol": ticker,
            "limit": limit,
            "from_date": published_after_str,
            "sort": "published_at:desc",
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=self.headers, params=params)
                response.raise_for_status()
                data = response.json()
                
                return data.get("data", [])
                    
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error fetching news from Financial Datasets: {str(e)}")
            return []
        except Exception as e:
            logger.error(f"Error fetching news from Financial Datasets: {str(e)}")
            return []
    
    async def get_company_filings(
        self,
        ticker: str,
        limit: int = 10,
        filed_after: Optional[datetime] = None
    ) -> List[Dict[Any, Any]]:
        """
        Fetch SEC filings for a specific ticker from Financial Datasets API.
        
        Args:
            ticker: Stock ticker symbol
            limit: Maximum number of filings to return
            filed_after: Only return filings filed after this datetime
            
        Returns:
            List of SEC filings
        """
        if not self.api_key:
            logger.warning("Financial Datasets API key not set, skipping filings fetch")
            return []
            
        # Set default filed_after to 30 days ago if not provided
        if filed_after is None:
            filed_after = datetime.now() - timedelta(days=30)
            
        # Format date for API
        filed_after_str = filed_after.strftime("%Y-%m-%dT%H:%M:%SZ")
        
        # Build URL
        url = f"{self.base_url}/sec/filings"
        
        # Set parameters
        params = {
            "symbol": ticker,
            "limit": limit,
            "from_date": filed_after_str,
            "sort": "filed_at:desc",
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=self.headers, params=params)
                response.raise_for_status()
                data = response.json()
                
                return data.get("data", [])
                    
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error fetching filings from Financial Datasets: {str(e)}")
            return []
        except Exception as e:
            logger.error(f"Error fetching filings from Financial Datasets: {str(e)}")
            return []
