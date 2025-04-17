# Bias-Aware U.S. Stock Market News Aggregator - Architecture Design

## System Architecture

### Data Flow
1. **News Ingestion Layer**
   - Scheduled jobs fetch news from external APIs
   - Data is normalized and stored in database
   - Metadata extraction (ticker symbols, publication date)

2. **Analysis Layer**
   - Bias classification based on source
   - Sentiment analysis of content
   - Vector embedding generation for similarity
   - Article clustering by topic/story

3. **Storage Layer**
   - PostgreSQL database with pgvector extension
   - Caching for frequently accessed data
   - Efficient indexing for performance

4. **API Layer**
   - RESTful endpoints for frontend consumption
   - Filtering, pagination, and sorting
   - Authentication (if implementing user accounts)

5. **Frontend Layer**
   - React-based SPA
   - Responsive UI components
   - Data visualization
   - User interaction handling

### Component Diagram
```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  External APIs  │────▶│  Ingestion Jobs │────▶│  Database       │
└─────────────────┘     └─────────────────┘     └────────┬────────┘
                                                         │
                                                         ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Frontend SPA   │◀───▶│  Backend API    │◀───▶│  Analysis       │
└─────────────────┘     └─────────────────┘     │  Modules        │
                                                 └─────────────────┘
```

## Database Schema

### Articles Table
- id (PK)
- ticker (indexed)
- headline
- summary
- url
- source
- bias_label
- sentiment_label
- published_date (indexed)
- embedding_vector
- created_at
- updated_at

### Sources Table
- id (PK)
- name
- domain
- bias_rating
- reference_url
- created_at
- updated_at

### Users Table (Optional)
- id (PK)
- email
- hashed_password
- created_at
- updated_at

### Watchlists Table (Optional)
- id (PK)
- user_id (FK)
- ticker
- created_at
- updated_at

## API Endpoints

### News Endpoints
- GET /api/news?ticker=SYMBOL&bias=left,right&sentiment=bullish,bearish
- GET /api/news/summary?ticker=SYMBOL
- GET /api/news/bias-distribution?ticker=SYMBOL
- GET /api/news/portfolio?tickers=SYMBOL1,SYMBOL2

### User Endpoints (Optional)
- POST /api/users/register
- POST /api/users/login
- GET /api/users/preferences
- PUT /api/users/preferences

## Deployment Architecture

### Docker Containers
- Backend container
- Frontend container
- Database container

### CI/CD Pipeline
- GitHub Actions workflow
- Testing, building, and deployment stages
- Docker image publishing

### Hosting Options
- Single VM deployment with Docker Compose
- Separate services for frontend and backend
- Database with vector search capabilities
