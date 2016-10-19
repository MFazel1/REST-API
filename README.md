# REST-API
Showing the most recent photos of the location posted in Instagram by entering the name of the location and the number of pages you want to go further.

# APIs Usage
- Google Map API: In this project in order to find the geographical information (latitude and longitude) of location entered, Google Map API is used.
- Apigee: In order to show the images of location posted in Instagram we have to:
    1. Identifying the location ID by entering the latitude and longitude of the location gaining from Google API.
    2. For each location ID(most of the time, we have multiple results for specific Latitude and longitude), checks whether the name presented in Google Map is similar to what Instagram API founds.
    3. Finding recent photos by using the IDs fall into step 2.
    4. Showing the results in the web browser.


# Libraries:
- request: To do the HTTP operations.
- json: To save the results in json format
- Webbrowser: to open images
- Ctypes: to open message box

# Usage:
    python insta_google_api.py lakeplacid 5
    #check the last 5 pages of images that has taken in lake placid and open them in the web browser
