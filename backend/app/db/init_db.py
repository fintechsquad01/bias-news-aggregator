from sqlalchemy import create_engine
from alembic.config import Config
from alembic import command
import os
import sys

from app.db.session import Base, engine
from app.models.models import Article, Source, User, Watchlist
from app.core.config import settings

def init_db():
    """Initialize the database with tables."""
    # Create tables
    Base.metadata.create_all(bind=engine)
    print("Database tables created.")

if __name__ == "__main__":
    init_db()
