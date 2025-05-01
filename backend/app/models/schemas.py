from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum


class BiasCategory(str, Enum):
    LEFT = "left"
    LEAN_LEFT = "lean_left"
    CENTER = "center"
    LEAN_RIGHT = "lean_right"
    RIGHT = "right"
    UNKNOWN = "unknown"


class SentimentCategory(str, Enum):
    BULLISH = "bullish"
    BEARISH = "bearish"
    NEUTRAL = "neutral"


class ArticleBase(BaseModel):
    """Base schema for article data."""
    ticker: str
    headline: str
    summary: str
    url: str
    source: str
    published_date: datetime


class ArticleCreate(ArticleBase):
    """Schema for creating a new article."""
    bias_label: BiasCategory
    sentiment_label: SentimentCategory
    sentiment_confidence: Optional[float] = None
    bias_score: Optional[float] = None
    embedding_vector: Optional[List[float]] = None


class ArticleResponse(ArticleBase):
    """Schema for article response."""
    id: int
    bias_label: BiasCategory
    sentiment_label: SentimentCategory
    sentiment_confidence: Optional[float] = None
    bias_score: Optional[float] = None
    created_at: datetime

    class Config:
        orm_mode = True


class BiasDistribution(BaseModel):
    """Schema for bias distribution statistics."""
    ticker: str
    total_articles: int
    left_count: int = 0
    lean_left_count: int = 0
    center_count: int = 0
    lean_right_count: int = 0
    right_count: int = 0
    unknown_count: int = 0
    left_percentage: float = Field(0.0, ge=0.0, le=100.0)
    lean_left_percentage: float = Field(0.0, ge=0.0, le=100.0)
    center_percentage: float = Field(0.0, ge=0.0, le=100.0)
    lean_right_percentage: float = Field(0.0, ge=0.0, le=100.0)
    right_percentage: float = Field(0.0, ge=0.0, le=100.0)
    unknown_percentage: float = Field(0.0, ge=0.0, le=100.0)
    days: int
    is_biased: bool = False  # True if one bias category dominates
    dominant_bias: Optional[BiasCategory] = None


class SourceBase(BaseModel):
    """Base schema for news source data."""
    name: str
    domain: str
    bias_rating: BiasCategory
    reference_url: Optional[str] = None


class SourceCreate(SourceBase):
    """Schema for creating a new source."""
    pass


class SourceResponse(SourceBase):
    """Schema for source response."""
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
