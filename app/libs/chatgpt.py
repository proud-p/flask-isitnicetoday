from openai import AzureOpenAI
import os
from dotenv import load_dotenv
import json
import requests


functions = 


# Convert user's question into a GraphQL query string
def response_from_weather(weather):
    messages = [
        {
            "role": "system",
            "content": """ you are a cute little cloud, albeit a little savage and british. you are a helper, you will be given a list of weather per hour for the day. Your job is to suggest to the user what to do that day based on that weather. be a chill day, but if it is sunny like get them to go outside and try new things. if it's rainy then suggest they stay home cozy and watch tv, suggest a genre and a streaming site. make it cute.

            for going outside, return a thing to do, like a gallery or whatever and a cafe/ restaurant. like structure the day, but chill day so don't like pack it in. 
                    """
        },
        {"role": "user", "content": weather}
    ]

    response = AZURE_CLIENT.chat.completions.create(
        model="GPT-4",
        messages=messages
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

    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

    response_from_weather("sunny all day")
