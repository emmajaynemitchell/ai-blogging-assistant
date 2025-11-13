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
