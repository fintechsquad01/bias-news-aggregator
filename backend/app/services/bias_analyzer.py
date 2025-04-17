import logging
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session

from app.models.models import Source
from app.models.schemas import BiasCategory

logger = logging.getLogger(__name__)

class BiasAnalyzer:
    """Analyze and determine bias for news sources."""
    
    def __init__(self, db: Session):
        self.db = db
        
    def get_bias_for_source(self, source_domain: str) -> BiasCategory:
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
        
    def get_bias_distribution(self, articles: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculate bias distribution statistics for a list of articles.
        
        Args:
            articles: List of article dictionaries
            
        Returns:
            Dictionary with bias distribution statistics
        """
        total = len(articles)
        if total == 0:
            return {
                "total_articles": 0,
                "left_count": 0,
                "lean_left_count": 0,
                "center_count": 0,
                "lean_right_count": 0,
                "right_count": 0,
                "unknown_count": 0,
                "left_percentage": 0,
                "lean_left_percentage": 0,
                "center_percentage": 0,
                "lean_right_percentage": 0,
                "right_percentage": 0,
                "unknown_percentage": 0,
                "is_biased": False,
                "dominant_bias": None
            }
            
        # Count articles by bias category
        counts = {
            "left": 0,
            "lean_left": 0,
            "center": 0,
            "lean_right": 0,
            "right": 0,
            "unknown": 0
        }
        
        for article in articles:
            bias = article.get("bias_label", BiasCategory.UNKNOWN)
            counts[bias] += 1
            
        # Calculate percentages
        percentages = {
            "left": (counts["left"] / total) * 100,
            "lean_left": (counts["lean_left"] / total) * 100,
            "center": (counts["center"] / total) * 100,
            "lean_right": (counts["lean_right"] / total) * 100,
            "right": (counts["right"] / total) * 100,
            "unknown": (counts["unknown"] / total) * 100
        }
        
        # Determine if coverage is biased (one category > 60%)
        is_biased = False
        dominant_bias = None
        
        for bias, percentage in percentages.items():
            if percentage > 60 and bias != "unknown":
                is_biased = True
                dominant_bias = bias
                break
                
        return {
            "total_articles": total,
            "left_count": counts["left"],
            "lean_left_count": counts["lean_left"],
            "center_count": counts["center"],
            "lean_right_count": counts["lean_right"],
            "right_count": counts["right"],
            "unknown_count": counts["unknown"],
            "left_percentage": percentages["left"],
            "lean_left_percentage": percentages["lean_left"],
            "center_percentage": percentages["center"],
            "lean_right_percentage": percentages["lean_right"],
            "right_percentage": percentages["right"],
            "unknown_percentage": percentages["unknown"],
            "is_biased": is_biased,
            "dominant_bias": dominant_bias
        }
