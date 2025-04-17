from transformers import pipeline
import logging
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session

from app.models.models import Article, Source
from app.models.schemas import BiasCategory, SentimentCategory
from app.core.config import settings

logger = logging.getLogger(__name__)

class SentimentAnalyzer:
    """Analyze sentiment of news articles."""
    
    def __init__(self):
        # Initialize sentiment analysis pipeline
        try:
            self.sentiment_pipeline = pipeline(
                "sentiment-analysis",
                model=settings.SENTIMENT_MODEL_NAME,
                tokenizer=settings.SENTIMENT_MODEL_NAME
            )
            logger.info(f"Sentiment analysis model {settings.SENTIMENT_MODEL_NAME} loaded successfully")
        except Exception as e:
            logger.error(f"Error loading sentiment model: {str(e)}")
            self.sentiment_pipeline = None
    
    def analyze_sentiment(self, text: str) -> SentimentCategory:
        """
        Analyze sentiment of text and return sentiment category.
        
        Args:
            text: Text to analyze
            
        Returns:
            SentimentCategory enum value
        """
        if not self.sentiment_pipeline:
            logger.warning("Sentiment pipeline not available, returning NEUTRAL")
            return SentimentCategory.NEUTRAL
            
        try:
            # Truncate text if too long
            max_length = 512
            if len(text) > max_length:
                text = text[:max_length]
                
            # Get sentiment prediction
            result = self.sentiment_pipeline(text)[0]
            label = result['label']
            score = result['score']
            
            # Map FinBERT labels to our sentiment categories
            # FinBERT typically uses 'positive', 'negative', 'neutral'
            if label.lower() == 'positive':
                return SentimentCategory.BULLISH
            elif label.lower() == 'negative':
                return SentimentCategory.BEARISH
            else:
                return SentimentCategory.NEUTRAL
                
        except Exception as e:
            logger.error(f"Error analyzing sentiment: {str(e)}")
            return SentimentCategory.NEUTRAL
    
    def analyze_article(self, article: Article) -> SentimentCategory:
        """
        Analyze sentiment of an article.
        
        Args:
            article: Article object to analyze
            
        Returns:
            SentimentCategory enum value
        """
        # Combine headline and summary for better context
        text = f"{article.headline} {article.summary}"
        return self.analyze_sentiment(text)
    
    def batch_analyze_articles(self, db: Session, limit: int = 100) -> int:
        """
        Analyze sentiment for articles that don't have sentiment yet.
        
        Args:
            db: Database session
            limit: Maximum number of articles to analyze
            
        Returns:
            Number of articles analyzed
        """
        # Get articles without sentiment analysis
        articles = db.query(Article).filter(
            Article.sentiment_label == SentimentCategory.NEUTRAL
        ).limit(limit).all()
        
        count = 0
        for article in articles:
            try:
                # Analyze sentiment
                sentiment = self.analyze_article(article)
                
                # Update article
                article.sentiment_label = sentiment
                count += 1
                
            except Exception as e:
                logger.error(f"Error analyzing article {article.id}: {str(e)}")
        
        # Commit changes
        db.commit()
        
        return count
