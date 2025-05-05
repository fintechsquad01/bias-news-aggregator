import os
from typing import Dict, Any, Optional, List
import requests
from supabase import create_client, Client

# Initialize Supabase client
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

class BiasAnalyzer:
    """Service for analyzing and categorizing news source bias"""
    
    def __init__(self):
        # Load bias ratings from database
        self.bias_ratings = self._load_bias_ratings()
    
    def _load_bias_ratings(self) -> Dict[str, Dict[str, Any]]:
        """Load bias ratings for news sources from database"""
        try:
            response = supabase.table("news_sources").select("domain, bias_label, bias_score").execute()
            
            # Convert to dictionary for faster lookups
            ratings = {}
            for source in response.data:
                ratings[source["domain"]] = {
                    "bias_label": source["bias_label"],
                    "bias_score": source["bias_score"]
                }
            
            return ratings
        except Exception as e:
            print(f"Error loading bias ratings: {e}")
            return {}
    
    def analyze_source(self, domain: str) -> Dict[str, Any]:
        """
        Analyze the bias of a news source based on its domain
        
        Args:
            domain: The domain of the news source (e.g., "cnn.com")
            
        Returns:
            Dictionary with bias_label and bias_score
        """
        # Check if we have bias data for this domain
        if domain in self.bias_ratings:
            return self.bias_ratings[domain]
        
        # If not found, try to find a parent domain
        # E.g., if "finance.yahoo.com" is not found, try "yahoo.com"
        parts = domain.split(".")
        if len(parts) > 2:
            parent_domain = ".".join(parts[-2:])
            if parent_domain in self.bias_ratings:
                return self.bias_ratings[parent_domain]
        
        # Default to center/neutral if not found
        return {
            "bias_label": "center",
            "bias_score": 0.0
        }
    
    def refresh_bias_ratings(self):
        """Refresh the cached bias ratings from the database"""
        self.bias_ratings = self._load_bias_ratings()
    
    def get_source_id(self, domain: str) -> Optional[int]:
        """Get the database ID for a news source by domain"""
        try:
            response = supabase.table("news_sources").select("id").eq("domain", domain).execute()
            
            if response.data and len(response.data) > 0:
                return response.data[0]["id"]
            
            return None
        except Exception as e:
            print(f"Error getting source ID: {e}")
            return None
    
    def add_or_update_source(self, source_data: Dict[str, Any]) -> Optional[int]:
        """
        Add a new news source or update an existing one
        
        Args:
            source_data: Dictionary with source information
                {
                    "name": "Source Name",
                    "domain": "source.com",
                    "bias_label": "center",
                    "bias_score": 0.0,
                    "reliability_score": 0.8,
                    "logo_url": "https://...",
                    "description": "Description..."
                }
                
        Returns:
            ID of the created or updated source, or None if operation failed
        """
        try:
            # Check if source already exists
            domain = source_data.get("domain") 
            existing_id = self.get_source_id(domain)
            
            if existing_id:
                # Update existing source
                response = supabase.table("news_sources").update(source_data).eq("id", existing_id).execute()
                self.refresh_bias_ratings()
                return existing_id
            else:
                # Create new source
                response = supabase.table("news_sources").insert(source_data).execute()
                self.refresh_bias_ratings()
                
                if response.data and len(response.data) > 0:
                    return response.data[0]["id"]
            
            return None
        except Exception as e:
            print(f"Error adding/updating source: {e}")
            return None

# Create singleton instance
bias_analyzer = BiasAnalyzer()
