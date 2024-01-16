# getweatherAPI.py

import requests
import json

def get_weather_data():
    try:
        latitude = 52.4159
        longitude = 4.8332
        timezone = 'Europe/Berlin'

        # Make the HTTP request
        url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&timezone={timezone}&current_weather=true"
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Extract the JSON content from the response
            weather_data = response.json()
            return weather_data
        else:
            print(f"Error fetching weather data from API. Status code: {response.status_code}")
            return {}

    except Exception as e:
        print(f"Error fetching weather data from API: {e}")
        return {}

if __name__ == "__main__":
    # Get weather data
    weather_data = get_weather_data()

    # Print the weather data (for debugging purposes)
    print(json.dumps(weather_data, indent=2))
