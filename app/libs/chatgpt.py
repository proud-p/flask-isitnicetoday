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
                        "description": "The streaming service to filter movies (e.g., 'Netflix', 'Hulu'), return one of these only: 'netflix','prime','disney','apple','crunchyroll','mubi','hayu'."
                    },
                    "genre": {
                        "type": "string",
                        "description": "Optional genre filter for movies. The genre returned should strictly be one of the following: ['action', 'animation', 'comedy', 'crime', 'documentary', 'drama', 'fantasy', 'horror', 'history', 'music', 'romance', 'science-fiction', 'sport', 'thriller', 'war', 'western', 'family', 'reality tv', 'adventure', 'biography', 'news', 'reality', 'short', 'soap', 'talk show'].",
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
                    }
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
    },
    {
        "type": "function",
        "function": {
            "name": "get_place_and_movie",
            "description": "Combine the functionality of getting a movie list and places for a day when the weather alternates between nice and rainy. For example, watch a movie in the morning and go out later in the day.",
            "parameters": {
                "type": "object",
                "properties": {
                    "service": {
                        "type": "string",
                        "description": "The streaming service to filter movies. Only these services are allowed: 'netflix','prime','disney','apple','crunchyroll','mubi','hayu'."
                    },
                    "genre": {
                        "type": "string",
                        "description": "Optional genre filter for movies. The genre returned should strictly be one of the following: ['action', 'animation', 'comedy', 'crime', 'documentary', 'drama', 'fantasy', 'horror', 'history', 'music', 'romance', 'science-fiction', 'sport', 'thriller', 'war', 'western', 'family', 'reality tv', 'adventure', 'biography', 'news', 'reality', 'short', 'soap', 'talk show'].",
                        "nullable": True
                    },
                    "release_year_from": {
                        "type": "integer",
                        "description": "Optional start year for filtering movies by release year, format YYYY.",
                        "nullable": True
                    },
                    "release_year_until": {
                        "type": "integer",
                        "description": "Optional end year for filtering movies by release year, format YYYY.",
                        "nullable":  True
                    },
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
                "required": ["service", "events_list"]
            }
        }
    }
]



# Convert user's question into a GraphQL query string
def response_from_weather(weather):
    messages = [
            {
        "role": "system",
        "content": "You are a helpful assistant that suggests activities based on the weather. Your primary task is to evaluate a list of hourly weather data for a day and suggest plans accordingly. Keep your responses concise and ensure all tools are called appropriately to fetch the required information. Here's how to proceed:\n\n1. **Sunny Weather:**\n   - Recommend outdoor activities using the `get_places` function. Choose an activity type from this list:\n     ['art_gallery', 'aquarium', 'bakery', 'book_store', 'cafe', 'museum', 'park', 'restaurant', 'shopping_mall', 'spa', 'tourist_attraction', 'zoo'].\n   - Use the tool call to query nearby places.\n\n2. **Rainy Weather:**\n   - Suggest cozy indoor activities like watching a movie. Use the `get_movie_list` function to recommend a movie based on genre and streaming service. Choose one genre from this list:\n     ['action', 'animation', 'comedy', 'crime', 'documentary', 'drama', 'fantasy', 'horror', 'history', 'music', 'romance', 'science-fiction', 'sport', 'thriller', 'war', 'western', 'family', 'reality tv', 'adventure', 'biography', 'news', 'reality', 'short', 'soap', 'talk show'].\n   - Ensure release year filters span at least 10 years starting from 1920.\n\n3. **Mixed Weather (Good then Bad or Vice Versa):**\n   - Call the `get_place_and_movie` function to combine an outdoor activity and a movie suggestion. Ensure parameters for both movies and places are included in the tool call.\n\nYour output must prioritize structured, informative tool calls to fetch the required data, avoiding verbose messages. The response will be passed into the next processing step for user formatting.\n\nFocus on accuracy and ensuring the tool calls are correct."
    }
    ,
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


    response_from_weather("rainy then sun")
