"""
Script to seed initial data into the database.
"""
import sys
import os
from pathlib import Path

# Add the parent directory to sys.path
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.models import Source
from app.models.schemas import BiasCategory

# Initial sources with bias ratings based on AllSides
INITIAL_SOURCES = [
    {"name": "CNN", "domain": "cnn.com", "bias_rating": BiasCategory.LEFT, "reference_url": "https://www.allsides.com/news-source/cnn-media-bias"},
    {"name": "New York Times", "domain": "nytimes.com", "bias_rating": BiasCategory.LEAN_LEFT, "reference_url": "https://www.allsides.com/news-source/new-york-times"},
    {"name": "Washington Post", "domain": "washingtonpost.com", "bias_rating": BiasCategory.LEAN_LEFT, "reference_url": "https://www.allsides.com/news-source/washington-post-media-bias"},
    {"name": "MSNBC", "domain": "msnbc.com", "bias_rating": BiasCategory.LEFT, "reference_url": "https://www.allsides.com/news-source/msnbc"},
    {"name": "HuffPost", "domain": "huffpost.com", "bias_rating": BiasCategory.LEFT, "reference_url": "https://www.allsides.com/news-source/huffpost-media-bias"},
    {"name": "Vox", "domain": "vox.com", "bias_rating": BiasCategory.LEFT, "reference_url": "https://www.allsides.com/news-source/vox-news-media-bias"},
    {"name": "Bloomberg", "domain": "bloomberg.com", "bias_rating": BiasCategory.LEAN_LEFT, "reference_url": "https://www.allsides.com/news-source/bloomberg"},
    {"name": "CNBC", "domain": "cnbc.com", "bias_rating": BiasCategory.CENTER, "reference_url": "https://www.allsides.com/news-source/cnbc-media-bias"},
    {"name": "Reuters", "domain": "reuters.com", "bias_rating": BiasCategory.CENTER, "reference_url": "https://www.allsides.com/news-source/reuters"},
    {"name": "Associated Press", "domain": "apnews.com", "bias_rating": BiasCategory.CENTER, "reference_url": "https://www.allsides.com/news-source/associated-press-media-bias"},
    {"name": "Financial Times", "domain": "ft.com", "bias_rating": BiasCategory.CENTER, "reference_url": "https://www.allsides.com/news-source/financial-times-media-bias"},
    {"name": "The Hill", "domain": "thehill.com", "bias_rating": BiasCategory.CENTER, "reference_url": "https://www.allsides.com/news-source/hill-media-bias"},
    {"name": "Wall Street Journal", "domain": "wsj.com", "bias_rating": BiasCategory.LEAN_RIGHT, "reference_url": "https://www.allsides.com/news-source/wall-street-journal-media-bias"},
    {"name": "Fox Business", "domain": "foxbusiness.com", "bias_rating": BiasCategory.LEAN_RIGHT, "reference_url": "https://www.allsides.com/news-source/fox-business"},
    {"name": "Fox News", "domain": "foxnews.com", "bias_rating": BiasCategory.RIGHT, "reference_url": "https://www.allsides.com/news-source/fox-news-media-bias"},
    {"name": "New York Post", "domain": "nypost.com", "bias_rating": BiasCategory.LEAN_RIGHT, "reference_url": "https://www.allsides.com/news-source/new-york-post"},
    {"name": "The Epoch Times", "domain": "theepochtimes.com", "bias_rating": BiasCategory.RIGHT, "reference_url": "https://www.allsides.com/news-source/epoch-times-media-bias"},
    {"name": "Breitbart News", "domain": "breitbart.com", "bias_rating": BiasCategory.RIGHT, "reference_url": "https://www.allsides.com/news-source/breitbart"},
    {"name": "Business Insider", "domain": "businessinsider.com", "bias_rating": BiasCategory.LEAN_LEFT, "reference_url": "https://www.allsides.com/news-source/business-insider"},
    {"name": "Yahoo Finance", "domain": "finance.yahoo.com", "bias_rating": BiasCategory.CENTER, "reference_url": "https://www.allsides.com/news-source/yahoo-news-media-bias"},
    {"name": "MarketWatch", "domain": "marketwatch.com", "bias_rating": BiasCategory.CENTER, "reference_url": "https://www.allsides.com/news-source/marketwatch-media-bias"},
    {"name": "Seeking Alpha", "domain": "seekingalpha.com", "bias_rating": BiasCategory.CENTER, "reference_url": None},
    {"name": "Benzinga", "domain": "benzinga.com", "bias_rating": BiasCategory.CENTER, "reference_url": None},
    {"name": "Motley Fool", "domain": "fool.com", "bias_rating": BiasCategory.CENTER, "reference_url": None},
    {"name": "Investor's Business Daily", "domain": "investors.com", "bias_rating": BiasCategory.LEAN_RIGHT, "reference_url": "https://www.allsides.com/news-source/investors-business-daily-media-bias"},
]

def seed_sources(db: Session):
    """Seed initial sources into the database."""
    for source_data in INITIAL_SOURCES:
        # Check if source already exists
        existing_source = db.query(Source).filter(Source.domain == source_data["domain"]).first()
        if not existing_source:
            source = Source(**source_data)
            db.add(source)
    
    db.commit()
    print(f"Added {len(INITIAL_SOURCES)} initial sources to the database.")

def main():
    """Main function to seed the database."""
    db = SessionLocal()
    try:
        seed_sources(db)
    finally:
        db.close()

if __name__ == "__main__":
    main()
