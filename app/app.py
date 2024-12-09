from flask import *
import requests
import dotenv
import os
import libs.get_places as place
import libs.get_weather as weather
from geopy.geocoders import Nominatim

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

    # get weather
    
    current_weather = weather.get_weather_current(weather_key,city)

    # Return JSON response with weather data
    return jsonify({'weather': current_weather})

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)