import requests
from datetime import datetime
from zoneinfo import ZoneInfo
from timezonefinder import TimezoneFinder

tf = TimezoneFinder()

def get_local_time(city: str) -> str:
    """Get the current local date and time in a given city."""
    try:
        geo = requests.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": city, "count": 1}
        ).json()

        if "results" not in geo:
            return f"Couldn't find location: {city}"

        lat = geo["results"][0]["latitude"]
        lon = geo["results"][0]["longitude"]

        tz_name = tf.timezone_at(lat=lat, lng=lon)
        if not tz_name:
            return f"Couldn't determine time zone for {city}"

        now = datetime.now(ZoneInfo(tz_name))
        return f"The current local time in {city} is {now.strftime('%A, %d %B %Y, %I:%M %p')} ({tz_name})."
    except Exception as e:
        return f"Error fetching local time: {e}"

if __name__ == "__main__":
    print(get_local_time("Lagos"))
    print(get_local_time("Tokyo"))
    print(get_local_time("New York"))