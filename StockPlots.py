#%%
import pandas as pd
import numpy as np
import sklearn.model_selection as sk
from sklearn.datasets import load_iris
import yfinance as yf
import matplotlib as mpl
import matplotlib.pyplot as plt
import SQL_Functions as sql

#print yf.tickers

# Get NASDAQ tickers
#nasdaq_tickers = pd.read_csv("https://www.nasdaqtrader.com/")["Symbol"]

# Get NYSE tickers
#nyse_tickers = pd.read_csv("https://www.nyse.com/regulation/nyse")["Symbol"]

# Combine lists (remove duplicates if necessary)
#combined_tickers = list(set(nasdaq_tickers.tolist() + nyse_tickers.tolist()))

#print(combined_tickers[:10])  # Print the first 10 tickers
#symbol = "GOOG"

def closing_price(ticker=""):
    #Asset = pd.DataFrame(yf.download(ticker, period="5y")['Close'])     
    Asset = sql.getMericaStonks()
    return Asset

#GOOG = closing_price(symbol)
#ticker = yf.Ticker(symbol)
#data = ticker.history(period="max")  # Adjust period as needed

#%%
#data.plot.line(y="Close", use_index=True)
sql.createSQLConnection()

stocks = closing_price()

# for stock in stocks:
#     for stock_info in stock:
#         print(stock_info)

stocks['Close'] = stocks['Close'].astype(float)
avg_values = stocks.groupby('Date')['Close'].mean()

plt.plot(avg_values)
plt.show()

sql.closeSqlConnection()