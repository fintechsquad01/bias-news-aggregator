import logging
from fastapi import BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional

from app.services.bias_analysis_service import BiasAnalysisService
from app.services.sentiment_analysis_service import SentimentAnalysisService
from app.models.schemas import BiasDistribution

logger = logging.getLogger(__name__)

class AnalysisManager:
    """Manager for coordinating bias and sentiment analysis."""
    
    def __init__(self, db: Session):
        self.db = db
        self.bias_service = BiasAnalysisService(db)
        self.sentiment_service = SentimentAnalysisService(db)
    
    def analyze_ticker(self, ticker: str, days: int = 7) -> Dict[str, Any]:
        """
        Perform comprehensive analysis for a ticker.
        
        Args:
            ticker: Stock ticker symbol
            days: Number of days to include
            
        Returns:
            Dictionary with analysis results
        """
        # Get bias distribution
        bias_distribution = self.bias_service.calculate_bias_distribution(ticker, days)
        
        # Get sentiment distribution
        sentiment_distribution = self.sentiment_service.get_sentiment_distribution(ticker, days)
        
        # Get viewpoint diversity warning
        diversity_warning = self.bias_service.get_viewpoint_diversity_warning(ticker, days)
        
        # Get sentiment summary
        sentiment_summary = self.sentiment_service.get_sentiment_summary(ticker, days)
        
        return {
            "ticker": ticker,
            "days": days,
            "bias_distribution": bias_distribution,
            "sentiment_distribution": sentiment_distribution,
            "diversity_warning": diversity_warning,
            "sentiment_summary": sentiment_summary
        }
    
    def run_batch_analysis(self, background_tasks: BackgroundTasks):
        """
        Run batch analysis for bias and sentiment in the background.
        
        Args:
            background_tasks: FastAPI BackgroundTasks object
        """
        background_tasks.add_task(self._perform_batch_analysis)
    
    def _perform_batch_analysis(self):
        """Perform batch analysis for bias and sentiment."""
        try:
            # Update bias labels
            bias_count = self.bias_service.update_article_bias_labels(limit=200)
            logger.info(f"Updated bias labels for {bias_count} articles")
            
            # Update sentiment labels
            sentiment_count = self.sentiment_service.batch_analyze_articles(limit=200)
            logger.info(f"Updated sentiment labels for {sentiment_count} articles")
            
        except Exception as e:
            logger.error(f"Error in batch analysis: {str(e)}")
    
    def get_portfolio_analysis(self, tickers: List[str], days: int = 7) -> Dict[str, Any]:
        """
        Perform analysis for a portfolio of tickers.
        
        Args:
            tickers: List of stock ticker symbols
            days: Number of days to include
            
        Returns:
            Dictionary with analysis results
        """
        results = {}
        
        # Analyze each ticker
        for ticker in tickers:
            results[ticker] = self.analyze_ticker(ticker, days)
        
        # Calculate aggregate statistics
        aggregate = self._calculate_portfolio_aggregate(results)
        
        return {
            "tickers": tickers,
            "days": days,
            "ticker_results": results,
            "aggregate": aggregate
        }
    
    def _calculate_portfolio_aggregate(self, ticker_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate aggregate statistics for a portfolio.
        
        Args:
            ticker_results: Dictionary of analysis results by ticker
            
        Returns:
            Dictionary with aggregate statistics
        """
        # Initialize counters
        total_articles = 0
        left_count = 0
        lean_left_count = 0
        center_count = 0
        lean_right_count = 0
        right_count = 0
        unknown_count = 0
        
        bullish_count = 0
        bearish_count = 0
        neutral_count = 0
        
        biased_tickers = []
        
        # Aggregate counts
        for ticker, result in ticker_results.items():
            bias_dist = result["bias_distribution"]
            sent_dist = result["sentiment_distribution"]
            
            total_articles += bias_dist.total_articles
            left_count += bias_dist.left_count
            lean_left_count += bias_dist.lean_left_count
            center_count += bias_dist.center_count
            lean_right_count += bias_dist.lean_right_count
            right_count += bias_dist.right_count
            unknown_count += bias_dist.unknown_count
            
            bullish_count += sent_dist["bullish_count"]
            bearish_count += sent_dist["bearish_count"]
            neutral_count += sent_dist["neutral_count"]
            
            if bias_dist.is_biased:
                biased_tickers.append(ticker)
        
        # Calculate percentages
        if total_articles > 0:
            left_percentage = (left_count / total_articles) * 100
            lean_left_percentage = (lean_left_count / total_articles) * 100
            center_percentage = (center_count / total_articles) * 100
            lean_right_percentage = (lean_right_count / total_articles) * 100
            right_percentage = (right_count / total_articles) * 100
            unknown_percentage = (unknown_count / total_articles) * 100
            
            bullish_percentage = (bullish_count / total_articles) * 100
            bearish_percentage = (bearish_count / total_articles) * 100
            neutral_percentage = (neutral_count / total_articles) * 100
        else:
            left_percentage = 0
            lean_left_percentage = 0
            center_percentage = 0
            lean_right_percentage = 0
            right_percentage = 0
            unknown_percentage = 0
            
            bullish_percentage = 0
            bearish_percentage = 0
            neutral_percentage = 0
        
        return {
            "total_articles": total_articles,
            "bias_distribution": {
                "left_count": left_count,
                "lean_left_count": lean_left_count,
                "center_count": center_count,
                "lean_right_count": lean_right_count,
                "right_count": right_count,
                "unknown_count": unknown_count,
                "left_percentage": left_percentage,
                "lean_left_percentage": lean_left_percentage,
                "center_percentage": center_percentage,
                "lean_right_percentage": lean_right_percentage,
                "right_percentage": right_percentage,
                "unknown_percentage": unknown_percentage
            },
            "sentiment_distribution": {
                "bullish_count": bullish_count,
                "bearish_count": bearish_count,
                "neutral_count": neutral_count,
                "bullish_percentage": bullish_percentage,
                "bearish_percentage": bearish_percentage,
                "neutral_percentage": neutral_percentage
            },
            "biased_tickers": biased_tickers,
            "has_biased_coverage": len(biased_tickers) > 0
        }
