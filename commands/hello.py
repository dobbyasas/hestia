import datetime
import requests
from hestia import speak
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")
CITY = os.getenv("CITY")
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "http://api.openweathermap.org/data/2.5/forecast"

def generate_greeting():
    current_hour = datetime.datetime.now().hour
    if 5 <= current_hour < 12:
        return "Good morning, Tofi"
    elif 12 <= current_hour < 18:
        return "Good afternoon, Tofi"
    elif 18 <= current_hour < 22:
        return "Good evening, Tofi"
    else:
        return "Good night, Tofi"

def get_weather():
    try:
        url = f"{BASE_URL}?q={CITY}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()

        if data["cod"] == 200:
            weather_description = data["weather"][0]["description"]
            temperature = data["main"]["temp"]
            wind_speed = data["wind"]["speed"]
            rain_chance = data.get("rain", {}).get("1h", 0)

            weather_info = f"The weather in {CITY} is {weather_description} with a temperature of {temperature}°C. "

            if wind_speed > 10:
                weather_info += f"It's quite windy with a wind speed of {wind_speed} m/s. "
            else:
                weather_info += "There is little to no wind. "

            if rain_chance > 0:
                weather_info += f"There is a chance of rain today with {rain_chance}mm of rainfall expected."
            else:
                weather_info += "It looks like it won't rain today."

            return weather_info
        else:
            return "Sorry, I couldn't fetch the weather right now."
    except Exception as e:
        return f"An error occurred: {str(e)}"

def get_forecast():
    try:
        url = f"{FORECAST_URL}?q={CITY}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()

        if data["cod"] == "200":
            tomorrow_weather = data["list"][8]
            weather_description = tomorrow_weather["weather"][0]["description"]
            temperature = tomorrow_weather["main"]["temp"]
            rain_chance = tomorrow_weather.get("rain", {}).get("3h", 0)

            forecast_info = f"Tomorrow's weather in {CITY} will be {weather_description} with a temperature of {temperature}°C."

            if rain_chance > 0:
                forecast_info += f" You might want to carry an umbrella as there is {rain_chance}mm of rain expected."

            return forecast_info
        else:
            return "Sorry, I couldn't fetch the forecast for tomorrow."
    except Exception as e:
        return f"An error occurred: {str(e)}"

def execute(args):
    current_hour = datetime.datetime.now().hour

    greeting = generate_greeting()
    speak(greeting)

    if 5 <= current_hour < 12:
        weather_info = get_weather()
        speak(weather_info)

    elif 12 <= current_hour < 18:
        weather_info = get_weather()
        speak(weather_info)

        url = f"{BASE_URL}?q={CITY}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()

        if data["cod"] == 200:
            rain_chance = data.get("rain", {}).get("1h", 0)
            if rain_chance > 0:
                speak("I'm sure you didn't forget your umbrella again, right?")

    elif 18 <= current_hour < 22:  # Evening
        forecast_info = get_forecast()
        speak(forecast_info)

    else:  # Night
        forecast_info = get_forecast()
        speak(forecast_info)
