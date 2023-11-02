# filename: earnings.py

import yfinance as yf

def get_earnings(symbol):
    stock = yf.Ticker(symbol)
    earnings = stock.earnings
    return earnings

if __name__ == "__main__":
    symbol = "PLTR"
    earnings = get_earnings(symbol)
    print(earnings)