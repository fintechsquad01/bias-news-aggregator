from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta

from app.models.models import Article
from app.models.schemas import BiasDistribution, ArticleResponse

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
