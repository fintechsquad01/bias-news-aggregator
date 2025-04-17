# API Documentation

This document provides detailed information about the Bias-Aware U.S. Stock Market News Aggregator API endpoints.

## Base URL

All API endpoints are prefixed with `/api/v1`.

## Authentication

Currently, the API does not require authentication.

## News Endpoints

### Get News Articles

```
GET /news
```

Retrieves news articles for a specific ticker with optional filtering.

**Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| ticker | string | **Required**. Stock ticker symbol |
| bias | string | Optional. Comma-separated bias categories (left,lean_left,center,lean_right,right) |
| sentiment | string | Optional. Comma-separated sentiment values (bullish,bearish,neutral) |
| limit | integer | Optional. Number of articles to return (default: 20) |
| offset | integer | Optional. Offset for pagination (default: 0) |

**Response:**

```json
[
  {
    "id": 1,
    "ticker": "AAPL",
    "headline": "Apple Reports Record Quarterly Revenue",
    "summary": "Apple Inc. announced financial results for its fiscal 2025 second quarter ended March 29, 2025, with record revenue of $97.3 billion, up 9 percent year over year.",
    "url": "https://example.com/article1",
    "source": "Financial Times",
    "bias_label": "center",
    "sentiment_label": "bullish",
    "published_date": "2025-04-15T14:30:00Z"
  }
]
```

### Get Portfolio News

```
GET /news/portfolio
```

Retrieves news for multiple tickers (portfolio view).

**Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| tickers | string | **Required**. Comma-separated list of ticker symbols |
| limit | integer | Optional. Number of articles to return per ticker (default: 10) |

**Response:**

```json
{
  "AAPL": [
    {
      "id": 1,
      "ticker": "AAPL",
      "headline": "Apple Reports Record Quarterly Revenue",
      "summary": "Apple Inc. announced financial results for its fiscal 2025 second quarter ended March 29, 2025, with record revenue of $97.3 billion, up 9 percent year over year.",
      "url": "https://example.com/article1",
      "source": "Financial Times",
      "bias_label": "center",
      "sentiment_label": "bullish",
      "published_date": "2025-04-15T14:30:00Z"
    }
  ],
  "MSFT": [
    {
      "id": 2,
      "ticker": "MSFT",
      "headline": "Microsoft Cloud Growth Accelerates",
      "summary": "Microsoft reported strong fiscal third-quarter results, with cloud revenue exceeding analyst expectations as more businesses adopt AI-powered solutions.",
      "url": "https://example.com/article2",
      "source": "Wall Street Journal",
      "bias_label": "lean_right",
      "sentiment_label": "bullish",
      "published_date": "2025-04-16T09:15:00Z"
    }
  ]
}
```

### Get Trending News

```
GET /news/trending
```

Retrieves trending news articles across all tickers.

**Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| limit | integer | Optional. Number of trending articles to return (default: 10) |

**Response:**

```json
[
  {
    "id": 1,
    "ticker": "AAPL",
    "headline": "Apple Reports Record Quarterly Revenue",
    "summary": "Apple Inc. announced financial results for its fiscal 2025 second quarter ended March 29, 2025, with record revenue of $97.3 billion, up 9 percent year over year.",
    "url": "https://example.com/article1",
    "source": "Financial Times",
    "bias_label": "center",
    "sentiment_label": "bullish",
    "published_date": "2025-04-15T14:30:00Z"
  }
]
```

## Analysis Endpoints

### Get Ticker Analysis

```
GET /analysis/ticker/{ticker}/analysis
```

Retrieves comprehensive analysis for a ticker including bias and sentiment.

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| ticker | string | **Required**. Stock ticker symbol |

**Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| days | integer | Optional. Number of days to include in analysis (default: 7) |

**Response:**

```json
{
  "ticker": "AAPL",
  "days": 7,
  "bias_distribution": {
    "ticker": "AAPL",
    "total_articles": 50,
    "left_count": 15,
    "lean_left_count": 10,
    "center_count": 10,
    "lean_right_count": 8,
    "right_count": 7,
    "left_percentage": 30,
    "lean_left_percentage": 20,
    "center_percentage": 20,
    "lean_right_percentage": 16,
    "right_percentage": 14,
    "days": 7,
    "is_biased": false
  },
  "sentiment_distribution": {
    "ticker": "AAPL",
    "total_articles": 50,
    "bullish_count": 25,
    "bearish_count": 15,
    "neutral_count": 10,
    "bullish_percentage": 50,
    "bearish_percentage": 30,
    "neutral_percentage": 20,
    "days": 7,
    "overall_sentiment": "bullish"
  },
  "diversity_warning": null,
  "sentiment_summary": "News sentiment for AAPL is predominantly bullish (50.0% positive) over the past 7 days."
}
```

### Get Ticker Bias Distribution

```
GET /analysis/ticker/{ticker}/bias
```

Retrieves bias distribution statistics for a specific ticker.

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| ticker | string | **Required**. Stock ticker symbol |

**Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| days | integer | Optional. Number of days to include (default: 7) |

**Response:**

```json
{
  "ticker": "AAPL",
  "total_articles": 50,
  "left_count": 15,
  "lean_left_count": 10,
  "center_count": 10,
  "lean_right_count": 8,
  "right_count": 7,
  "left_percentage": 30,
  "lean_left_percentage": 20,
  "center_percentage": 20,
  "lean_right_percentage": 16,
  "right_percentage": 14,
  "days": 7,
  "is_biased": false
}
```

### Get Ticker Sentiment

```
GET /analysis/ticker/{ticker}/sentiment
```

Retrieves sentiment distribution statistics for a specific ticker.

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| ticker | string | **Required**. Stock ticker symbol |

**Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| days | integer | Optional. Number of days to include (default: 7) |

**Response:**

```json
{
  "ticker": "AAPL",
  "total_articles": 50,
  "bullish_count": 25,
  "bearish_count": 15,
  "neutral_count": 10,
  "bullish_percentage": 50,
  "bearish_percentage": 30,
  "neutral_percentage": 20,
  "days": 7,
  "overall_sentiment": "bullish"
}
```

### Get Portfolio Analysis

```
GET /analysis/portfolio
```

Retrieves comprehensive analysis for a portfolio of tickers.

**Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| tickers | string | **Required**. Comma-separated list of ticker symbols |
| days | integer | Optional. Number of days to include (default: 7) |

**Response:**

```json
{
  "tickers": ["AAPL", "MSFT", "GOOGL"],
  "days": 7,
  "ticker_results": {
    "AAPL": {
      "ticker": "AAPL",
      "bias_distribution": { ... },
      "sentiment_distribution": { ... },
      "diversity_warning": null,
      "sentiment_summary": "News sentiment for AAPL is predominantly bullish (50.0% positive) over the past 7 days."
    },
    "MSFT": { ... },
    "GOOGL": { ... }
  },
  "aggregate": {
    "total_articles": 135,
    "bias_distribution": { ... },
    "sentiment_distribution": { ... },
    "biased_tickers": ["GOOGL"],
    "has_biased_coverage": true
  }
}
```

### Run Analysis

```
POST /analysis/analyze
```

Triggers background analysis of news articles.

**Response:**

```json
{
  "message": "Analysis started in background"
}
```

## Metadata Endpoints

### Get Sources

```
GET /metadata/sources
```

Retrieves a list of all news sources with their bias ratings.

**Response:**

```json
[
  {
    "id": 1,
    "name": "CNN",
    "domain": "cnn.com",
    "bias_rating": "lean_left",
    "description": "Cable News Network, an American news-based pay television channel"
  }
]
```

### Get Source by Domain

```
GET /metadata/sources/{domain}
```

Retrieves a specific news source by domain.

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| domain | string | **Required**. Domain of the news source |

**Response:**

```json
{
  "id": 1,
  "name": "CNN",
  "domain": "cnn.com",
  "bias_rating": "lean_left",
  "description": "Cable News Network, an American news-based pay television channel"
}
```

### Get Methodology

```
GET /metadata/methodology
```

Retrieves information about the methodology used for bias and sentiment analysis.

**Response:**

```json
{
  "bias_methodology": {
    "description": "We categorize news sources on a political spectrum from Left to Right based on AllSides Media Bias Ratings, a widely respected methodology.",
    "categories": [
      {"name": "left", "description": "Sources with a strong liberal bias"},
      {"name": "lean_left", "description": "Sources with a moderate liberal bias"},
      {"name": "center", "description": "Sources with minimal partisan bias"},
      {"name": "lean_right", "description": "Sources with a moderate conservative bias"},
      {"name": "right", "description": "Sources with a strong conservative bias"},
      {"name": "unknown", "description": "Sources with an undetermined bias"}
    ],
    "reference": "https://www.allsides.com/media-bias/media-bias-ratings"
  },
  "sentiment_methodology": {
    "description": "Our sentiment analysis uses natural language processing to determine if an article is bullish (positive), bearish (negative), or neutral about a stock.",
    "categories": [
      {"name": "bullish", "description": "Positive sentiment towards the stock"},
      {"name": "bearish", "description": "Negative sentiment towards the stock"},
      {"name": "neutral", "description": "Neutral or balanced sentiment towards the stock"}
    ],
    "model": "FinBERT or similar financial sentiment analysis model"
  }
}
```

## Health Endpoint

### Get Health Status

```
GET /health
```

Checks the health status of the API.

**Response:**

```json
{
  "status": "ok",
  "version": "1.0.0"
}
```
