import dotenv
import requests
import os

# load env from root 
dotenv.load_dotenv("../.env")



def get_places(longitude,latitude):

    # Your API key
    api_key = os.getenv("GOOGLE_PLACES_KEY")

    # Define the endpoint
    endpoint_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

    # Parameters for the request
    params = {
    'location': f'{latitude},{longitude}',  # Latitude and longitude 
    'radius': 1500,                  # Radius in meters
    'type': 'restaurant',            # Type of place (e.g., restaurant, cafe, etc.)
    'key': api_key
    }

    # Make the request
    response = requests.get(endpoint_url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        places = response.json().get('results', [])
        for place in places:
            name = place.get('name')
            address = place.get('vicinity')
            print(f"Name: {name}, Address: {address}")
    else:
        print("Error:", response.status_code, response.text)

if __name__ == "__main__":

    # get_places(34.0365,-118.2351)
