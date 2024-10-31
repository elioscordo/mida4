from alpaca.data import CryptoHistoricalDataClient, StockHistoricalDataClient
from alpaca.data import StockLatestQuoteRequest
from alpaca.trading.client import TradingClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame, TimeFrameUnit
from alpaca.data.enums import DataFeed, Adjustment
import pandas as pd
from datetime import date, timedelta, datetime
from django.conf import settings
# no keys required.
crypto_client = CryptoHistoricalDataClient()


key = settings.ALPACA_KEY
secret = settings.ALPACA_SECRET

# keys required
historical_client = StockHistoricalDataClient(key,  secret)

data_client = StockHistoricalDataClient(key, secret)
trading_client = TradingClient(key, secret, paper=True)


def get_ask_price(symbols):
    # multi symbol request - single symbol is similar
    multisymbol_request_params = StockLatestQuoteRequest(
        symbol_or_symbols=symbols
    )

    latest_multisymbol_quotes = data_client.get_stock_latest_quote(
        multisymbol_request_params
    )
    return latest_multisymbol_quotes



def get_all_assets():
    # multi symbol request - single symbol is similar
    active_assets = trading_client.get_all_assets()
    return active_assets


def asset_to_dict(asset):
    return {
        "alpaca": {
            "status": asset.status,
            "tradable": asset.tradable,
            "marginable": asset.marginable,
            "shortable": asset.shortable,
            "easy_to_borrow": asset.easy_to_borrow,
            "fractionable": asset.fractionable
        }
    }


def fetch_alpaca_data(symbol, time_frame=TimeFrame.Day, start=None, end=None):
    if start is None:
        start = datetime.now()
    if end is None:
        end = start - timedelta(days=365)
    start_str = start.strftime("%m/%d/%Y, %H:%M:%S")
    end_str = end.strftime("%m/%d/%Y, %H:%M:%S")

    request_params = StockBarsRequest(
            symbol_or_symbols=[symbol],
            timeframe=time_frame,
            start=start_str,
            end=end_str,
            adjustment=Adjustment.RAW,
            feed=DataFeed.SIP
        )
    df = historical_client.get_stock_bars(request_params)
    return df


if __name__ == "__main__":
    pass
