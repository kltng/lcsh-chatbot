"""
LCSH API Module - Handles interactions with the LCSH API
"""
import requests
import json
from typing import List, Dict, Any, Union

class LCSHApi:
    """
    Client for interacting with the LCSH API
    """
    def __init__(self, base_url: str = "https://lcsh.098484.xyz"):
        self.base_url = base_url
        self.recommend_endpoint = f"{self.base_url}/recommend"
    
    def get_recommendations(self, terms: Union[List[str], str]) -> Dict[str, Any]:
        """
        Get LCSH recommendations for the given terms
        
        Args:
            terms: A single term or list of terms to get recommendations for
            
        Returns:
            Dictionary containing the recommendations
        """
        try:
            payload = {"terms": terms}
            response = requests.post(self.recommend_endpoint, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            # Handle API errors gracefully
            return {
                "error": str(e),
                "recommendations": []
            } 