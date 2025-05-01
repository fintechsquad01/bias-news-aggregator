from pydantic_settings import BaseSettings
from typing import Optional, List
import os


class Settings(BaseSettings):
    """Application settings."""
    
    # API settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Bias-Aware Stock News Aggregator"
    
    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/news_aggregator")
    
    # CORS settings
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost", "http://localhost:3000", "http://localhost:8000"]
    CORS_ORIGINS: Optional[str] = None
    
    # External API keys
    POLYGON_API_KEY: Optional[str] = None
    FINNHUB_API_KEY: Optional[str] = None
    OPENAI_API_KEY: Optional[str] = None
    REDDIT_CLIENT_ID: Optional[str] = None
    REDDIT_CLIENT_SECRET: Optional[str] = None
    FINANCIAL_DATASETS_API_KEY: Optional[str] = None
    WHALEWISDOM_API_KEY: Optional[str] = None
    
    # Supabase settings
    SUPABASE_URL: Optional[str] = None
    SUPABASE_SERVICE_ROLE_KEY: Optional[str] = None
    
    # News fetch settings
    NEWS_FETCH_INTERVAL_MINUTES: int = 5
    MAX_NEWS_AGE_DAYS: int = 7
    
    # Security settings (if implementing user auth)
    SECRET_KEY: str = os.getenv("SECRET_KEY", "supersecretkey")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    JWT_SECRET: Optional[str] = None
    
    # Environment settings
    NODE_ENV: Optional[str] = None
    
    # NLP settings
    SENTIMENT_MODEL_NAME: str = "ProsusAI/finbert"
    EMBEDDING_MODEL_NAME: str = "sentence-transformers/all-MiniLM-L6-v2"
    SIMILARITY_THRESHOLD: float = 0.85  # Threshold for article similarity
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
