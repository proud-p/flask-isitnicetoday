from openai import AzureOpenAI
import os
from dotenv import load_dotenv
import json
import requests


def return_first_functions():
    return [
        {
            "type": "function",
            "function": {
                "name": "get_movie_list",
                "description": "Retrieve a list of movies based on country, streaming service, and optional filters like genre and release year.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "service": {
                            "type": "string",
                            "description": "The streaming service to filter movies (e.g., 'Netflix', 'Hulu')."
                        },
                        "genre": {
                            "type": "string",
                            "description": "Optional genre filter for movies (e.g., 'Action', 'Comedy').",
                            "nullable": True
                        },
                        "release_year_from": {
                            "type": "integer",
                            "description": "Optional start year for filtering movies by release year.",
                            "nullable": True
                        },
                        "release_year_until": {
                            "type": "integer",
                            "description": "Optional end year for filtering movies by release year.",
                            "nullable": True
                        },
                    },
                    "required": ["service"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_places",
                "description": "Retrieve a list of places near a given location based on longitude and latitude.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "events_list": {
                            "type": "number",
                            "description": (
                                "A single comma-separated string listing the types of places to fetch for that day. For example, 'cafe,art_gallery'. "
                                "All events should be from the following options: "
                                "['art_gallery', 'bakery', 'book_store', 'cafe', 'museum', 'park', 'restaurant', "
                                "'shopping_mall', 'spa', 'tourist_attraction', 'zoo']."
                            )
                        }
                    },
                    "required": ["events_list"]
                }
            }
        }
    ]




# Convert user's question into a GraphQL query string
def response_from_weather(weather):
    messages = [
        {
            "role": "system",
            "content": """ you are a cute little cloud, albeit a little savage and british. you are a helper, you will be given a list of weather per hour for the day. Your job is to suggest to the user what to do that day based on that weather. be a chill day, but if it is sunny like get them to go outside and try new things. if it's rainy then suggest they stay home cozy and watch tv, suggest a genre and a streaming site. make it cute.

            for going outside, return a thing to do, like a gallery or whatever and a cafe/ restaurant. like structure the day, but chill day so don't like pack it in. 

            if it's sunny, call the places api to like get the list of possible places you can go to in reality, you have to give it like what kinda activity you want , choose from one of these types which will be used to query the google places api: [
            "art_gallery",
            "aquarium",
            "bakery",
            "book_store",
            "cafe",
            "museum",
            "park",
            "restaurant",
            "shopping_mall",
            "spa",
            "tourist_attraction",
            "zoo"
            ]

            if weather is bad, then like get tell the user to stay home and watch something. i have a function to query movies, so like maybe do something like, oh let's watch scifi, or like let's watch old romance drama cause it's rainy today. whatever get creative. these are all the possible genres, return one of them, return just the key:     'action': 'act',
        'animation': 'ani',
        'comedy': 'cmy',
        'crime': 'crm',
        'documentary': 'doc',
        'drama': 'drm',
        'fantasy': 'fnt',
        'horror': 'hrr',
        'history': 'hst',
        'music': 'msc',
        'romance': 'rma',
        'science-fiction': 'scf',
        'sport': 'spt',
        'thriller': 'trl',
        'war': 'war',
        'western': 'wsn',
        'family': 'fml',
        'reality tv': 'rly',
        'adventure': 'adv',
        'biography': 'bio',
        'news': 'nws',
        'reality': 'rly',
        'short': 'shr',
        'soap': 'sof',
        'talk show': 'tlv'

        if you want to return date period to query, it has to be after 1920 and in this format YYYY


                    """
        },
        {"role": "user", "content": weather}
    ]

    functions = return_first_functions()

    response = AZURE_CLIENT.chat.completions.create(
        model="GPT-4",
        messages=messages,
        tools=functions,
        tool_choice="auto"
    )

    # Debugging response
    print("Response from Azure OpenAI:", response)


# TODO response from weather fetch api
# TODO get justwatch, return description and info
# TODO integrate response with text to return
# TODO integrate with google places
# TODO function tools



if __name__ == "__main__":
    os.chdir("../")
    # Load environment variables
    load_dotenv()

    # Global variables
    AZURE_CLIENT = AzureOpenAI(
        api_key=os.getenv("AZURE_KEY"),
        azure_endpoint=os.getenv("AZURE_ENDPOINT"),
        api_version="2023-10-01-preview"
    )


    response_from_weather("rainy all day")
