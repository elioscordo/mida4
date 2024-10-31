import yfinance as yf
from django.core.cache import cache


def symbols_by_index(index):
    # wrong  not working
    symbols = cache.get(index.ticker)
    if symbols is None:
        tickers = yf.Ticker(index.ticker)
        symbols = [ticker for ticker in tickers.get_info()['components']]
        cache.set(index.code, symbols)
    return symbols
