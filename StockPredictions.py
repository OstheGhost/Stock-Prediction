# This predictor uses simple linear regression
# Need to look into Support Vector Machines (SVM), Random Forests, and LSTMs

from sklearn.linear_model import LinearRegression  # Example model
from sklearn.model_selection import train_test_split
import pandas as pd
import SQL_Functions as sql
import datetime as dt
from matplotlib import pyplot as plt

# Plot X and y arrays
def plotStocks(X, y):
    # plt.scatter(X_train, y_train, color='g')
    plt.plot(X["Close"], y, color='k')

    plt.show()

# Add potential predictive factors to data array
def buildDataArray(data):
    # Build moving averages
    data["MA25"] = data["Close"].rolling(window=25).mean()
    data["MA50"] = data["Close"].rolling(window=50).mean()
    data["MA100"] = data["Close"].rolling(window=100).mean()
    data["MA200"] = data["Close"].rolling(window=200).mean()
    data["MA500"] = data["Close"].rolling(window=500).mean()
    data["MA1000"] = data["Close"].rolling(window=1000).mean()

    # drop null data
    data = data.dropna(axis=0, how='any')

    #convert dates to numeric
    data["Date"] = pd.to_datetime(data["Date"]).map(dt.datetime.toordinal)

    return data

def printPredictionInfo(ticker, y_pred, data):
    #mse = mean_squared_error(y_test, y_pred)
    #print("Mean Squared Error: ", mse)
    print(ticker + " predicted range from " + str(y_pred.min()) + " to " + str(y_pred.max()))
    print("Average predicted price = " + str(y_pred.mean()))
    print("Current " + ticker + " price = " + str(data['Close'].iloc[-1]))


ticker = "DIS"  # Replace with your desired stock ticker
start_date = "2020-01-01"
end_date = "2023-12-31"

# Set up array of dates to predict Close prices for
x_arr = ["2024-05-01", "2024-09-01", "2025-01-01", "2030-01-01"]
x_vals = pd.DataFrame({"Date": x_arr})
x_vals["OriginalDate"] = x_vals["Date"].copy()
x_vals["Date"] = pd.to_datetime(x_vals["Date"]).map(dt.datetime.toordinal)
x_pred = x_vals[["Date"]]


sql.createSQLConnection()

# Get list of stock symbols from SQL
stockSymbols = sql.queryStocks()

# Loop over stocks
for stock in stockSymbols:
    symbol = stock[0]
    data = sql.queryStockPrices(symbol)
    data = buildDataArray(data)

    # Skip this iteration if we have no data
    if data.size < 100:
        continue

    X = data[["Date"]]
    y = data[["Close", "MA25", "MA50", "MA100", "MA200", "MA500", "MA1000"]] #.shift(-20)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    model_test = LinearRegression()
    model_test.fit(X_test, y_test)

    y_pred = model_test.predict(x_pred)

    predictions = pd.concat([x_vals[["OriginalDate"]], pd.DataFrame(y_pred, columns=["Close", "MA25", "MA50", "MA100", "MA200", "MA500", "MA1000"])], axis=1)
    predictions.insert(loc=0, column="Symbol", value=symbol)
    # print(predictions)
    sql.insertPredictions(predictions)

sql.closeSqlConnection()
