import yfinance as yf
import pandas as pd
from datetime import date

# Replace "AAPL" with your desired ticker symbol(s)
ticker = "AAPL"

# Set start and end dates in YYYY-MM-DD format (optional)
#start_date = None  # Download all available data
#end_date = None

years = 1
end_date = date.today()
start_date = end_date - pd.Timedelta(days=365*years)

data = yf.download(ticker, start=start_date, end=end_date)

data.to_csv(ticker + "_data.csv")  # Replace with your desired filename