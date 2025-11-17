"""Generate a booking.com affiliate link and insert it into the blog post."""

import re
from typing import List, Dict
from urllib.parse import quote


class LinkProcessor:
    """Generates affiliate links and processes markdown to add hyperlinks."""
    
    def __init__(self, affiliate_id: str = "12345"):
        """
        Initialize the link processor.
        
        Args:
            affiliate_id: Booking.com affiliate ID
        """
        self.affiliate_id = affiliate_id
    
    def generate_affiliate_url(self, accomodation_name: str, location: str = "") -> str:
        """
        Generate a booking.com affiliate URL for a property in the format:
        "https://www.booking.com/searchresults.html?ss=<accomodation_name+location>&aid=<affiliate_id>"
        
        Args:
            accomodation_name: Name of the accommodation 
            location: Location including city and country (e.g., "Donegal, Ireland")
            
        Returns:
            Booking.com affiliate URL
        """
        # Build search string with property name and location
        search_string = accomodation_name
        if location:
            search_string = f"{accomodation_name}, {location}"
        
        # URL encode the search string
        encoded_search = quote(search_string, safe='')
        return f"https://booking.com/searchresults.html?ss={encoded_search}&aid={self.affiliate_id}"
    
    def process_markdown(self, markdown_content: str, accommodations: List[Dict[str, str]]) -> str:
        """
        Edit the markdown blog post to add hyperlinks to property names in the format:
        [Property Name](affiliate_url) .
        
        Finds the first mention of each property name (case-insensitive,
        handling variations like "The Hotel X" vs "Hotel X") and wraps it with a
        markdown hyperlink to the affiliate URL that includes location and country.
        
        Args:
            markdown_content: The markdown blog post content
            accomodations: List of dictionaries of accomodations with 'name' and 'location' keys
            
        Returns:
            Modified markdown with hyperlinks added
        """
        result = markdown_content
        # Keep track of processed property names to avoid duplicates, only want to link first mention.
        processed_properties = set()
        
        for prop in accommodations:
            prop_name = prop.get("name", "")
            prop_location = prop.get("location", "")
            
            # Skip if we've already processed this property
            if prop_name.lower() in processed_properties:
                continue
            
            # Generate the affiliate URL with location included
            url = self.generate_affiliate_url(prop_name, prop_location)
            
            # Find and replace the first mention of the property
            # Use word boundary and case-insensitive search
            # Pattern handles variations like "The Hotel X", "Hotel X", etc.
            pattern = r'\b' + re.escape(prop_name) + r'\b'
            
            # Use a flag to replace only the first occurrence
            count = 0
            def replace_func(match_obj):
                nonlocal count
                if count == 0:
                    count += 1
                    return f"[{match_obj.group()}]({url})"
                return match_obj.group()
            
            result = re.sub(pattern, replace_func, result, flags=re.IGNORECASE)
            processed_properties.add(prop_name.lower())
        
        return result
