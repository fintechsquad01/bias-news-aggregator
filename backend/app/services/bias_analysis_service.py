import logging
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.models.models import Article, Source
from app.models.schemas import BiasCategory, BiasDistribution

logger = logging.getLogger(__name__)

class BiasAnalysisService:
    """Service for analyzing bias in news articles."""
    
    def __init__(self, db: Session):
        self.db = db
        
    def get_source_bias(self, source_domain: str) -> BiasCategory:
        """
        Get bias category for a news source domain.
        
        Args:
            source_domain: Domain of the news source
            
        Returns:
            BiasCategory enum value
        """
        # Clean up the domain
        domain = source_domain.lower().strip()
        if domain.startswith('www.'):
            domain = domain[4:]
            
        # Query the database for the source
        source = self.db.query(Source).filter(Source.domain == domain).first()
        
        if source:
            return source.bias_rating
            
        # Try partial match if exact match not found
        for source in self.db.query(Source).all():
            if source.domain in domain or domain in source.domain:
                logger.info(f"Partial domain match for {domain}: {source.domain} with bias {source.bias_rating}")
                return source.bias_rating
        
        # Default to unknown if source not found
        logger.warning(f"No bias rating found for domain: {domain}")
        return BiasCategory.UNKNOWN
        
    def calculate_bias_distribution(self, ticker: str, days: int = 7) -> BiasDistribution:
        """
        Calculate bias distribution statistics for a specific ticker.
        
        Args:
            ticker: Stock ticker symbol
            days: Number of days to include
            
        Returns:
            BiasDistribution object with statistics
        """
        # Calculate date threshold
        date_threshold = datetime.now() - timedelta(days=days)
        
        # Get articles within date range
        articles = self.db.query(Article).filter(
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
        left_count = sum(1 for a in articles if a.bias_label == BiasCategory.LEFT)
        lean_left_count = sum(1 for a in articles if a.bias_label == BiasCategory.LEAN_LEFT)
        center_count = sum(1 for a in articles if a.bias_label == BiasCategory.CENTER)
        lean_right_count = sum(1 for a in articles if a.bias_label == BiasCategory.LEAN_RIGHT)
        right_count = sum(1 for a in articles if a.bias_label == BiasCategory.RIGHT)
        unknown_count = sum(1 for a in articles if a.bias_label == BiasCategory.UNKNOWN)
        
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
            (BiasCategory.LEFT, left_percentage),
            (BiasCategory.LEAN_LEFT, lean_left_percentage),
            (BiasCategory.CENTER, center_percentage),
            (BiasCategory.LEAN_RIGHT, lean_right_percentage),
            (BiasCategory.RIGHT, right_percentage)
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
    
    def get_viewpoint_diversity_warning(self, ticker: str, days: int = 7) -> Optional[str]:
        """
        Check if news coverage for a ticker lacks viewpoint diversity.
        
        Args:
            ticker: Stock ticker symbol
            days: Number of days to include
            
        Returns:
            Warning message if coverage is biased, None otherwise
        """
        distribution = self.calculate_bias_distribution(ticker, days)
        
        if distribution.is_biased and distribution.dominant_bias:
            return f"Warning: News coverage for {ticker} is predominantly from {distribution.dominant_bias} sources ({round(getattr(distribution, f'{distribution.dominant_bias}_percentage'), 1)}%)."
        
        return None
    
    def update_article_bias_labels(self, limit: int = 100) -> int:
        """
        Update bias labels for articles based on their source.
        
        Args:
            limit: Maximum number of articles to update
            
        Returns:
            Number of articles updated
        """
        # Get articles with unknown bias
        articles = self.db.query(Article).filter(
            Article.bias_label == BiasCategory.UNKNOWN
        ).limit(limit).all()
        
        count = 0
        for article in articles:
            try:
                # Extract domain from source
                source_parts = article.source.split('.')
                if len(source_parts) >= 2:
                    domain = f"{source_parts[-2]}.{source_parts[-1]}"
                else:
                    domain = article.source
                
                # Get bias for source
                bias = self.get_source_bias(domain)
                
                # Update article
                article.bias_label = bias
                count += 1
                
            except Exception as e:
                logger.error(f"Error updating bias for article {article.id}: {str(e)}")
        
        # Commit changes
        self.db.commit()
        
        return count
