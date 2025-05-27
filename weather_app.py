import requests
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

API_KEY = os.getenv('WEATHER_API_KEY')  # Get the API key safely

def get_weather(city):
    url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}"
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200 and "current" in data:
        location = data['location']['name']
        temp_c = data['current']['temp_c']
        condition = data['current']['condition']['text']
        print(f"🌦️ Weather in {location}: {temp_c}°C, {condition}")
    else:
        error_msg = data.get('error', {}).get('message', 'Something went wrong')
        print(f"❌ Error: {error_msg}")

if __name__ == "__main__":
    city = input("Enter a city name: ")
    get_weather(city)
