# Deployment Guide

This guide provides instructions for deploying the Bias-Aware U.S. Stock Market News Aggregator to production environments.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Deployment Options](#deployment-options)
3. [Docker Deployment](#docker-deployment)
4. [Vercel and Supabase Deployment](#vercel-and-supabase-deployment)
5. [CI/CD Pipeline](#cicd-pipeline)
6. [Environment Variables](#environment-variables)
7. [Monitoring and Maintenance](#monitoring-and-maintenance)

## Prerequisites

Before deploying, ensure you have:

- API keys for all required services:
  - Polygon.io
  - Finnhub
  - Financial Datasets API
  - WhaleWisdom API
- A server or cloud environment with Docker support
- Domain name (optional but recommended for production)
- SSL certificate (recommended for production)

## Deployment Options

The application can be deployed using:

1. **Docker Compose**: Self-hosted deployment using the provided Docker configuration
2. **Vercel and Supabase**: Cloud-based deployment using Vercel for the frontend and Supabase for the backend database
3. **CI/CD Pipeline**: Automated deployment using GitHub Actions

## Docker Deployment

### Server Requirements

- Linux server (Ubuntu 20.04 LTS or newer recommended)
- Docker and Docker Compose installed
- At least 2GB RAM and 10GB storage
- Open ports: 80 (HTTP), 443 (HTTPS), 3000 (Frontend), 8000 (Backend API)

### Deployment Steps

1. Clone the repository on your server:
   ```
   git clone https://github.com/yourusername/bias-news-aggregator.git
   cd bias-news-aggregator
   ```

2. Create a `.env` file with your configuration:
   ```
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=your_secure_password
   POSTGRES_DB=newsdb
   POLYGON_API_KEY=your_polygon_api_key
   FINNHUB_API_KEY=your_finnhub_api_key
   FINANCIAL_DATASETS_API_KEY=your_financial_datasets_api_key
   WHALEWISDOM_API_KEY=your_whalewisdom_api_key
   NEWS_FETCH_INTERVAL_MINUTES=60
   ```

3. Start the application:
   ```
   docker-compose up -d
   ```

4. Set up a reverse proxy (Nginx or similar) to handle SSL termination and domain routing.

### Nginx Configuration Example

```nginx
server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name your-domain.com;

    ssl_certificate /path/to/certificate.crt;
    ssl_certificate_key /path/to/private.key;

    # Frontend
    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # Backend API
    location /api/ {
        proxy_pass http://localhost:8000/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Vercel and Supabase Deployment

### Supabase Setup

1. Create a new Supabase project at [supabase.com](https://supabase.com)
2. Get your Supabase URL and API key from the project settings
3. Run the database migrations:
   ```
   cd backend
   DATABASE_URL=your_supabase_postgres_connection_string alembic upgrade head
   ```
4. Run the seed script to populate initial data:
   ```
   DATABASE_URL=your_supabase_postgres_connection_string python -m app.db.init_db
   ```

### Vercel Setup for Frontend

1. Push your code to a GitHub repository
2. Create a new project in Vercel and connect it to your repository
3. Configure the following environment variables:
   ```
   REACT_APP_API_BASE_URL=https://your-backend-url.com/api/v1
   ```
4. Deploy the frontend:
   ```
   cd frontend
   vercel
   ```

### Vercel Setup for Backend API

1. Create a `vercel.json` file in the backend directory:
   ```json
   {
     "version": 2,
     "builds": [
       {
         "src": "app/main.py",
         "use": "@vercel/python"
       }
     ],
     "routes": [
       {
         "src": "/(.*)",
         "dest": "app/main.py"
       }
     ]
   }
   ```

2. Configure the following environment variables in Vercel:
   ```
   DATABASE_URL=your_supabase_postgres_connection_string
   POLYGON_API_KEY=your_polygon_api_key
   FINNHUB_API_KEY=your_finnhub_api_key
   FINANCIAL_DATASETS_API_KEY=your_financial_datasets_api_key
   WHALEWISDOM_API_KEY=your_whalewisdom_api_key
   ```

3. Deploy the backend:
   ```
   cd backend
   vercel
   ```

## CI/CD Pipeline

The repository includes a GitHub Actions workflow for continuous integration and deployment.

### Setup

1. Add the following secrets to your GitHub repository:
   - `DOCKERHUB_USERNAME`: Your Docker Hub username
   - `DOCKERHUB_TOKEN`: Your Docker Hub access token
   - `DEPLOY_HOST`: Your deployment server hostname or IP
   - `DEPLOY_USERNAME`: SSH username for your deployment server
   - `DEPLOY_KEY`: SSH private key for your deployment server

2. Push to the main branch to trigger the CI/CD pipeline.

### Pipeline Workflow

The CI/CD pipeline performs the following steps:
1. Runs backend tests
2. Runs frontend tests
3. Builds Docker images
4. Pushes images to Docker Hub
5. Deploys to the production server

## Environment Variables

### Backend Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| DATABASE_URL | PostgreSQL connection string | Yes |
| POLYGON_API_KEY | API key for Polygon.io | Yes |
| FINNHUB_API_KEY | API key for Finnhub | Yes |
| FINANCIAL_DATASETS_API_KEY | API key for Financial Datasets API | Yes |
| WHALEWISDOM_API_KEY | API key for WhaleWisdom API | Yes |
| NEWS_FETCH_INTERVAL_MINUTES | Interval for fetching news (default: 60) | No |
| SENTIMENT_MODEL_NAME | Name of sentiment model to use (default: finbert) | No |

### Frontend Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| REACT_APP_API_BASE_URL | URL of the backend API | Yes |
| REACT_APP_DEFAULT_TICKERS | Default tickers to display (comma-separated) | No |

## Monitoring and Maintenance

### Logs

View Docker container logs:
```
docker-compose logs -f
```

View specific service logs:
```
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f scheduler
```

### Database Backups

Create a database backup:
```
docker-compose exec postgres pg_dump -U postgres newsdb > backup.sql
```

Restore from a backup:
```
cat backup.sql | docker-compose exec -T postgres psql -U postgres newsdb
```

### Updating the Application

1. Pull the latest code:
   ```
   git pull
   ```

2. Rebuild and restart containers:
   ```
   docker-compose down
   docker-compose build
   docker-compose up -d
   ```

### Scaling

For higher traffic loads, consider:
1. Increasing resources allocated to Docker containers
2. Setting up a load balancer
3. Implementing database replication
4. Using a managed Kubernetes service for container orchestration
