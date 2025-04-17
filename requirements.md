# Bias-Aware U.S. Stock Market News Aggregator - Requirements Analysis

## Core Features

### News Aggregation
- Fetch news from multiple sources (Polygon.io, Finnhub, SEC EDGAR, Reddit)
- Standardize news data format across sources
- Associate news with stock tickers
- Schedule regular updates for real-time data

### Bias Analysis
- Implement source-based bias classification using AllSides Media Bias Ratings
- Categorize sources as Left, Lean Left, Center, Lean Right, or Right
- Default unknown sources to "Center/Not rated"
- Display bias distribution for news coverage

### Sentiment Analysis
- Analyze news sentiment for each stock (Bullish, Bearish, Neutral)
- Use pre-trained financial sentiment model (FinBERT)
- Apply sentiment analysis to headlines and summaries
- Calculate aggregate sentiment for stocks

### Article Clustering
- Use vector embeddings to group similar news articles
- Identify coverage of the same story from different perspectives
- Show diversity of sources per story
- Implement similarity search for related articles

### User Interface
- Ticker-based news pages with bias and sentiment indicators
- Portfolio/watchlist view for personalized news feeds
- Bias distribution visualization (charts/indicators)
- Filtering options by bias category and sentiment
- Responsive design for desktop and mobile

### Optional Features
- AI-generated summaries of news articles
- Bias diversity warnings when coverage is one-sided
- User accounts and preferences

## Technical Components

### Backend
- Python-based API server (FastAPI)
- Scheduled jobs for news ingestion
- NLP processing pipeline
- Database storage and retrieval
- RESTful API endpoints

### Frontend
- React-based single-page application
- Responsive UI components
- Data visualization for bias and sentiment
- Search and filtering functionality

### Database
- PostgreSQL with pgvector extension for embeddings
- Tables for articles, sources, users, preferences
- Efficient indexing for performance

### Infrastructure
- Docker containerization
- CI/CD pipeline with GitHub Actions
- Deployment configuration

## External APIs and Data Sources
- Polygon.io - Stock news articles
- Finnhub - Alternative stock news source
- SEC EDGAR - Company filings
- Reddit - Social sentiment (optional)
- AllSides - Media bias ratings data

## Constraints
- 4-month development timeline
- Small development team
- Budget constraints for API usage
- Focus on MVP features first
