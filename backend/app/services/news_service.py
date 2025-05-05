import os
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session

from app.models.models import Article
from app.models.schemas import BiasDistribution, ArticleResponse

# API keys from environment variables
POLYGON_API_KEY = os.getenv("POLYGON_API_KEY")
FINANCIAL_DATASETS_API_KEY = os.getenv("FINANCIAL_DATASETS_API_KEY")
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")

class NewsService:
    """Service for fetching news from various sources"""
    
    def get_news_for_ticker(self, ticker: str, days: int = 7) -> List[Dict[str, Any]]:
        """
        Get news for a specific ticker from multiple sources
        
        Args:
            ticker: Stock ticker symbol
            days: Number of days to look back
            
        Returns:
            List of news articles
        """
        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # Format dates for API requests
        start_date_str = start_date.strftime("%Y-%m-%d")
        end_date_str = end_date.strftime("%Y-%m-%d")
        
        # Fetch from multiple sources and combine results
        polygon_news = self._get_polygon_news(ticker, start_date_str, end_date_str)
        finnhub_news = self._get_finnhub_news(ticker, start_date.timestamp(), end_date.timestamp())
        
        # Combine and deduplicate news (based on URL)
        all_news = polygon_news + finnhub_news
        unique_news = self._deduplicate_news(all_news)
        
        return unique_news
    
    def _get_polygon_news(self, ticker: str, start_date: str, end_date: str) -> List[Dict[str, Any]]:
        """Fetch news from Polygon.io"""
        if not POLYGON_API_KEY:
            print("Warning: POLYGON_API_KEY not set")
            return []
            
        url = f"https://api.polygon.io/v2/reference/news"
        params = {
            "ticker": ticker,
            "published_utc.gte": start_date,
            "published_utc.lte": end_date,
            "limit": 100,
            "apiKey": POLYGON_API_KEY
        }
        
        try:
            response = requests.get(url, params=params) 
            response.raise_for_status()
            data = response.json()
            
            # Transform to standard format
            articles = []
            for item in data.get("results", []):
                articles.append({
                    "headline": item.get("title", ""),
                    "summary": item.get("description", ""),
                    "url": item.get("article_url", ""),
                    "image_url": item.get("image_url", ""),
                    "published_date": item.get("published_utc", ""),
                    "source": {
                        "name": item.get("publisher", {}).get("name", ""),
                        "domain": self._extract_domain(item.get("article_url", ""))
                    }
                })
            
            return articles
        except Exception as e:
            print(f"Error fetching news from Polygon: {e}")
            return []
    
    def _get_finnhub_news(self, ticker: str, start_timestamp: float, end_timestamp: float) -> List[Dict[str, Any]]:
        """Fetch news from Finnhub"""
        if not FINNHUB_API_KEY:
            print("Warning: FINNHUB_API_KEY not set")
            return []
            
        url = "https://finnhub.io/api/v1/company-news"
        params = {
            "symbol": ticker,
            "from": datetime.fromtimestamp(start_timestamp).strftime("%Y-%m-%d"),
            "to": datetime.fromtimestamp(end_timestamp).strftime("%Y-%m-%d"),
            "token": FINNHUB_API_KEY
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Transform to standard format
            articles = []
            for item in data:
                articles.append({
                    "headline": item.get("headline", ""),
                    "summary": item.get("summary", ""),
                    "url": item.get("url", ""),
                    "image_url": item.get("image", ""),
                    "published_date": datetime.fromtimestamp(item.get("datetime", 0)).isoformat(),
                    "source": {
                        "name": item.get("source", ""),
                        "domain": self._extract_domain(item.get("url", ""))
                    }
                })
            
            return articles
        except Exception as e:
            print(f"Error fetching news from Finnhub: {e}")
            return []
    
    def _extract_domain(self, url: str) -> str:
        """Extract domain from URL"""
        try:
            from urllib.parse import urlparse
            parsed_url = urlparse(url)
            domain = parsed_url.netloc
            # Remove www. prefix if present
            if domain.startswith("www."):
                domain = domain[4:]
            return domain
        except:
            return ""
    
    def _deduplicate_news(self, news_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove duplicate news articles based on URL"""
        unique_urls = set()
        unique_news = []
        
        for news in news_list:
            url = news.get("url", "")
            if url and url not in unique_urls:
                unique_urls.add(url)
                unique_news.append(news)
        
        return unique_news

# Database access functions (preserving existing functionality)
def get_news_by_ticker(
    db: Session, 
    ticker: str, 
    bias_list: Optional[List[str]] = None, 
    sentiment_list: Optional[List[str]] = None,
    limit: int = 20,
    offset: int = 0
) -> List[ArticleResponse]:
    """
    Get news articles for a specific ticker with optional filtering.
    
    Args:
        db: Database session
        ticker: Stock ticker symbol
        bias_list: Optional list of bias categories to filter by
        sentiment_list: Optional list of sentiment values to filter by
        limit: Maximum number of articles to return
        offset: Offset for pagination
        
    Returns:
        List of article response objects
    """
    query = db.query(Article).filter(Article.ticker == ticker)
    
    # Apply bias filter if provided
    if bias_list:
        query = query.filter(Article.bias_label.in_(bias_list))
        
    # Apply sentiment filter if provided
    if sentiment_list:
        query = query.filter(Article.sentiment_label.in_(sentiment_list))
        
    # Order by published date (newest first)
    query = query.order_by(Article.published_date.desc())
    
    # Apply pagination
    articles = query.offset(offset).limit(limit).all()
    
    # Convert to response model
    return [ArticleResponse.from_orm(article) for article in articles]

def get_bias_distribution(
    db: Session,
    ticker: str,
    days: int = 7
) -> BiasDistribution:
    """
    Get bias distribution statistics for a specific ticker.
    
    Args:
        db: Database session
        ticker: Stock ticker symbol
        days: Number of days to include
        
    Returns:
        BiasDistribution object with statistics
    """
    # Calculate date threshold
    date_threshold = datetime.now() - timedelta(days=days)
    
    # Get articles within date range
    articles = db.query(Article).filter(
        Article.ticker == ticker,
        Article.published_date >= date_threshold
    ).all()
    
    # Count total articles
    total_articles = len(articles)
    
    if total_articles == 0:
        return BiasDistribution(
            ticker=ticker,
            total_articles=0,
            days=days,
            is_biased=False
        )
    
    # Count articles by bias category
    left_count = sum(1 for a in articles if a.bias_label == "left")
    lean_left_count = sum(1 for a in articles if a.bias_label == "lean_left")
    center_count = sum(1 for a in articles if a.bias_label == "center")
    lean_right_count = sum(1 for a in articles if a.bias_label == "lean_right")
    right_count = sum(1 for a in articles if a.bias_label == "right")
    unknown_count = sum(1 for a in articles if a.bias_label == "unknown")
    
    # Calculate percentages
    left_percentage = (left_count / total_articles) * 100 if total_articles > 0 else 0
    lean_left_percentage = (lean_left_count / total_articles) * 100 if total_articles > 0 else 0
    center_percentage = (center_count / total_articles) * 100 if total_articles > 0 else 0
    lean_right_percentage = (lean_right_count / total_articles) * 100 if total_articles > 0 else 0
    right_percentage = (right_count / total_articles) * 100 if total_articles > 0 else 0
    unknown_percentage = (unknown_count / total_articles) * 100 if total_articles > 0 else 0
    
    # Determine if coverage is biased (one category > 60%)
    is_biased = False
    dominant_bias = None
    
    for bias, percentage in [
        ("left", left_percentage),
        ("lean_left", lean_left_percentage),
        ("center", center_percentage),
        ("lean_right", lean_right_percentage),
        ("right", right_percentage)
    ]:
        if percentage > 60:
            is_biased = True
            dominant_bias = bias
            break
    
    return BiasDistribution(
        ticker=ticker,
        total_articles=total_articles,
        left_count=left_count,
        lean_left_count=lean_left_count,
        center_count=center_count,
        lean_right_count=lean_right_count,
        right_count=right_count,
        unknown_count=unknown_count,
        left_percentage=left_percentage,
        lean_left_percentage=lean_left_percentage,
        center_percentage=center_percentage,
        lean_right_percentage=lean_right_percentage,
        right_percentage=right_percentage,
        unknown_percentage=unknown_percentage,
        days=days,
        is_biased=is_biased,
        dominant_bias=dominant_bias
    )

# Create singleton instance
news_service = NewsService()
