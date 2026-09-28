import os
import streamlit as st
import requests
from dotenv import load_dotenv

load_dotenv()

TWELVE_DATA_KEY = os.environ.get("TWELVEDATA_API_KEY") or st.secrets.get("TWELVEDATA_API_KEY")

def get_forex_rate(base: str, target: str) -> str:
    """Get the current exchange rate between two currencies or assets, 
    e.g. base='USD', target='NGN', or base='XAU', target='USD' for gold."""
    base = base.upper()
    target = target.upper()
    try:
        r = requests.get(
            "https://api.twelvedata.com/exchange_rate",
            params={"symbol": f"{base}/{target}", "apikey": TWELVE_DATA_KEY}
        ).json()

        if "rate" not in r:
            return f"Couldn't get rate for {base} to {target}: {r.get('message', 'unknown error')}"

        rate = r["rate"]
        return f"1 {base} = {rate} {target}"
    except Exception as e:
        return f"Error fetching forex rate: {e}"

if __name__ == "__main__":
    print(get_forex_rate("USD", "NGN"))
    print(get_forex_rate("XAU", "USD"))
    print(get_forex_rate("GBP", "EUR"))
