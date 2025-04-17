import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the parent directory to the path so we can import the app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.sentiment_analyzer import SentimentAnalyzer
from app.models.schemas import SentimentCategory

class TestSentimentAnalyzer(unittest.TestCase):
    
    def setUp(self):
        # Create a mock sentiment pipeline
        self.mock_pipeline = MagicMock()
        
        # Patch the pipeline initialization
        with patch('app.services.sentiment_analyzer.pipeline', return_value=self.mock_pipeline):
            self.sentiment_analyzer = SentimentAnalyzer()
            
        # Set the pipeline directly to ensure it's available
        self.sentiment_analyzer.sentiment_pipeline = self.mock_pipeline
        
    def test_analyze_sentiment_bullish(self):
        # Configure mock to return bullish sentiment
        self.mock_pipeline.return_value = [{'label': 'positive', 'score': 0.95}]
        
        # Test the method with bullish text
        result = self.sentiment_analyzer.analyze_sentiment("Company reports record profits and raises guidance.")
        
        # Assert the result is BULLISH
        self.assertEqual(result, SentimentCategory.BULLISH)
        
    def test_analyze_sentiment_bearish(self):
        # Configure mock to return bearish sentiment
        self.mock_pipeline.return_value = [{'label': 'negative', 'score': 0.85}]
        
        # Test the method with bearish text
        result = self.sentiment_analyzer.analyze_sentiment("Company misses earnings expectations and lowers guidance.")
        
        # Assert the result is BEARISH
        self.assertEqual(result, SentimentCategory.BEARISH)
        
    def test_analyze_sentiment_neutral(self):
        # Configure mock to return neutral sentiment
        self.mock_pipeline.return_value = [{'label': 'neutral', 'score': 0.75}]
        
        # Test the method with neutral text
        result = self.sentiment_analyzer.analyze_sentiment("Company reports quarterly earnings in line with expectations.")
        
        # Assert the result is NEUTRAL
        self.assertEqual(result, SentimentCategory.NEUTRAL)
        
    def test_analyze_sentiment_long_text_truncation(self):
        # Configure mock to return any sentiment
        self.mock_pipeline.return_value = [{'label': 'positive', 'score': 0.9}]
        
        # Create a very long text (over 512 characters)
        long_text = "Company reports earnings " * 100
        
        # Test the method with long text
        result = self.sentiment_analyzer.analyze_sentiment(long_text)
        
        # Assert the pipeline was called with truncated text
        args, _ = self.mock_pipeline.call_args
        self.assertTrue(len(args[0]) <= 512)
        
    def test_analyze_sentiment_pipeline_error(self):
        # Configure mock to raise an exception
        self.mock_pipeline.side_effect = Exception("Test error")
        
        # Test the method with any text
        result = self.sentiment_analyzer.analyze_sentiment("Any text")
        
        # Assert the result is NEUTRAL (default when error occurs)
        self.assertEqual(result, SentimentCategory.NEUTRAL)
        
    def test_analyze_sentiment_no_pipeline(self):
        # Set pipeline to None to simulate initialization failure
        self.sentiment_analyzer.sentiment_pipeline = None
        
        # Test the method with any text
        result = self.sentiment_analyzer.analyze_sentiment("Any text")
        
        # Assert the result is NEUTRAL (default when pipeline not available)
        self.assertEqual(result, SentimentCategory.NEUTRAL)
        
    def test_analyze_article(self):
        # Configure mock to return bullish sentiment
        self.mock_pipeline.return_value = [{'label': 'positive', 'score': 0.9}]
        
        # Create a mock article
        mock_article = MagicMock()
        mock_article.headline = "Great quarterly results"
        mock_article.summary = "Company exceeds expectations"
        
        # Test the method
        result = self.sentiment_analyzer.analyze_article(mock_article)
        
        # Assert the result is BULLISH
        self.assertEqual(result, SentimentCategory.BULLISH)
        
        # Assert the pipeline was called with combined headline and summary
        args, _ = self.mock_pipeline.call_args
        self.assertEqual(args[0], "Great quarterly results Company exceeds expectations")

if __name__ == '__main__':
    unittest.main()
