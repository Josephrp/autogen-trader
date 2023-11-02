# filename: ytd_gain.py

import yfinance as yf
from datetime import datetime

def get_ytd_gain(ticker):
    now = datetime.now()
    start_date = datetime(now.year, 1, 1)
    stock = yf.Ticker(ticker)
    hist = stock.history(start=start_date.strftime('%Y-%m-%d'), end=now.strftime('%Y-%m-%d'))
    ytd_gain = (hist['Close'][-1] - hist['Close'][0]) / hist['Close'][0] * 100
    return ytd_gain

msft_gain = get_ytd_gain('MSFT')
tesla_gain = get_ytd_gain('TSLA')

print(f"MSFT's YTD gain: {msft_gain}%")
print(f"TESLA's YTD gain: {tesla_gain}%")