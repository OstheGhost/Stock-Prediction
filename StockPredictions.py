# This predictor uses simple linear regression
# Need to look into Support Vector Machines (SVM), Random Forests, and LSTMs

import yfinance as yf
from sklearn.linear_model import LinearRegression  # Example model
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import pandas as pd
import SQL_Functions as sql
import datetime as dt

ticker = "AAPL"  # Replace with your desired stock ticker
start_date = "2020-01-01"
end_date = "2023-12-31"

#data = yf.download(ticker, start=start_date, end=end_date)
#data = yf.download(ticker, period='1y')
sql.createSQLConnection()
data = sql.queryStockPrices("DIS")
sql.closeSqlConnection()

# if not isinstance(data, pd.DataFrame):
#     data = data.to_frame()

#print(data)

#data = data['Close']
data["MA50"] = data["Close"].rolling(window=50).mean()

data = data.dropna(axis=0, how='any')

data["Date"] = pd.to_datetime(data["Date"]).map(dt.datetime.toordinal)
X = data[["Date"]]
y = data[["Close", "MA50"]] #.shift(-20)

#data = data.dropna(axis=0, how='any')

# print(X)
# print(y)

#X_train, X_test, y_train, y_test = train_test_split(data[:-1], data['Close'][1:], test_size=0.2)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model = LinearRegression()
model.fit(X_train, y_train)

# Set up array of dates to predict Close prices for
x_arr = ["2024-05-01", "2024-09-01", "2025-01-01", "2030-01-01"]
x_vals = pd.DataFrame({"Date": x_arr})
x_vals["OriginalDate"] = x_vals["Date"].copy()
x_vals["Date"] = pd.to_datetime(x_vals["Date"]).map(dt.datetime.toordinal)
x_pred = x_vals[["Date"]]

y_pred = model.predict(x_pred)

# df_x_pred = pd.DataFrame(x_pred, columns=pd.Series("Feature_" + str(i) for i in range(x_pred.size)))
# df_y_pred = pd.DataFrame(y_pred.reshape(-1, 1), columns=["Prediction"])

# predictions = y_pred.astype(str)
predictions = pd.concat([x_vals[["OriginalDate"]], pd.DataFrame(y_pred, columns=["max", "min"])], axis=1)
print(predictions)
#mse = mean_squared_error(y_test, y_pred)
#print("Mean Squared Error: ", mse)
print(ticker + " predicted range from " + str(y_pred.min()) + " to " + str(y_pred.max()))
print("Average predicted price = " + str(y_pred.mean()))
print("Current " + ticker + " price = " + str(data['Close'].iloc[-1]))
# y_pred_2 = y_pred.sort()
# len = y_pred.__len__
# median_idx = len // 2
# print("Median predicted price = " + str(y_pred_2[median_idx]))

# Predict for the next 20 days (adjust for your time horizon)
#last_data_point = X.iloc[-1]  # Get features for the last data point
#future_prediction = model.predict([last_data_point])

# Print the predicted closing price (assuming daily predictions)
#print(f"Predicted closing price in 20 days: {future_prediction[0]:.2f}")
