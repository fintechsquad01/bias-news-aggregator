# Bias-Aware U.S. Stock Market News Aggregator

A web-based platform that aggregates stock market news and analyzes each piece for ideological bias and market sentiment. The system labels news sources on a left-center-right spectrum, indicates sentiment (bullish, bearish, neutral), and presents this information in a user-friendly interface.

## Features

- **News Aggregation**: Collects articles from multiple financial news sources
- **Bias Analysis**: Categorizes news sources on a left-center-right political spectrum
- **Sentiment Analysis**: Determines if articles are bullish, bearish, or neutral about mentioned stocks
- **Interactive Visualizations**: Charts showing bias and sentiment distribution
- **Portfolio Tracking**: Monitor news for multiple stocks in a personalized portfolio
- **Viewpoint Diversity Warnings**: Alerts when coverage lacks balance

## Tech Stack

- **Frontend**: React, Material UI, Recharts
- **Backend**: FastAPI, SQLAlchemy, Alembic
- **Database**: PostgreSQL (via Supabase)
- **Deployment**: Vercel, Docker
- **CI/CD**: GitHub Actions

## Getting Started

### Prerequisites

- Node.js 16+
- Python 3.9+
- API keys for:
  - Polygon.io
  - Financial Datasets API
  - WhaleWisdom API
  - Finnhub API

### Local Development

1. Clone the repository:
   ```
   git clone https://github.com/fintechsquad01/bias-news-aggregator.git
   cd bias-news-aggregator
   ```

2. Set up the backend:
   ```
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   cp .env.example .env  # Edit with your API keys
   ```

3. Set up the frontend:
   ```
   cd frontend
   npm install
   cp .env.example .env  # Edit with your API configuration
   ```

4. Run the backend:
   ```
   cd backend
   uvicorn app.main:app --reload
   ```

5. Run the frontend:
   ```
   cd frontend
   npm run dev
   ```

6. Open [http://localhost:3000](http://localhost:3000) in your browser

### Docker Deployment

Alternatively, use Docker Compose:

```
docker-compose up -d
```

## Documentation

- [API Documentation](docs/api.md)
- [User Guide](docs/user-guide.md)
- [Deployment Guide](docs/deployment.md)
- [Project Structure](docs/project-structure.md)

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
