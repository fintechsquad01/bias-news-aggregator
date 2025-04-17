from fastapi import APIRouter, Depends, Query, HTTPException, BackgroundTasks
from typing import List, Optional
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.schemas import ArticleResponse, BiasDistribution
from app.services.news_service import get_news_by_ticker
from app.services.analysis_manager import AnalysisManager

router = APIRouter()

@router.get("/ticker/{ticker}", response_model=List[ArticleResponse])
def get_ticker_news(
    ticker: str,
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

@router.get("/ticker/{ticker}/analysis")
def get_ticker_analysis(
    ticker: str,
    days: int = Query(7, description="Number of days to include in analysis"),
    db: Session = Depends(get_db)
):
    """
    Get comprehensive analysis for a ticker including bias and sentiment.
    """
    analysis_manager = AnalysisManager(db)
    return analysis_manager.analyze_ticker(ticker, days)

@router.get("/ticker/{ticker}/bias", response_model=BiasDistribution)
def get_ticker_bias_distribution(
    ticker: str,
    days: int = Query(7, description="Number of days to include"),
    db: Session = Depends(get_db)
):
    """
    Get bias distribution statistics for a specific ticker.
    """
    analysis_manager = AnalysisManager(db)
    return analysis_manager.bias_service.calculate_bias_distribution(ticker, days)

@router.get("/ticker/{ticker}/sentiment")
def get_ticker_sentiment(
    ticker: str,
    days: int = Query(7, description="Number of days to include"),
    db: Session = Depends(get_db)
):
    """
    Get sentiment distribution statistics for a specific ticker.
    """
    analysis_manager = AnalysisManager(db)
    return analysis_manager.sentiment_service.get_sentiment_distribution(ticker, days)

@router.get("/portfolio")
def get_portfolio_analysis(
    tickers: str = Query(..., description="Comma-separated list of ticker symbols"),
    days: int = Query(7, description="Number of days to include"),
    db: Session = Depends(get_db)
):
    """
    Get comprehensive analysis for a portfolio of tickers.
    """
    ticker_list = tickers.split(",")
    analysis_manager = AnalysisManager(db)
    return analysis_manager.get_portfolio_analysis(ticker_list, days)

@router.post("/analyze")
def run_analysis(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Trigger background analysis of news articles.
    """
    analysis_manager = AnalysisManager(db)
    analysis_manager.run_batch_analysis(background_tasks)
    return {"message": "Analysis started in background"}
