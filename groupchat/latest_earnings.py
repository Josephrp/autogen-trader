# filename: latest_earnings.py

import yfinance as yf

# Define the ticker symbol
tickerSymbol = 'PLTR'

# Get data on this ticker
tickerData = yf.Ticker(tickerSymbol)

# Get earnings data
earnings_data = tickerData.earnings

# Print the last earning data
print(earnings_data.tail(1))