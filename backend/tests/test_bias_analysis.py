import pytest
import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the parent directory to the path so we can import the app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.bias_analysis_service import BiasAnalysisService
from app.models.schemas import BiasCategory

class TestBiasAnalysisService(unittest.TestCase):
    
    def setUp(self):
        # Create a mock database session
        self.mock_db = MagicMock()
        self.bias_service = BiasAnalysisService(self.mock_db)
        
    def test_get_source_bias_exact_match(self):
        # Setup mock source in database
        mock_source = MagicMock()
        mock_source.bias_rating = BiasCategory.CENTER
        mock_source.domain = "example.com"
        
        # Configure the mock query to return our mock source
        self.mock_db.query.return_value.filter.return_value.first.return_value = mock_source
        
        # Test the method
        result = self.bias_service.get_source_bias("example.com")
        
        # Assert the result is as expected
        self.assertEqual(result, BiasCategory.CENTER)
        
    def test_get_source_bias_with_www(self):
        # Setup mock source in database
        mock_source = MagicMock()
        mock_source.bias_rating = BiasCategory.LEFT
        mock_source.domain = "example.com"
        
        # Configure the mock query to return our mock source
        self.mock_db.query.return_value.filter.return_value.first.return_value = mock_source
        
        # Test the method with www prefix
        result = self.bias_service.get_source_bias("www.example.com")
        
        # Assert the result is as expected
        self.assertEqual(result, BiasCategory.LEFT)
        
    def test_get_source_bias_no_match(self):
        # Configure the mock query to return None (no match)
        self.mock_db.query.return_value.filter.return_value.first.return_value = None
        self.mock_db.query.return_value.all.return_value = []
        
        # Test the method with a domain that doesn't exist
        result = self.bias_service.get_source_bias("nonexistent.com")
        
        # Assert the result is UNKNOWN
        self.assertEqual(result, BiasCategory.UNKNOWN)
        
    def test_calculate_bias_distribution_empty(self):
        # Configure the mock query to return empty list
        self.mock_db.query.return_value.filter.return_value.all.return_value = []
        
        # Test the method with no articles
        result = self.bias_service.calculate_bias_distribution("AAPL")
        
        # Assert the result has expected properties
        self.assertEqual(result.ticker, "AAPL")
        self.assertEqual(result.total_articles, 0)
        self.assertEqual(result.is_biased, False)
        
    def test_calculate_bias_distribution_biased(self):
        # Create mock articles with predominantly LEFT bias
        mock_articles = []
        for i in range(10):
            article = MagicMock()
            article.bias_label = BiasCategory.LEFT
            mock_articles.append(article)
        
        # Add a few articles with other biases
        for bias in [BiasCategory.CENTER, BiasCategory.RIGHT]:
            article = MagicMock()
            article.bias_label = bias
            mock_articles.append(article)
            
        # Configure the mock query to return our mock articles
        self.mock_db.query.return_value.filter.return_value.all.return_value = mock_articles
        
        # Test the method
        result = self.bias_service.calculate_bias_distribution("AAPL")
        
        # Assert the result indicates bias
        self.assertEqual(result.ticker, "AAPL")
        self.assertEqual(result.total_articles, 12)
        self.assertEqual(result.left_count, 10)
        self.assertTrue(result.is_biased)
        self.assertEqual(result.dominant_bias, BiasCategory.LEFT)
        
    def test_get_viewpoint_diversity_warning(self):
        # Mock the calculate_bias_distribution method
        self.bias_service.calculate_bias_distribution = MagicMock()
        
        # Configure it to return a biased distribution
        mock_distribution = MagicMock()
        mock_distribution.is_biased = True
        mock_distribution.dominant_bias = BiasCategory.RIGHT
        mock_distribution.right_percentage = 75.0
        self.bias_service.calculate_bias_distribution.return_value = mock_distribution
        
        # Test the method
        result = self.bias_service.get_viewpoint_diversity_warning("AAPL")
        
        # Assert the result contains a warning
        self.assertIsNotNone(result)
        self.assertIn("predominantly from right sources", result)
        
    def test_no_viewpoint_diversity_warning(self):
        # Mock the calculate_bias_distribution method
        self.bias_service.calculate_bias_distribution = MagicMock()
        
        # Configure it to return a balanced distribution
        mock_distribution = MagicMock()
        mock_distribution.is_biased = False
        self.bias_service.calculate_bias_distribution.return_value = mock_distribution
        
        # Test the method
        result = self.bias_service.get_viewpoint_diversity_warning("AAPL")
        
        # Assert the result is None (no warning)
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
