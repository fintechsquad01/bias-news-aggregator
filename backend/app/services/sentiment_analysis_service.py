import logging
from typing import List, Dict, Any, Optional, Tuple
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import torch.nn.functional as F

from app.models.models import Article
from app.models.schemas import SentimentCategory
from app.services.sentiment_analyzer import SentimentAnalyzer

logger = logging.getLogger(__name__)

class SentimentAnalysisService:
    """Service for analyzing sentiment in news articles using FinBERT."""
    
    def __init__(self, db: Session):
        self.db = db
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = None
        self.model = None
        self._load_model()
        
    def _load_model(self) -> None:
        """Load the FinBERT model and tokenizer."""
        try:
            model_name = "ProsusAI/finbert"
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
            self.model.to(self.device)
            logger.info("FinBERT model loaded successfully")
        except Exception as e:
            logger.error(f"Error loading FinBERT model: {str(e)}")
            raise
            
    def _map_finbert_to_sentiment(self, label: str, confidence: float) -> Tuple[SentimentCategory, float]:
        """
        Map FinBERT labels to application sentiment categories.
        
        Args:
            label: FinBERT label ('positive', 'negative', 'neutral')
            confidence: Model confidence score
            
        Returns:
            Tuple of (SentimentCategory, confidence)
        """
        mapping = {
            'positive': SentimentCategory.BULLISH,
            'negative': SentimentCategory.BEARISH,
            'neutral': SentimentCategory.NEUTRAL
        }
        return mapping.get(label, SentimentCategory.NEUTRAL), confidence
        
    def analyze_text(self, text: str) -> Tuple[SentimentCategory, float]:
        """
        Analyze sentiment of a given text using FinBERT.
        
        Args:
            text: Text to analyze
            
        Returns:
            Tuple of (SentimentCategory, confidence_score)
            
        Raises:
            RuntimeError: If model is not loaded or prediction fails
        """
        if not self.model or not self.tokenizer:
            raise RuntimeError("FinBERT model not loaded")
            
        try:
            # Tokenize and prepare input
            inputs = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            # Get model predictions
            with torch.no_grad():
                outputs = self.model(**inputs)
                probabilities = F.softmax(outputs.logits, dim=-1)
                confidence, predicted_class = torch.max(probabilities, dim=-1)
                
            # Get label and confidence
            label = self.model.config.id2label[predicted_class.item()]
            confidence_score = confidence.item()
            
            # Map to application sentiment categories
            return self._map_finbert_to_sentiment(label, confidence_score)
            
        except Exception as e:
            logger.error(f"Error analyzing text: {str(e)}")
            raise RuntimeError(f"Failed to analyze text: {str(e)}")
            
    def analyze_article_sentiment(self, article_id: int) -> SentimentCategory:
        """
        Analyze sentiment for a specific article.
        
        Args:
            article_id: ID of the article to analyze
            
        Returns:
            SentimentCategory enum value
        """
        # Get article from database
        article = self.db.query(Article).filter(Article.id == article_id).first()
        
        if not article:
            logger.warning(f"Article with ID {article_id} not found")
            return SentimentCategory.NEUTRAL
            
        try:
            # Analyze sentiment
            sentiment, confidence = self.analyze_text(article.content)
            
            # Update article
            article.sentiment_label = sentiment
            article.sentiment_confidence = confidence
            self.db.commit()
            
            return sentiment
            
        except Exception as e:
            logger.error(f"Error analyzing article {article_id}: {str(e)}")
            return SentimentCategory.NEUTRAL
    
    def batch_analyze_articles(self, limit: int = 100) -> int:
        """
        Analyze sentiment for articles that don't have sentiment yet.
        
        Args:
            limit: Maximum number of articles to analyze
            
        Returns:
            Number of articles analyzed
        """
        return self.analyzer.batch_analyze_articles(self.db, limit)
    
    def get_sentiment_distribution(self, ticker: str, days: int = 7) -> Dict[str, Any]:
        """
        Calculate sentiment distribution statistics for a specific ticker.
        
        Args:
            ticker: Stock ticker symbol
            days: Number of days to include
            
        Returns:
            Dictionary with sentiment distribution statistics
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
            return {
                "ticker": ticker,
                "total_articles": 0,
                "bullish_count": 0,
                "bearish_count": 0,
                "neutral_count": 0,
                "bullish_percentage": 0,
                "bearish_percentage": 0,
                "neutral_percentage": 0,
                "days": days,
                "overall_sentiment": SentimentCategory.NEUTRAL
            }
        
        # Count articles by sentiment category
        bullish_count = sum(1 for a in articles if a.sentiment_label == SentimentCategory.BULLISH)
        bearish_count = sum(1 for a in articles if a.sentiment_label == SentimentCategory.BEARISH)
        neutral_count = sum(1 for a in articles if a.sentiment_label == SentimentCategory.NEUTRAL)
        
        # Calculate percentages
        bullish_percentage = (bullish_count / total_articles) * 100 if total_articles > 0 else 0
        bearish_percentage = (bearish_count / total_articles) * 100 if total_articles > 0 else 0
        neutral_percentage = (neutral_count / total_articles) * 100 if total_articles > 0 else 0
        
        # Determine overall sentiment
        overall_sentiment = SentimentCategory.NEUTRAL
        
        if bullish_percentage > bearish_percentage + 20:
            overall_sentiment = SentimentCategory.BULLISH
        elif bearish_percentage > bullish_percentage + 20:
            overall_sentiment = SentimentCategory.BEARISH
        
        return {
            "ticker": ticker,
            "total_articles": total_articles,
            "bullish_count": bullish_count,
            "bearish_count": bearish_count,
            "neutral_count": neutral_count,
            "bullish_percentage": bullish_percentage,
            "bearish_percentage": bearish_percentage,
            "neutral_percentage": neutral_percentage,
            "days": days,
            "overall_sentiment": overall_sentiment
        }
    
    def get_sentiment_summary(self, ticker: str, days: int = 7) -> str:
        """
        Get a summary of sentiment for a specific ticker.
        
        Args:
            ticker: Stock ticker symbol
            days: Number of days to include
            
        Returns:
            Summary string
        """
        distribution = self.get_sentiment_distribution(ticker, days)
        
        if distribution["total_articles"] == 0:
            return f"No sentiment data available for {ticker} in the past {days} days."
        
        if distribution["overall_sentiment"] == SentimentCategory.BULLISH:
            return f"News sentiment for {ticker} is predominantly bullish ({round(distribution['bullish_percentage'], 1)}% positive) over the past {days} days."
        elif distribution["overall_sentiment"] == SentimentCategory.BEARISH:
            return f"News sentiment for {ticker} is predominantly bearish ({round(distribution['bearish_percentage'], 1)}% negative) over the past {days} days."
        else:
            return f"News sentiment for {ticker} is relatively neutral over the past {days} days."
