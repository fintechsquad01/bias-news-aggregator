import logging
import asyncio
from typing import List, Dict, Any, Optional
from datetime import datetime
from sqlalchemy.orm import Session

from app.services.polygon_service import PolygonNewsService
from app.services.financial_datasets_service import FinancialDatasetsService
from app.services.whalewisdom_service import WhaleWisdomService
from app.services.finnhub_service import FinnhubService
from app.models.models import Article
from app.models.schemas import ArticleCreate, BiasCategory, SentimentCategory
from app.core.config import settings

logger = logging.getLogger(__name__)

class NewsProcessor:
    """Process news from various sources and standardize format."""
    
    def __init__(self, db: Session):
        self.db = db
        self.polygon_service = PolygonNewsService()
        self.financial_datasets_service = FinancialDatasetsService()
        self.whalewisdom_service = WhaleWisdomService()
        self.finnhub_service = FinnhubService()
        
    async def fetch_and_process_news(self, ticker: str, limit_per_source: int = 10) -> List[Article]:
        """
        Fetch news from all sources and process them into a standardized format.
        
        Args:
            ticker: Stock ticker symbol
            limit_per_source: Maximum number of news items to fetch per source
            
        Returns:
            List of processed articles
        """
        # Fetch news from all sources concurrently
        polygon_task = self.polygon_service.get_ticker_news(ticker, limit_per_source)
        financial_datasets_task = self.financial_datasets_service.get_ticker_news(ticker, limit_per_source)
        finnhub_task = self.finnhub_service.get_company_news(ticker, limit_per_source)
        
        # Await all tasks
        polygon_news, financial_datasets_news, finnhub_news = await asyncio.gather(
            polygon_task, financial_datasets_task, finnhub_task
        )
        
        # Process news from each source
        processed_articles = []
        
        # Process Polygon news
        for article in polygon_news:
            processed_article = self._process_polygon_article(article, ticker)
            if processed_article:
                processed_articles.append(processed_article)
                
        # Process Financial Datasets news
        for article in financial_datasets_news:
            processed_article = self._process_financial_datasets_article(article, ticker)
            if processed_article:
                processed_articles.append(processed_article)
                
        # Process Finnhub news
        for article in finnhub_news:
            processed_article = self._process_finnhub_article(article, ticker)
            if processed_article:
                processed_articles.append(processed_article)
                
        # Save articles to database
        saved_articles = []
        for article_data in processed_articles:
            # Check if article already exists by URL
            existing_article = self.db.query(Article).filter(Article.url == article_data.url).first()
            if not existing_article:
                article = Article(
                    ticker=article_data.ticker,
                    headline=article_data.headline,
                    summary=article_data.summary,
                    url=article_data.url,
                    source=article_data.source,
                    bias_label=article_data.bias_label,
                    sentiment_label=article_data.sentiment_label,
                    published_date=article_data.published_date
                )
                self.db.add(article)
                saved_articles.append(article)
                
        self.db.commit()
        
        return saved_articles
    
    def _process_polygon_article(self, article: Dict[str, Any], ticker: str) -> Optional[ArticleCreate]:
        """Process an article from Polygon.io into standardized format."""
        try:
            # Extract source domain from publisher.homepage
            source = article.get("publisher", {}).get("name", "Unknown")
            source_domain = article.get("publisher", {}).get("homepage", "").replace("https://", "").replace("http://", "").split("/")[0]
            
            # Get published date
            published_str = article.get("published_utc")
            if not published_str:
                return None
                
            published_date = datetime.fromisoformat(published_str.replace("Z", "+00:00"))
            
            # Create standardized article
            return ArticleCreate(
                ticker=ticker,
                headline=article.get("title", ""),
                summary=article.get("description", ""),
                url=article.get("article_url", ""),
                source=source,
                bias_label=self._get_bias_for_source(source_domain),
                sentiment_label=SentimentCategory.NEUTRAL,  # Will be updated by sentiment analysis module
                published_date=published_date
            )
        except Exception as e:
            logger.error(f"Error processing Polygon article: {str(e)}")
            return None
    
    def _process_financial_datasets_article(self, article: Dict[str, Any], ticker: str) -> Optional[ArticleCreate]:
        """Process an article from Financial Datasets into standardized format."""
        try:
            # Extract source domain
            source = article.get("source", "Unknown")
            source_domain = article.get("source_url", "").replace("https://", "").replace("http://", "").split("/")[0]
            
            # Get published date
            published_str = article.get("published_at")
            if not published_str:
                return None
                
            published_date = datetime.fromisoformat(published_str.replace("Z", "+00:00"))
            
            # Create standardized article
            return ArticleCreate(
                ticker=ticker,
                headline=article.get("title", ""),
                summary=article.get("summary", ""),
                url=article.get("url", ""),
                source=source,
                bias_label=self._get_bias_for_source(source_domain),
                sentiment_label=SentimentCategory.NEUTRAL,  # Will be updated by sentiment analysis module
                published_date=published_date
            )
        except Exception as e:
            logger.error(f"Error processing Financial Datasets article: {str(e)}")
            return None
    
    def _process_finnhub_article(self, article: Dict[str, Any], ticker: str) -> Optional[ArticleCreate]:
        """Process an article from Finnhub into standardized format."""
        try:
            # Extract source domain
            source = article.get("source", "Unknown")
            source_domain = source.lower()
            
            # Get published date
            published_timestamp = article.get("datetime")
            if not published_timestamp:
                return None
                
            published_date = datetime.fromtimestamp(published_timestamp)
            
            # Create standardized article
            return ArticleCreate(
                ticker=ticker,
                headline=article.get("headline", ""),
                summary=article.get("summary", ""),
                url=article.get("url", ""),
                source=source,
                bias_label=self._get_bias_for_source(source_domain),
                sentiment_label=SentimentCategory.NEUTRAL,  # Will be updated by sentiment analysis module
                published_date=published_date
            )
        except Exception as e:
            logger.error(f"Error processing Finnhub article: {str(e)}")
            return None
    
    def _get_bias_for_source(self, domain: str) -> BiasCategory:
        """
        Get bias category for a news source domain.
        This is a placeholder - in the real implementation, this would query the database.
        """
        # Query the database for the source
        source = self.db.query(Article).filter_by(domain=domain).first()
        
        if source:
            return source.bias_rating
        
        # Default to unknown if source not found
        return BiasCategory.UNKNOWN
