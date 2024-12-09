import dotenv
import requests
import os


# load env from root 
dotenv.load_dotenv("../.env")

def get_places(events_list_string,longitude="85.137566",latitude="25.594095" ):
    events_list = events_list_string.split(",")
    
    all_places_dict = []
    for event_type in events_list:
        places = get_places_event(event_type,longitude,latitude)
        all_places_dict.append({event_type:places})

    return all_places_dict



def get_places_event(event,longitude,latitude):
    # Your API key
    api_key = os.getenv("GOOGLE_PLACES_KEY")

    # Define the endpoint
    endpoint_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

    # Parameters for the request
    params = {
    'location': f'{latitude},{longitude}',  # Latitude and longitude 
    'radius': 50000,                  # Radius in meters
    'type': event,            # Type of place (e.g., restaurant, cafe, etc.) 
                                        #  https://developers.google.com/maps/documentation/places/web-service/supported_types
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
        
        return places
    else:
        print("Error:", response.status_code, response.text)

if __name__ == "__main__":

    get_places('park,art_gallery,zoo')
