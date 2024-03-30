import pandas as pd
import yfinance as yf
import SQL_Functions as sql
from datetime import date

#print yf.tickers

# Get NASDAQ tickers
#nasdaq_tickers = pd.read_csv("https://www.nasdaqtrader.com/")["Symbol"]

# Get NYSE tickers
#nyse_tickers = pd.read_csv("https://www.nyse.com/regulation/nyse")["Symbol"]

# Combine lists (remove duplicates if necessary)
#combined_tickers = list(set(nasdaq_tickers.tolist() + nyse_tickers.tolist()))

#print(combined_tickers[:10])  # Print the first 10 tickers

#symbol = "GOOG"

#Query SQL for stock tickers
def getStockSymbols():
    #get stock symbols from SQL
    stockSymbols = sql.queryStocks()
    return stockSymbols
    
def getStockPrices(stock, years=10):
    #Query SQL
    stockPrices = sql.queryStockPrices(stock)
    stockPrices = pd.DataFrame(stockPrices)

    #If SQL data present, short circuit
    if len(stockPrices) > 0:
        return None
    
    #Download data from specified range
    endDate = date.today()
    start_date = endDate - pd.Timedelta(days=365*years)
    stockPrices = yf.download(stock, start=start_date, end=endDate)
    
    #convert Date index into a column for SQL INSERT later
    stockPrices = stockPrices.reset_index()
    
    desired_columns = ["Date", "Open", "High", "Low", "Close", "Volume"]

    #Reduce dataframe down to desired columns
    stockPrices = stockPrices[desired_columns]

    #print(stockPrices['Date'])
    stockPrices['Date'] = stockPrices['Date'].dt.strftime('%Y-%m-%d')
    stockPrices.insert(loc=0, column="Symbol", value=stock) #Add a column for stock symbol
    return stockPrices

#Do Stuff
sql.createSQLConnection()

stockSymbols = getStockSymbols()

for stock in stockSymbols:
    symbol = stock[0]
    stockPrices = getStockPrices(symbol, 5)

    if not stockPrices is None:
        sql.insertStocksPrices(stockPrices)

# stockPrices = getStockPrices("GOOG", 5)
# sql.insertStocksPrices(stockPrices)

sql.closeSqlConnection()