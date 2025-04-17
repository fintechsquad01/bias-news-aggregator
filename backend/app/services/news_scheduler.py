import asyncio
import logging
import schedule
import time
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.session import SessionLocal
from app.services.news_processor import NewsProcessor
from app.core.config import settings

logger = logging.getLogger(__name__)

class NewsScheduler:
    """Scheduler for periodically fetching news."""
    
    def __init__(self):
        self.default_tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]
        self.fetch_interval_minutes = settings.NEWS_FETCH_INTERVAL_MINUTES
        
    def start(self):
        """Start the scheduler."""
        logger.info(f"Starting news scheduler with {self.fetch_interval_minutes} minute interval")
        
        # Schedule the job
        schedule.every(self.fetch_interval_minutes).minutes.do(self.fetch_news_job)
        
        # Run the job immediately on startup
        self.fetch_news_job()
        
        # Keep the scheduler running
        while True:
            schedule.run_pending()
            time.sleep(1)
            
    def fetch_news_job(self):
        """Job to fetch news for all tickers."""
        logger.info("Running scheduled news fetch job")
        
        # Get tickers to fetch (in a real implementation, this would include user watchlists)
        tickers = self.get_tickers_to_fetch()
        
        # Create a new database session
        db = SessionLocal()
        try:
            # Create news processor
            processor = NewsProcessor(db)
            
            # Run the async fetch in the event loop
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            for ticker in tickers:
                try:
                    # Fetch and process news for each ticker
                    articles = loop.run_until_complete(processor.fetch_and_process_news(ticker))
                    logger.info(f"Fetched {len(articles)} new articles for {ticker}")
                    
                    # Add delay between tickers to avoid rate limits
                    time.sleep(1)
                except Exception as e:
                    logger.error(f"Error fetching news for {ticker}: {str(e)}")
            
            loop.close()
            
        except Exception as e:
            logger.error(f"Error in news fetch job: {str(e)}")
        finally:
            db.close()
            
        logger.info("Completed scheduled news fetch job")
        
    def get_tickers_to_fetch(self) -> List[str]:
        """
        Get list of tickers to fetch news for.
        In a real implementation, this would include user watchlists.
        """
        # For now, just return the default tickers
        return self.default_tickers

# Function to run the scheduler
def run_scheduler():
    """Run the news scheduler."""
    scheduler = NewsScheduler()
    scheduler.start()

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    
    # Run the scheduler
    run_scheduler()
