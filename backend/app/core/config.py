import os
from typing import Dict, Any

class Settings:
    def __init__(self):
        self.PROJECT_NAME: str = "News Aggregator"
        self.VERSION: str = "1.0.0"
        self.API_V1_STR: str = "/api/v1"
        self.SQLALCHEMY_DATABASE_URI: str = os.getenv("DATABASE_URL", "sqlite:///news_aggregator.db")

settings = Settings()
