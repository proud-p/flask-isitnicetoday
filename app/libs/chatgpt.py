
import sys
import os




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
                            "type": "string",
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
                            "nullable": True
                        },
                        "events_list": {
                            "type": "string",
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
# FIXME collapse the loc stuff into one
def response_from_weather(AZURE_CLIENT, weather,city,latitude,longitude,country):
    messages = [
            {
    "role": "system",
    "content": "You are a helpful assistant that suggests activities based on the weather. Your primary task is to evaluate a list of hourly weather data for a day and suggest plans accordingly. Keep your responses concise and ensure all tools are called appropriately to fetch the required information. Here's how to proceed:\n\n1. **Sunny Weather:**\n   - Recommend outdoor activities using the `get_places` function. Choose an activity type from this list:\n     ['art_gallery', 'aquarium', 'bakery', 'book_store', 'cafe', 'museum', 'park', 'restaurant', 'shopping_mall', 'spa', 'tourist_attraction', 'zoo'].\n   - Use the tool call to query nearby places.\n\n2. **Rainy Weather:**\n   - Suggest cozy indoor activities like watching a movie. Use the `get_movie_list` function to recommend a movie based on genre and streaming service. Choose one genre from this list:\n     ['action', 'animation', 'comedy', 'crime', 'documentary', 'drama', 'fantasy', 'horror', 'history', 'music', 'romance', 'science-fiction', 'sport', 'thriller', 'war', 'western', 'family', 'reality tv', 'adventure', 'biography', 'news', 'reality', 'short', 'soap', 'talk show'].\n   - Ensure release year filters span at least 10 years starting from 1920.\n\n3. **Mixed Weather (Good then Bad or Vice Versa):**\n   - Call the `get_place_and_movie` function to combine an outdoor activity and a movie suggestion. Ensure parameters for both movies and places are included in the tool call.\n\nYour output must prioritize structured, informative tool calls to fetch the required data, avoiding verbose messages. The response will be passed into the next processing step for user formatting.\n\nFocus on accuracy and ensuring the tool calls are correct. YOU MUST CALL AT LEAST 1 FUNCTION"
    }
    ,
        {"role": "user", "content": weather}
        # TODO add available streaming services
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

    gpt_tools = response.choices[0].message.tool_calls

    print("GPT TOOLS"+"-"*20)
    print(gpt_tools)

    # FIXME is there a better way to do this?
    available_functions = {
        "get_places": {
            "function": places.get_places,  # The actual function to call
            "chatgpt_params": ["events_list"],  # Parameters expected from ChatGPT's tool call
            "additional_params": {  # Default or extra parameters to pass
                "longitude": longitude,
                "latitude": latitude,
                "skip_opened": False
            }
        },
        "get_movie_list": {
            "function": justwatch.get_movie_list,
            "chatgpt_params": [ "service", "genre", "release_year_from", "release_year_until"],
            "additional_params": { 
                "country": country, # Defaults if not provided
                "headless": True
            }
        }
    }


    if gpt_tools:

        for gpt_tool in gpt_tools:
            function_name = gpt_tool.function.name
            function_to_call = available_functions[function_name]["function"]
            function_parameters = json.loads(gpt_tool.function.arguments)

            print("FUNCTION PARAMETERS:")
            print(function_parameters)

            # Call the function
            # Dynamically construct kwargs for the function call
            kwargs = {
                k: function_parameters.get(k, available_functions[function_name]["additional_params"].get(k))
                for k in available_functions[function_name]["chatgpt_params"]
            }
            kwargs.update(available_functions[function_name]["additional_params"])

            # call function
            function_response = function_to_call(**kwargs)

            # # Add the function response to the messages
      
            final_messages = []
            final_messages.append({
                "role": "system",
                "content": (
                    f"You are a playful and charming cloud friend with a casual and witty tone. Based on the input weather, "
                    
                )
            })

            if gpt_tool == "get_places" or "get_place_and_movie" :
                final_messages.append({
                    "role": "system",
                    "content": (
                        f"You've just called {gpt_tool} with {kwargs} parameters. the Event list parameter is what the previous bot chose as activity types for the user to do on this {weather} day. The {gpt_tool} you called returned a list of places to you for each of the event type for you to choose from  "
                        f"help the user pick from the recommendations and explain why they should visit these places. Don't pick too many things, we want to give them a chill day.  Prioritise picking things that are currently opened. Here are the recommendations: "
                        f"{function_response}. For each recommendation, provide details such as the opening hours, rating, and a short description."
                        f"Add a fun and conversational comment about these details, making your response engaging and delightful."
                        f"Focus on being helpful and conversational—no need to call any functions, just respond with a friendly and detailed message! Phrase it like you are planning out the chill day for them from morning till evening. Put lots of emoji in as well for cuteness and format the response into paragraphs nicely"
                    )
                })

            if gpt_tool == "get_movie_list" or gpt_tool == "get_place_and_movie":
                final_messages.append({
                    "role": "system",
                    "content": (
                        f"You've just called {gpt_tool} with the parameters {kwargs}. The service parameter refers to the streaming service the user has access to, "
                        f"while the genre, release year range, and other details provide filters to match the user's preferences. Your previous instance chose these parameters because you thought it matches the weather. The {gpt_tool} you called returned a list of movies matching those criterias "
                        f"Help the user choose from the recommendations and explain why they should watch a particular movie.  "
                        f"Here are the movie recommendations: {function_response}. For each movie, provide details such as the title, genre, release year, and streaming service it is available on. "
                        f"Add a fun and conversational comment about the movie's plot, cast, or general vibe to make the recommendation engaging. Link the genre or vibes of the movie to the weather to explain why you picked them for the user"
                        f"Focus on being witty and approachable, but also ensure your response is clear and informative. There is no need to call any functions—just respond with an engaging and detailed message! Put lots of emoji in as well for cuteness and format the response into paragraphs nicely"
                    )
                })



            final_messages.append({
                "role": "user",
                "content": f"what should I do today? The weather is {weather}, in {city}"
            })



            # Get a final response from GPT using the function's output
            second_response = AZURE_CLIENT.chat.completions.create(
                model="GPT-4",
                messages=final_messages
            )
            print("Second GPT Response:", second_response.choices[0].message)
    else:
        print(response.choices[0].message)









# TODO second chat - should be weather, list of places for chat gpt to choose from (done), film description (done)
# TODO fix kwargs args for different functions




if __name__ == "__main__":
    project_root = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, os.path.join(project_root, "app"))

    import os

    from openai import AzureOpenAI
    from dotenv import load_dotenv
    import json
    import requests
    import get_places as places
    import get_justwatch as justwatch
    import get_weather as weather

    os.chdir("../")
    # Load environment variables
    load_dotenv()

    # Global variables
    AZURE_CLIENT = AzureOpenAI(
        api_key=os.getenv("AZURE_KEY"),
        azure_endpoint=os.getenv("AZURE_ENDPOINT"),
        api_version="2023-10-01-preview"
    )

    WEATHER_KEY = os.getenv("WEATHER_KEY")

    # weather_hour = weather.weather_hour_string(WEATHER_KEY,"bangkok")
    weather_hour = weather.weather_hour_string(WEATHER_KEY,"london")


    # response = response_from_weather(AZURE_CLIENT, weather=weather_hour,latitude=25.594095,longitude=85.137566,city="bangkok",country="Thailand")

    response = response_from_weather(AZURE_CLIENT, weather=weather_hour,latitude=51.5072,longitude=0.1276,city="london",country="england")

    # TODO integrate this into main
   