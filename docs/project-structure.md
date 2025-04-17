# Bias-Aware U.S. Stock Market News Aggregator - Project Structure

This document provides an overview of the project structure and organization.

## Directory Structure

```
bias-news-aggregator/
├── backend/                  # Backend API and services
│   ├── app/                  # Application code
│   │   ├── api/              # API endpoints
│   │   │   └── api_v1/       # API version 1
│   │   │       ├── endpoints/# API endpoint modules
│   │   │       └── api.py    # API router
│   │   ├── core/             # Core configuration
│   │   ├── db/               # Database modules
│   │   │   ├── migrations/   # Alembic migrations
│   │   │   └── seed_data.py  # Seed data for initial setup
│   │   ├── models/           # Database models
│   │   ├── services/         # Business logic services
│   │   └── main.py           # Application entry point
│   ├── tests/                # Backend tests
│   ├── alembic.ini           # Alembic configuration
│   ├── Dockerfile            # Backend Docker configuration
│   └── requirements.txt      # Python dependencies
│
├── frontend/                 # React frontend
│   ├── public/               # Static files
│   ├── src/                  # Source code
│   │   ├── components/       # Reusable UI components
│   │   ├── pages/            # Page components
│   │   ├── App.js            # Main application component
│   │   └── index.js          # Entry point
│   ├── tests/                # Frontend tests
│   ├── Dockerfile            # Frontend Docker configuration
│   └── package.json          # Node.js dependencies
│
├── docs/                     # Documentation
│   ├── api.md                # API documentation
│   ├── deployment.md         # Deployment guide
│   └── user-guide.md         # User guide
│
├── .github/                  # GitHub configuration
│   └── workflows/            # GitHub Actions workflows
│       └── ci-cd.yml         # CI/CD pipeline configuration
│
├── docker-compose.yml        # Docker Compose configuration
├── .gitignore                # Git ignore file
└── README.md                 # Project overview
```

## Key Components

### Backend

1. **API Endpoints**
   - `news.py`: Endpoints for retrieving news articles
   - `analysis.py`: Endpoints for bias and sentiment analysis
   - `metadata.py`: Endpoints for source information and methodology
   - `health.py`: Health check endpoint

2. **Database Models**
   - `models.py`: SQLAlchemy ORM models
   - `schemas.py`: Pydantic schemas for API requests/responses

3. **Services**
   - `news_service.py`: News retrieval and management
   - `bias_analyzer.py`: Analysis of news source bias
   - `sentiment_analyzer.py`: Analysis of article sentiment
   - `polygon_service.py`: Integration with Polygon.io API
   - `financial_datasets_service.py`: Integration with Financial Datasets API
   - `whalewisdom_service.py`: Integration with WhaleWisdom API
   - `finnhub_service.py`: Integration with Finnhub API
   - `news_scheduler.py`: Background service for periodic news fetching

### Frontend

1. **Pages**
   - `HomePage.js`: Landing page with featured news and trending tickers
   - `TickerPage.js`: Detailed view for a specific ticker
   - `PortfolioPage.js`: Portfolio management and analysis

2. **Components**
   - `BiasDistributionChart.js`: Visualization of bias distribution
   - `SentimentDistributionChart.js`: Visualization of sentiment distribution
   - `NewsArticleList.js`: Display of news articles
   - `BiasLegend.js`: Legend explaining bias categories
   - `NewsFilters.js`: Filters for news articles
   - `TrendingTickers.js`: Display of trending tickers
   - `FeaturedNews.js`: Display of featured news articles
   - `Navbar.js`: Navigation bar
   - `Footer.js`: Page footer

### Infrastructure

1. **Docker Configuration**
   - `docker-compose.yml`: Multi-container setup
   - Backend `Dockerfile`: Python FastAPI container
   - Frontend `Dockerfile`: React container

2. **CI/CD Pipeline**
   - GitHub Actions workflow for testing, building, and deployment

## Data Flow

1. **News Ingestion**
   - Scheduler triggers periodic news fetching
   - News is retrieved from multiple sources via API integrations
   - Articles are processed and stored in the database

2. **Bias and Sentiment Analysis**
   - News sources are categorized by political bias
   - Article content is analyzed for sentiment
   - Analysis results are stored with the articles

3. **API Endpoints**
   - Frontend requests data from backend API
   - API retrieves and processes data from the database
   - API returns formatted responses to the frontend

4. **User Interface**
   - Frontend components render data in user-friendly visualizations
   - Users can filter and interact with the data
   - Portfolio tracking allows personalized news monitoring
