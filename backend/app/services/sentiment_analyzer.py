import os
from typing import Dict, Any, List, Optional
import requests
from transformers import pipeline
import numpy as np
import logging
from sqlalchemy.orm import Session

from app.models.models import Article, Source
from app.models.schemas import BiasCategory, SentimentCategory
from app.core.config import settings

logger = logging.getLogger(__name__)

class SentimentAnalyzer:
    """Service for analyzing sentiment in financial news articles"""
    
    def __init__(self):
        # Initialize sentiment analysis pipeline
        try:
            # Use FinBERT model specifically trained for financial sentiment
            self.sentiment_pipeline = pipeline(
                "sentiment-analysis",
                model="ProsusAI/finbert",
                tokenizer="ProsusAI/finbert"
            )
        except Exception as e:
            print(f"Error initializing sentiment pipeline: {e}")
            self.sentiment_pipeline = None
    
    def analyze_text(self, text: str, ticker: str = None) -> Dict[str, Any]:
        """
        Analyze the sentiment of a text
        
        Args:
            text: The text to analyze (headline or summary)
            ticker: Optional ticker symbol for context
            
        Returns:
            Dictionary with sentiment_label, sentiment_score, and confidence_score
        """
        if not self.sentiment_pipeline:
            # Default to neutral if pipeline not available
            return {
                "sentiment_label": "neutral",
                "sentiment_score": 0.0,
                "confidence_score": 0.0
            }
        
        try:
            # Add ticker context if provided
            if ticker:
                analysis_text = f"{ticker}: {text}"
            else:
                analysis_text = text
            
            # Truncate text if too long (model has token limits)
            if len(analysis_text) > 512:
                analysis_text = analysis_text[:512]
            
            # Run sentiment analysis
            result = self.sentiment_pipeline(analysis_text)[0]
            
            # Map FinBERT labels to our labels
            label_mapping = {
                "positive": "bullish",
                "negative": "bearish",
                "neutral": "neutral"
            }
            
            # Map score to -1 to 1 range
            # FinBERT gives confidence scores, we need to convert to a directional score
            raw_label = result["label"]
            confidence = result["score"]  # Between 0 and 1
            
            if raw_label == "positive":
                score = confidence
            elif raw_label == "negative":
                score = -confidence
            else:
                score = 0.0
            
            return {
                "sentiment_label": label_mapping.get(raw_label, "neutral"),
                "sentiment_score": score,
                "confidence_score": confidence
            }
        except Exception as e:
            print(f"Error analyzing sentiment: {e}")
            # Default to neutral on error
            return {
                "sentiment_label": "neutral",
                "sentiment_score": 0.0,
                "confidence_score": 0.0
            }
    
    def analyze_article(self, article: Dict[str, Any], ticker: str) -> Dict[str, Any]:
        """
        Analyze the sentiment of a news article
        
        Args:
            article: Dictionary with article data (headline, summary)
            ticker: Ticker symbol the article is about
            
        Returns:
            Dictionary with sentiment analysis results
        """
        # Combine headline and summary for analysis
        headline = article.get("headline", "")
        summary = article.get("summary", "")
        
        # Prioritize headline but use summary if headline is too short
        if len(headline) > 20:
            analysis_text = headline
        elif summary:
            analysis_text = summary
        else:
            analysis_text = headline
        
        return self.analyze_text(analysis_text, ticker)
    
    def batch_analyze(self, articles: List[Dict[str, Any]], ticker: str) -> List[Dict[str, Any]]:
        """
        Analyze sentiment for a batch of articles
        
        Args:
            articles: List of article dictionaries
            ticker: Ticker symbol the articles are about
            
        Returns:
            List of articles with sentiment analysis added
        """
        results = []
        
        for article in articles:
            sentiment = self.analyze_article(article, ticker)
            article["sentiment"] = sentiment
            results.append(article)
        
        return results

# Create singleton instance
sentiment_analyzer = SentimentAnalyzer()
