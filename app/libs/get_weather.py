import requests
import os
import urllib
import json
import pandas as pd



def get_weather_current(weather_key,city="london"):

    response = requests.get(f"http://api.weatherapi.com/v1/current.json",
                    params={
                        "key": weather_key,
                        "q": city,
                        "aqi": "no"
                    })
    weather = response.json()


    return weather["current"]["condition"]["text"]

def get_weather_forecast(weather_key,city="london"):
    response = requests.get(f"http://api.weatherapi.com/v1/forecast.json",
                    params={
                        "key": weather_key,
                        "q": city,
                        "aqi": "no"
                    })
    weather = response.json()

    return weather

def weather_hour_pandas(weather_key,city="london"):
    weather_forecast = get_weather_forecast(weather_key,city)
    weather_hour = [[e["time"],e["condition"]["text"]] for e in weather_forecast["forecast"]["forecastday"][0]["hour"]]

    return pd.DataFrame(weather_hour,columns=["datetime","weather"])


def weather_hour_string(weather_key, city="london"):
    # Get weather forecast data
    weather_forecast = get_weather_forecast(weather_key, city)
    # Extract hourly weather data
    weather_hour_data = [
        [e["time"], e["condition"]["text"]]
        for e in weather_forecast["forecast"]["forecastday"][0]["hour"]
    ]
    # Format the data into a readable string
    formatted_weather = "\n".join(
        [f"{time.split(' ')[1]}: {condition}" for time, condition in weather_hour_data]
    )

    # Return the formatted string for ChatGPT
    return f"The hourly weather forecast for {city.capitalize()} is:\n{formatted_weather}"





if __name__ == "__main__":
    import pprint

    os.chdir("../")
    weather_key = os.getenv("WEATHER_KEY")

    weather = get_weather_forecast(weather_key)
    pprint.pprint(weather)