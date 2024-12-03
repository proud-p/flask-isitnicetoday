from flask import *
import requests
app = Flask(__name__)

def get_ip():
    response = requests.get('https://api64.ipify.org?format=json').json()
    return response["ip"]

def get_location():
	ip_address = get_ip()
	response = requests.get(f'https://ipapi.co/{ip_address}/json/').json()
	location_data = {
        "ip": ip_address,
        "city": response.get("city"),
        "region": response.get("region"),
    	"country": response.get("country_name")
	}
    
	print(location_data)
    
	return location_data
@app.route("/")
def home():
    data = get_location()
    return render_template("index.html",data=data)

if __name__ == "__main__":
    app.run(debug=True)