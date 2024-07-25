import ccxt

def get_binance_data(symbol):
    binance = ccxt.binance()
    data = binance.fetch_ticker(symbol)
    return data
