from fastapi import APIRouter, Depends, Query, HTTPException, Path
from typing import List, Optional
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.schemas import ArticleResponse
from app.services.news_service import get_news_by_ticker

router = APIRouter()

@router.get("", response_model=List[ArticleResponse])
def get_news(
    ticker: str = Query(..., description="Stock ticker symbol"),
    bias: Optional[str] = Query(None, description="Comma-separated bias categories (left,lean_left,center,lean_right,right)"),
    sentiment: Optional[str] = Query(None, description="Comma-separated sentiment values (bullish,bearish,neutral)"),
    limit: int = Query(20, description="Number of articles to return"),
    offset: int = Query(0, description="Offset for pagination"),
    db: Session = Depends(get_db)
):
    """
    Get news articles for a specific ticker with optional filtering by bias and sentiment.
    """
    bias_list = bias.split(",") if bias else None
    sentiment_list = sentiment.split(",") if sentiment else None
    
    return get_news_by_ticker(db, ticker, bias_list, sentiment_list, limit, offset)

@router.get("/portfolio")
def get_portfolio_news(
    tickers: str = Query(..., description="Comma-separated list of ticker symbols"),
    limit: int = Query(10, description="Number of articles to return per ticker"),
    db: Session = Depends(get_db)
):
    """
    Get news for multiple tickers (portfolio view).
    """
    ticker_list = tickers.split(",")
    result = {}
    
    for ticker in ticker_list:
        result[ticker] = get_news_by_ticker(db, ticker, None, None, limit, 0)
    
    return result

@router.get("/trending")
def get_trending_news(
    limit: int = Query(10, description="Number of trending articles to return"),
    db: Session = Depends(get_db)
):
    """
    Get trending news articles across all tickers.
    """
    # In a real implementation, this would use a more sophisticated algorithm
    # to determine trending articles based on recency, popularity, etc.
    # For now, we'll just return the most recent articles
    
    # This is a placeholder implementation
    default_tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]
    result = []
    
    for ticker in default_tickers:
        articles = get_news_by_ticker(db, ticker, None, None, 2, 0)
        result.extend(articles)
    
    # Sort by published date (newest first) and limit
    result.sort(key=lambda x: x.published_date, reverse=True)
    return result[:limit]

@router.get("/sources")
def get_news_sources(
    db: Session = Depends(get_db)
):
    """
    Get list of news sources with their bias ratings.
    """
    # This would query the database for all sources
    # For now, we'll return a placeholder
    return {
        "message": "This endpoint will return a list of news sources with their bias ratings."
    }
