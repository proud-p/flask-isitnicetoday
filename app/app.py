import os
from flask import *
import requests
import dotenv
import os
# import libs.get_places as places
import libs.get_weather as weather
from geopy.geocoders import Nominatim
import libs.chatgpt as chatgpt
from openai import AzureOpenAI
from libs.chatgpt import response_from_weather

app = Flask(__name__)

dotenv.load_dotenv()

# Your API key
google_places_key = os.getenv("GOOGLE_PLACES_KEY")
weather_key = os.getenv("WEATHER_KEY")

# Define the endpoint
endpoint_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

@app.route("/location", methods=["POST"])
def index_location():
    data = request.get_json()
    latitude = float(data.get('latitude'))
    longitude = float(data.get('longitude'))

    # initialize Nominatim API 
    geolocator = Nominatim(user_agent="isitnicetoday")
    location = geolocator.reverse(str(latitude)+","+str(longitude))
    city = location.raw["address"]["city"]
    country = location.raw["address"]["country"]

    # get weather
    
    current_weather = weather.get_weather_current(weather_key,city)

    # Return JSON response with weather data
    return jsonify({'weather': current_weather,
                    'redirect': f'/results?country={country}&city={city}&lat={latitude}&lon={longitude}'})

@app.route("/", methods=["GET"])
def index():
    # initial landing page hit
    return render_template("index.html")

@app.route("/results")
def results():
    city = request.args.get('city')
    country = request.args.get('country')
    lat = request.args.get('lat')
    lon = request.args.get('lon')
  
    if not all([city, lat, lon]):
        return redirect(url_for('index'))
        
    current_weather = weather.get_weather_current(weather_key, city)
    # places_near_me = places.get_places(lon,lat)
    # print(places_near_me)

    # FIXME forecast weather not current weather
    #   chatgpt
    AZURE_CLIENT = AzureOpenAI(
            api_key=os.getenv("AZURE_KEY"),
            azure_endpoint=os.getenv("AZURE_ENDPOINT"),
            api_version="2023-10-01-preview"

        )
    
    # FIXME dont do this in main do it in chatgpt then just import the entire thing
    # chat_weather_response = chatgpt.response_from_weather(client = AZURE_CLIENT, weather=current_weather,)

    response = response_from_weather(AZURE_CLIENT,latitude=lat,longitude=lon)

    return render_template(
        "results.html",
        city=city,
        country=country,
        weather=current_weather,
        coordinates={'lat': lat, 'lon': lon},
        response =response
    )

# TODO integrate chatgpt 2
# TODO integrate dallee 3
# TODO integrate netflix and whatnot 4
# TODO integrate places 1


if __name__ == "__main__":
    app.run(debug=True)