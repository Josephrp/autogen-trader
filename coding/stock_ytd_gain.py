# filename: stock_ytd_gain.py

import datetime
import yfinance as yf

# Get the current date
current_date = datetime.date.today()
print("Today's date is:", current_date)

# Define the tickers
tickers = ['AAPL', 'MSFT', 'SPY']

# Get the data for the tickers
data = yf.download(tickers, start='2022-01-01', end=current_date)

# Calculate the YTD gain for each ticker
for ticker in tickers:
    start_price = data['Adj Close'][ticker][0]
    end_price = data['Adj Close'][ticker][-1]
    ytd_gain = (end_price - start_price) / start_price * 100
    print(f"The YTD gain for {ticker} is {ytd_gain:.2f}%")