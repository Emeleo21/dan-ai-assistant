import requests

def get_crypto_price(coin: str) -> str:
    """Get the current price of a cryptocurrency (e.g. bitcoin, ethereum, solana) in USD."""
    coin = coin.lower()
    try:
        r = requests.get(
            "https://api.coingecko.com/api/v3/simple/price",
            params={"ids": coin, "vs_currencies": "usd", "include_24hr_change": "true"}
        ).json()

        if coin not in r:
            return f"Couldn't find price data for {coin}"

        price = r[coin]["usd"]
        change = r[coin]["usd_24h_change"]
        return f"{coin.capitalize()} is currently ${price:,.2f}, {'up' if change >= 0 else 'down'} {abs(change):.2f}% in the last 24 hours."
    except Exception as e:
        return f"Error fetching crypto price: {e}"

if __name__ == "__main__":
    
    print(get_crypto_price("ethereum"))