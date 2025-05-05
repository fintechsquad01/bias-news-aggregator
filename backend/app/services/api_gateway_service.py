import httpx
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

async def make_external_api_call(url: str, params: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
    """
    Makes an asynchronous GET request to an external API endpoint.
    
    Args:
        url (str): The URL to make the request to
        params (Optional[Dict[str, Any]]): Optional query parameters for the request
        
    Returns:
        Optional[Dict[str, Any]]: The JSON response if successful, None if the request fails
        
    Raises:
        httpx.HTTPError: If there's an HTTP-related error
        ValueError: If the response is not valid JSON
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            response.raise_for_status()  # Raises an exception for 4XX/5XX responses
            return response.json()
            
    except httpx.HTTPError as e:
        logger.error(f"HTTP error occurred while calling {url}: {str(e)}")
        raise
    except ValueError as e:
        logger.error(f"Invalid JSON response from {url}: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error while calling {url}: {str(e)}")
        raise 