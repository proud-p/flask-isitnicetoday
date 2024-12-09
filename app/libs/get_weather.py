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

def get_weather_forecast(city="london"):
    response = requests.get(f"http://api.weatherapi.com/v1/forecast.json",
                    params={
                        "key": weather_key,
                        "q": city,
                        "aqi": "no"
                    })
    weather = response.json()

    return weather

def weather_hour_pandas(city="london"):
    weather_forecast = get_weather_forecast(city)
    weather_hour = [[e["time"],e["condition"]["text"]] for e in weather["forecast"]["forecastday"][0]["hour"]]

    return pd.DataFrame(weather_hour,columns=["datetime","weather"])




if __name__ == "__main__":
    import pprint

    os.chdir("../")
    weather_key = os.getenv("WEATHER_KEY")

    weather = get_weather_current(weather_key)
    pprint.pprint(weather)