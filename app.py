import os
import requests
from flask import Flask, render_template, request
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/weather", methods=["POST"])
def weather():
    city = request.form.get("city", "").strip()
    if not city:
        return render_template("index.html", error="Please enter a city name.")

    api_key = os.getenv("OPENWEATHERMAP_API_KEY")
    if not api_key:
        return render_template("index.html", error="API key is missing. Add OPENWEATHERMAP_API_KEY to your .env file.")

    try:
        resp = requests.get(
            "https://api.openweathermap.org/data/2.5/weather",
            params={"q": city, "appid": api_key, "units": "imperial"},
            timeout=10,
        )
    except requests.RequestException:
        return render_template("index.html", error="Could not connect to weather service. Try again later.")

    if resp.status_code == 404:
        return render_template("index.html", error=f"City '{city}' not found. Check the spelling and try again.")
    if resp.status_code != 200:
        return render_template("index.html", error="Something went wrong fetching the weather. Try again later.")

    data = resp.json()
    weather_data = {
        "city": data["name"],
        "country": data["sys"]["country"],
        "temp": round(data["main"]["temp"]),
        "feels_like": round(data["main"]["feels_like"]),
        "description": data["weather"][0]["description"].title(),
        "icon": data["weather"][0]["icon"],
        "humidity": data["main"]["humidity"],
        "wind": round(data["wind"]["speed"]),
    }

    return render_template("index.html", weather=weather_data)
