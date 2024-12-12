# Weather and Recommendations App

This project is a Flask-based application that provides users with weather updates and activity recommendations based on their current location. The app integrates several APIs and tools to enhance the user experience, including weather forecasts, nearby places, movie suggestions, and interactive AI-powered recommendations.

## Features

- **Weather Forecast:** Displays current and hourly weather updates for the user’s location.
- **Activity Recommendations:** Suggests activities or places to visit based on the weather conditions.
- **Movie Recommendations:** Suggests movies for cozy indoor days using the JustWatch API.
- **Interactive AI Assistant:** Provides tailored activity plans through OpenAI's Azure API integration.
- **Responsive UI:** Includes multiple Flask routes for an interactive user interface.

## Technologies Used

- **Backend Framework:** Flask
- **APIs:**
  - WeatherAPI for weather data
  - Google Places API for nearby location recommendations
  - JustWatch API for movie suggestions
- **Libraries:**
  - `requests` for API calls
  - `dotenv` for managing environment variables
  - `geopy` for geolocation processing
  - `selenium` for web scraping movie details
  - `pandas` for handling weather data
- **Frontend:** Flask templating with HTML and CSS

## File Overview

### 1. `app.py`
The main Flask application file that handles routing, API calls, and rendering HTML templates.

### 2. `libs/chatgpt.py`
Handles AI recommendations by integrating OpenAI's Azure API. Provides activity and movie recommendations based on weather conditions.

### 3. `libs/get_justwatch.py`
Scrapes movie recommendations from JustWatch using Selenium and provides details like title, image, and description.

### 4. `libs/get_places.py`
Uses the Google Places API to fetch nearby locations based on the user’s latitude and longitude. Filters and formats the data to prioritize highly-rated, operational places.

### 5. `libs/get_weather.py`
Fetches current and forecasted weather data using WeatherAPI. Formats data for easy consumption by other components.

### 6. `static`
Contains everything frontend including css, fonts, images and javascripts.

### 7. `templates`
Contains html templates for all pages.


## Installation

### Prerequisites

- Python 3.8+
- pip
- Chrome WebDriver (for Selenium)

### Keys
All keys need to be in a .env file in the root folder. Please see exact format below. Variable names need to be kept the same.

```.env
AZURE_ENDPOINT=
AZURE_KEY=
GOOGLE_PLACES_KEY=
WEATHER_KEY=
```

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/weather-recommendations.git
   cd weather-recommendations
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   - Create a `.env` file in the root directory.
   - Add the following keys:
     ```
     GOOGLE_PLACES_KEY=your_google_places_api_key
     WEATHER_KEY=your_weather_api_key
     AZURE_KEY=your_azure_openai_api_key
     AZURE_ENDPOINT=your_azure_openai_endpoint
     ```

4. Run the application:
   ```bash
   python app.py
   ```

5. Access the app at `http://127.0.0.1:5000`.

## Usage

1. Open the app in your web browser.
2. Allow location access to fetch weather and nearby places.
3. View recommendations tailored to the weather conditions in your area.
4. Explore movie suggestions for indoor days.

## Future Enhancements

- **DALL-E Integration:** Add visual elements by generating images based on weather and activity themes.
- **Additional Services:** Include more APIs like Netflix for expanded recommendations.
- **Improved UI/UX:** Enhance frontend design for a seamless user experience.
- **User Accounts and Profiles:** Allow users to customise their recommendation by allowing them to add preferences, for example: what streaming services they have, how far can they travel, their accessibility etc.
- **Optimisation:** Decrease loading time.
## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contributors

- Avika Pulges - Developer
- [OpenAI](https://openai.com) - Azure API Integration
- [JustWatch](https://www.justwatch.com) - Movie Data

## Acknowledgments

- Flask documentation
- Selenium and BeautifulSoup for web scraping
- WeatherAPI and Google Places for reliable data

