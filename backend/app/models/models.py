from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Text, Enum, ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.db.session import Base
from app.models.schemas import BiasCategory, SentimentCategory


class Article(Base):
    """Database model for news articles."""
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String, index=True, nullable=False)
    headline = Column(String, nullable=False)
    summary = Column(Text, nullable=False)
    url = Column(String, unique=True, nullable=False)
    source = Column(String, nullable=False)
    bias_label = Column(Enum(BiasCategory), nullable=False)
    sentiment_label = Column(Enum(SentimentCategory), nullable=False)
    sentiment_confidence = Column(Float, nullable=True)
    bias_score = Column(Float, nullable=True)
    published_date = Column(DateTime, nullable=False, index=True)
    embedding_vector = Column(ARRAY(Float), nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)


class Source(Base):
    """Database model for news sources."""
    __tablename__ = "sources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    domain = Column(String, unique=True, nullable=False, index=True)
    bias_rating = Column(Enum(BiasCategory), nullable=False)
    reference_url = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)


class User(Base):
    """Database model for users (optional)."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Integer, default=True, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    watchlists = relationship("Watchlist", back_populates="user")


class Watchlist(Base):
    """Database model for user watchlists (optional)."""
    __tablename__ = "watchlists"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    ticker = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    
    user = relationship("User", back_populates="watchlists")
    
    __table_args__ = (
        # Composite unique constraint to prevent duplicate tickers per user
        {'sqlite_autoincrement': True},
    )
