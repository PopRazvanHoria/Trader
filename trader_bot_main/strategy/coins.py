COINS = [
    {"symbol": "BTC", "name": "Bitcoin"},
    {"symbol": "ETH", "name": "Ethereum"},
    {"symbol": "SOL", "name": "Solana"},
    {"symbol": "XRP", "name": "Ripple"},
    {"symbol": "DOGE", "name": "Dogecoin"},
    {"symbol": "TON", "name": "Toncoin"},
    {"symbol": "TRX", "name": "Tron"},
    {"symbol": "ADA", "name": "Cardano"},
    {"symbol": "BNB", "name": "Binance Coin"},
    {"symbol": "USDC", "name": "USD Coin"},
]

def get_coin_choices():
    return [(coin["symbol"], coin["name"]) for coin in COINS]