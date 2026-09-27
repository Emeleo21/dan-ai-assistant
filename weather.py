import requests

def get_weather(city: str) -> str:
    """Get the current weather for a given city."""
    # Step 1: turn city name into lat/lon
    geo = requests.get(
        "https://geocoding-api.open-meteo.com/v1/search",
        params={"name": city, "count": 1}
    ).json()

    if "results" not in geo:
        return f"Couldn't find location: {city}"

    lat = geo["results"][0]["latitude"]
    lon = geo["results"][0]["longitude"]

    # Step 2: get current weather for that lat/lon
    weather = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={"latitude": lat, "longitude": lon, "current_weather": True}
    ).json()

    temp = weather["current_weather"]["temperature"]
    wind = weather["current_weather"]["windspeed"]
    return f"It's currently {temp}°C in {city}, with wind speed {wind} km/h."

if __name__ == "__main__":
    print(get_weather("Lagos"))