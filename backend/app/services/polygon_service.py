import httpx
import asyncio
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import logging

from app.core.config import settings

logger = logging.getLogger(__name__)

class PolygonNewsService:
    """Service to fetch news from Polygon.io API."""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or settings.POLYGON_API_KEY
        self.base_url = "https://api.polygon.io/v2"
        self.headers = {"Authorization": f"Bearer {self.api_key}"}
        
    async def get_ticker_news(
        self, 
        ticker: str, 
        limit: int = 10, 
        published_after: Optional[datetime] = None
    ) -> List[Dict[Any, Any]]:
        """
        Fetch news for a specific ticker from Polygon.io.
        
        Args:
            ticker: Stock ticker symbol
            limit: Maximum number of news items to return
            published_after: Only return news published after this datetime
            
        Returns:
            List of news articles
        """
        if not self.api_key:
            logger.warning("Polygon API key not set, skipping news fetch")
            return []
            
        # Set default published_after to 7 days ago if not provided
        if published_after is None:
            published_after = datetime.now() - timedelta(days=settings.MAX_NEWS_AGE_DAYS)
            
        # Format date for API
        published_after_str = published_after.strftime("%Y-%m-%d")
        
        # Build URL
        url = f"{self.base_url}/reference/news"
        
        # Set parameters
        params = {
            "ticker": ticker,
            "limit": limit,
            "published_utc.gte": published_after_str,
            "order": "published_utc.desc",
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=self.headers, params=params)
                response.raise_for_status()
                data = response.json()
                
                if data.get("status") == "OK":
                    return data.get("results", [])
                else:
                    logger.error(f"Error fetching news from Polygon: {data.get('error')}")
                    return []
                    
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 429:
                logger.warning("Polygon API rate limit exceeded, consider implementing backoff")
            logger.error(f"HTTP error fetching news from Polygon: {str(e)}")
            return []
        except Exception as e:
            logger.error(f"Error fetching news from Polygon: {str(e)}")
            return []
            
    async def get_multiple_tickers_news(
        self, 
        tickers: List[str], 
        limit_per_ticker: int = 5,
        published_after: Optional[datetime] = None
    ) -> Dict[str, List[Dict[Any, Any]]]:
        """
        Fetch news for multiple tickers with rate limiting for free tier.
        
        Args:
            tickers: List of stock ticker symbols
            limit_per_ticker: Maximum number of news items per ticker
            published_after: Only return news published after this datetime
            
        Returns:
            Dictionary mapping tickers to their news articles
        """
        results = {}
        
        # For free tier, we need to be careful about rate limits
        # Process one ticker at a time with delay between requests
        for ticker in tickers:
            ticker_news = await self.get_ticker_news(
                ticker=ticker,
                limit=limit_per_ticker,
                published_after=published_after
            )
            results[ticker] = ticker_news
            
            # Add delay to avoid hitting rate limits on free tier
            await asyncio.sleep(0.5)
            
        return results
