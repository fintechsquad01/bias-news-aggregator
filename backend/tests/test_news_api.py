import pytest
import unittest
from unittest.mock import patch, MagicMock
import sys
import os
from fastapi.testclient import TestClient

# Add the parent directory to the path so we can import the app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app
from app.api.api_v1.endpoints.news import get_news

class TestNewsAPI(unittest.TestCase):
    
    def setUp(self):
        self.client = TestClient(app)
        
    def test_get_news_endpoint(self):
        # Mock the get_news_by_ticker function
        with patch('app.api.api_v1.endpoints.news.get_news_by_ticker') as mock_get_news:
            # Configure mock to return sample articles
            mock_articles = [
                {
                    "id": 1,
                    "ticker": "AAPL",
                    "headline": "Test Headline",
                    "summary": "Test Summary",
                    "url": "https://example.com",
                    "source": "Test Source",
                    "bias_label": "center",
                    "sentiment_label": "bullish",
                    "published_date": "2025-04-17T12:00:00Z"
                }
            ]
            mock_get_news.return_value = mock_articles
            
            # Make request to the endpoint
            response = self.client.get("/api/v1/news?ticker=AAPL")
            
            # Assert response status code and content
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.json()), 1)
            self.assertEqual(response.json()[0]["ticker"], "AAPL")
            
            # Verify mock was called with correct parameters
            mock_get_news.assert_called_once()
            args, kwargs = mock_get_news.call_args
            self.assertEqual(kwargs["ticker"], "AAPL")
            
    def test_get_news_with_filters(self):
        # Mock the get_news_by_ticker function
        with patch('app.api.api_v1.endpoints.news.get_news_by_ticker') as mock_get_news:
            # Configure mock to return sample articles
            mock_get_news.return_value = []
            
            # Make request to the endpoint with filters
            response = self.client.get("/api/v1/news?ticker=AAPL&bias=left,center&sentiment=bullish")
            
            # Assert response status code
            self.assertEqual(response.status_code, 200)
            
            # Verify mock was called with correct parameters
            mock_get_news.assert_called_once()
            args, kwargs = mock_get_news.call_args
            self.assertEqual(kwargs["ticker"], "AAPL")
            self.assertEqual(kwargs["bias_list"], ["left", "center"])
            self.assertEqual(kwargs["sentiment_list"], ["bullish"])
            
    def test_get_portfolio_news(self):
        # Mock the get_news_by_ticker function
        with patch('app.api.api_v1.endpoints.news.get_news_by_ticker') as mock_get_news:
            # Configure mock to return different articles for different tickers
            def side_effect(db, ticker, *args, **kwargs):
                return [
                    {
                        "id": 1,
                        "ticker": ticker,
                        "headline": f"Test Headline for {ticker}",
                        "summary": "Test Summary",
                        "url": "https://example.com",
                        "source": "Test Source",
                        "bias_label": "center",
                        "sentiment_label": "bullish",
                        "published_date": "2025-04-17T12:00:00Z"
                    }
                ]
            
            mock_get_news.side_effect = side_effect
            
            # Make request to the portfolio endpoint
            response = self.client.get("/api/v1/news/portfolio?tickers=AAPL,MSFT")
            
            # Assert response status code and content
            self.assertEqual(response.status_code, 200)
            self.assertIn("AAPL", response.json())
            self.assertIn("MSFT", response.json())
            self.assertEqual(response.json()["AAPL"][0]["ticker"], "AAPL")
            self.assertEqual(response.json()["MSFT"][0]["ticker"], "MSFT")
            
            # Verify mock was called twice (once for each ticker)
            self.assertEqual(mock_get_news.call_count, 2)
            
    def test_get_trending_news(self):
        # Mock the get_news_by_ticker function
        with patch('app.api.api_v1.endpoints.news.get_news_by_ticker') as mock_get_news:
            # Configure mock to return sample articles
            mock_get_news.return_value = [
                {
                    "id": 1,
                    "ticker": "AAPL",
                    "headline": "Test Headline",
                    "summary": "Test Summary",
                    "url": "https://example.com",
                    "source": "Test Source",
                    "bias_label": "center",
                    "sentiment_label": "bullish",
                    "published_date": "2025-04-17T12:00:00Z"
                }
            ]
            
            # Make request to the trending endpoint
            response = self.client.get("/api/v1/news/trending")
            
            # Assert response status code
            self.assertEqual(response.status_code, 200)
            
            # Verify mock was called at least once
            mock_get_news.assert_called()

if __name__ == '__main__':
    unittest.main()
