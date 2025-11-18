"""Extract names of accommodations/properties mentioned in a blog post using an LLM.
    Just a placeholder for demonstration, not actually implemented yet"""

from typing import List, Dict



class AccommodationExtractor:
    """Extracts names of accommodations/properties mentioned in a blog post"""
    
    def __init__(self):
        """
        Initialize the property extractor.

        """

    def extract_accommodations(self, text: str) -> List[Dict[str, str]]:
        """
        Extract accommodation properties from text using mock LLM.
        
        Args:
            text: The blog post text to analyze.
            
        Returns:
            List of dictionaries with 'name' and 'location' keys.
        """
        # Demo implementation in the future this willcall an LLM
        # For this demo it return the properties mentioned in the sample blog post
        mock_properties = [
            {"name": "Central Hotel", "location": "Donegal, Ireland"},
            {"name": "Harvey's Point Hotel", "location": "Donegal, Ireland"},
            {"name": "Slieve League B&B", "location": "Donegal, Ireland"},
        ]
    
        return mock_properties
    
