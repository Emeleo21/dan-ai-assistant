import requests

def get_forex_rate(base: str, target: str) -> str:
    """Get the current exchange rate between two currencies, e.g. base='USD', target='NGN'."""
    base = base.upper()
    target = target.upper()
    try:
        r = requests.get(
    "https://api.frankfurter.dev/v2/rates",
    params={"base": base, "symbols": target}
        ).json()

        rate = r["rates"][target]
        return f"1 {base} = {rate} {target}"
    except Exception as e:
        return f"Error fetching forex rate: {e}"

if __name__ == "__main__":
    print(get_forex_rate("USD", "NGN"))