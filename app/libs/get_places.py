import dotenv
import requests
import os


# load env from root 
dotenv.load_dotenv("../.env")

def get_places(events_list,longitude="85.137566",latitude="25.594095" ,skip_opened=False):
    events_list = events_list.split(",")
    
    all_places_dict = []
    for event_type in events_list:
        places = get_places_event(event_type,longitude,latitude)
        all_places_dict.append({event_type:places})

    extracted_recommended_places = extract_recommended_places(all_places_dict)
    formatted_recommended_places = format_recommendations(extracted_recommended_places,skip_opened)

    return formatted_recommended_places



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
        # for place in places:
        #     name = place.get('name')
        #     address = place.get('vicinity')
        #     print(f"Name: {name}, Address: {address}")
        
        return places
    else:
        print("Error:", response.status_code, response.text)


def extract_recommended_places_one(function_response):
    recommendations = {}
    for event in function_response:
        for category, places in event.items():
            # Extract the first operational place (or the highest-rated one)
            recommended_place = next(
                (place for place in places if place["business_status"] == "OPERATIONAL"),
                None
            )
            if recommended_place:
                recommendations[category] = {
                    "name": recommended_place["name"],
                    "rating": recommended_place.get("rating"),
                    "vicinity": recommended_place.get("vicinity"),
                    "photo": recommended_place.get("photos", [{}])[0].get("photo_reference"),
                    "opening_hours": recommended_place.get("opening_hours", {}).get("open_now")
                }
    return recommendations

def extract_recommended_places(function_response):
    recommendations = {}
    for event in function_response:
        for category, places in event.items():
            # Filter operational places and sort by rating
            operational_places = [
                place for place in places 
                if place["business_status"] == "OPERATIONAL"
            ]
            # Sort by rating (highest first) and take top 5
            top_places = sorted(
                operational_places, 
                key=lambda x: x.get("rating", 0), 
                reverse=True
            )[:5]
            
            if top_places:
                recommendations[category] = []
                for place in top_places:
                    recommendations[category].append({
                        "name": place["name"],
                        "rating": place.get("rating"),
                        "vicinity": place.get("vicinity"),
                        "photo": place.get("photos", [{}])[0].get("photo_reference"),
                        "opening_hours": place.get("opening_hours", {}).get("open_now")
                    })
    return recommendations


def format_recommendations(recommendations, filter_open=False):
    """
    Formats the recommendations into a readable text format.

    Args:
        recommendations (dict): A dictionary containing recommended places with details.
        filter_open (bool): If True, filters out places that are not currently open.

    Returns:
        str: A formatted string of recommendations.
    """
    formatted = []
    for category,places in recommendations.items():
        # list of places, format detail for each place
        for details in places:  
            # Filter for open places if filter_open is True
            if filter_open and not details.get("opening_hours"):
                continue  # Skip places that are not open

            recommendation_text = (
                f"{category.capitalize()} Recommendation:\n"
                f"Name: {details['name']}\n"
                f"Rating: {details['rating']} ⭐\n"
                f"Vicinity: {details['vicinity']}\n"
            )
            if details.get("photo"):
                recommendation_text += f"Photo: {details['photo']}\n"
            if details.get("opening_hours") is not None:
                recommendation_text += (
                    "Currently Open: Yes\n" if details["opening_hours"] else "Currently Open: No\n"
                )
            formatted.append(recommendation_text)
    
    return "\n".join(formatted)


if __name__ == "__main__":

    response = get_places('park,cafe,zoo',longitude=-0.1021067,latitude=51.5244376)

    print(response) 