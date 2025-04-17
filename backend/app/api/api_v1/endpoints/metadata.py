from fastapi import APIRouter, Depends, Query, HTTPException, Path
from typing import List, Optional
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.models import Source
from app.models.schemas import SourceResponse

router = APIRouter()

@router.get("/sources", response_model=List[SourceResponse])
def get_sources(
    db: Session = Depends(get_db)
):
    """
    Get list of all news sources with their bias ratings.
    """
    sources = db.query(Source).all()
    return [SourceResponse.from_orm(source) for source in sources]

@router.get("/sources/{domain}", response_model=SourceResponse)
def get_source_by_domain(
    domain: str = Path(..., description="Domain of the news source"),
    db: Session = Depends(get_db)
):
    """
    Get a specific news source by domain.
    """
    # Clean up domain
    domain = domain.lower().strip()
    if domain.startswith('www.'):
        domain = domain[4:]
        
    source = db.query(Source).filter(Source.domain == domain).first()
    if not source:
        raise HTTPException(status_code=404, detail=f"Source with domain {domain} not found")
    
    return SourceResponse.from_orm(source)

@router.get("/methodology")
def get_methodology():
    """
    Get information about the methodology used for bias and sentiment analysis.
    """
    return {
        "bias_methodology": {
            "description": "We categorize news sources on a political spectrum from Left to Right based on AllSides Media Bias Ratings, a widely respected methodology.",
            "categories": [
                {"name": "left", "description": "Sources with a strong liberal bias"},
                {"name": "lean_left", "description": "Sources with a moderate liberal bias"},
                {"name": "center", "description": "Sources with minimal partisan bias"},
                {"name": "lean_right", "description": "Sources with a moderate conservative bias"},
                {"name": "right", "description": "Sources with a strong conservative bias"},
                {"name": "unknown", "description": "Sources with an undetermined bias"}
            ],
            "reference": "https://www.allsides.com/media-bias/media-bias-ratings"
        },
        "sentiment_methodology": {
            "description": "Our sentiment analysis uses natural language processing to determine if an article is bullish (positive), bearish (negative), or neutral about a stock.",
            "categories": [
                {"name": "bullish", "description": "Positive sentiment towards the stock"},
                {"name": "bearish", "description": "Negative sentiment towards the stock"},
                {"name": "neutral", "description": "Neutral or balanced sentiment towards the stock"}
            ],
            "model": "FinBERT or similar financial sentiment analysis model"
        }
    }
