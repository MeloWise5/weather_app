import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENWEATHERMAP_API_KEY")
print(f"API Key: {api_key[:6]}...{api_key[-4:]}" if api_key else "API Key: NOT SET")

resp = requests.get(
    "https://api.openweathermap.org/data/2.5/weather",
    params={"q": "Dallas", "appid": api_key, "units": "imperial"},
    timeout=10,
)

print(f"Status: {resp.status_code}")
if resp.status_code == 200:
    data = resp.json()
    print(f"City: {data['name']}")
    print(f"Temp: {data['main']['temp']}°F")
    print(f"Weather: {data['weather'][0]['description']}")
    print("\n✅ API key is working!")
else:
    print(f"Response: {resp.json()}")
    print("\n❌ API key not active yet. Try again later.")
