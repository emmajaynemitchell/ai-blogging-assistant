# AI Blogging Assistant 
This is a Python project aimed to improve the blogging process using AI.
It includes features to detect when accomodations options are mentioned in a text and to insert affiliate links.


## Affiliate links 
### Booking.com
Affiliate links are one of the main ways bloggers create income, a common website used for this is Booking.com, a worldwide online travel agency that allows travelers to search for and book accommodation, flights, car rentals and attractions. 
To start with this project will focus on accomodation. The tool will search for mentions of accomodation such as hotels, apartments and insert a hyperlink to Booking.com. Saving the blogger time from having to go through each blog post to find each mention of accomodation and manually inserting a hyperlink.

#### Booking.com Affiliate Partner Program
To generate revenue from affiliate links in booking.com you must sign up for the Booking.com Affiliate Partner Program. Once accepted, you'll receive an affiliate id (`aid`) and access to their link builder and documentation.  

Set the BOOKING_AID parameter in your env variables. In this project the aid is set as "12345" by default. 

The approach used here generates an affiliate link in the form 
"https://www.booking.com/searchresults.html?ss=<`extracted_accomodation_name`>&aid=`BOOKING_AID`"

## How It Works

1. Reads in the markdown file of a blog post
2. Use LLM (placeholder for now) to identify accommodation properties and their locations
3. Create booking.com affiliate URLs for each property
4. Find first mentions of properties and add the hyperlink
5. Save the modified markdown to new file with `_linked` suffix

## Example

Input blog post mentions: "The Central Hotel in Donegal..."  

Output: "The [Central Hotel](https://booking.com/searchresults.html?ss=Central+Hotel&aid=12345) in Donegal..."

# Process
## Installation

1. Clone the repository, navigate to the folder.
2. Install dependencies:  
   ```pip install -r requirements.txt```

## Running the affiliate link insertion process
Basic use with defaults:  
```python -m affiliate.cli examples/donegal_blog.md```

Output file will be created with `_linked` suffix (e.g., `donegal_blog_linked.md`)

## Testing
To test the affiliate link feature run:` 
``python -m pytest tests/affiliate_tests.py``

# TLDR
A modular Python CLI application using LangChain and HuggingFace that analyzes markdown blog posts with an LLM to identify accommodation properties, extract their names and locations, generate booking.com affiliate links, and automatically hyperlink the first mention of each property.