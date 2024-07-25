import requests

ALPACA_BASE_URL = 'https://paper-api.alpaca.markets'
ALPACA_API_KEY = 'your_api_key'
ALPACA_SECRET_KEY = 'your_secret_key'

def place_order(symbol, qty, side, type, time_in_force):
    url = f"{ALPACA_BASE_URL}/v2/orders"
    headers = {
        'APCA-API-KEY-ID': ALPACA_API_KEY,
        'APCA-API-SECRET-KEY': ALPACA_SECRET_KEY
    }
    params = {
        'symbol': symbol,
        'qty': qty,
        'side': side,
        'type': type,
        'time_in_force': time_in_force
    }
    response = requests.post(url, json=params, headers=headers)
    return response.json()
