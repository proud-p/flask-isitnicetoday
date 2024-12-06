from flask import *
import requests
import dotenv
import os
import libs.get_places as place

app = Flask(__name__)

dotenv.load_dotenv()

# Your API key
api_key = os.getenv("GOOGLE_PLACES_KEY")

# Define the endpoint
endpoint_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"



@app.route("/location", methods=["POST"])
def index_location():
    print("JUST CHECKING")
    data = request.get_json()
    latitude = float(data.get('latitude'))
    longitude = float(data.get('longitude'))
    print(latitude,longitude)
    print(type(latitude))
    print(type(longitude))

    place.get_places(longitude=longitude,latitude=latitude)

    return render_template("index.html")
        
@app.route("/", methods=["GET","POST"])
def index():
    return render_template("index.html")

# TODO and disney plus - filter by area
# TODO connect to weather API

if __name__ == "__main__":
    app.run(debug=True)