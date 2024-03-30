import pyodbc
import pandas as pd
#from sqlalchemy import create_engine

def executeSQL(sqlStatement):
    cursor.execute(sqlStatement)
    cursor.commit()
    return

#Truncate tables
def truncateTables():
    executeSQL('''TRUNCATE TABLE STARTING_BALANCES''')
    executeSQL('''TRUNCATE TABLE ENDING_BALANCES''')
    executeSQL('''TRUNCATE TABLE ACCOUNT_TRANSACTIONS''')
    executeSQL('''TRUNCATE TABLE BALANCES''')
    executeSQL('''TRUNCATE TABLE AVERAGE_MONTHLY_BALANCES''')
    executeSQL('''TRUNCATE TABLE MINIMUM_MONTHLY_BALANCES''')

#Get a list of values to insert into SQL
# def listValuesForSQL(list):
#     listvalues = ""
#     colvalues = ""
#     for row in list:
#         colvalues = ""
#         for col in row:
#             colvalues = colvalues  + "'" + str(col).replace("'", "''") + "',"
#         listvalues = listvalues + "\n(" + colvalues[:-1] + "),"
#     print(listvalues[:-1])
#     return listvalues[:-1]  #strip the last comma character because loops with commas are bullshit


def insertStocks(stocks):
    executeSQL('''  IF NOT EXISTS (SELECT * FROM sysobjects WHERE id = object_id(N'[dbo].[Stocks]'))
                    CREATE TABLE dbo.Stocks (
                        [Symbol] [nvarchar](50) NOT NULL,
                        [Name] [nvarchar](150) NULL,
                        [Last_Sale] [money] NULL,
                        [Net_Change] [float] NULL,
                        [Change] [nvarchar](50) NULL,
                        [Market_Cap] [float] NULL,
                        [Country] [nvarchar](50) NULL,
                        [IPO_Year] [smallint] NULL,
                        [Volume] [int] NOT NULL,
                        [Sector] [nvarchar](50) NULL,
                        [Industry] [nvarchar](100) NULL
                            )''')

    # listValues = listValuesForSQL(stocks)
    # if listValues != "":
    columns = list(stocks)
    sql_query = f"INSERT INTO [dbo].[Stocks]([Symbol],[Name],[Last_Sale],[Net_Change],[Change],[Market_Cap],[Country],[IPO_Year],[Volume],[Sector],[Industry]) VALUES ({','.join('?' * len(columns))})"
    for chunk in stocks.iterrows(chunksize=1000):
        value_list = chunk[1].to_numpy().tolist()  # Convert chunk to list of values
        cursor.executemany(sql_query, value_list)
        connection.commit()
    return

def insertStocksPrices(stockPrices):
    executeSQL('''  IF NOT EXISTS (SELECT * FROM sysobjects WHERE id = object_id(N'[dbo].[StockPrices]'))
                    CREATE TABLE dbo.StockPrices (
	                        [Symbol] [varchar](50) NOT NULL,
                            [Date] [varchar](50) NULL,
                            [Open] [varchar](50) NULL,
                            [High] [varchar](50) NULL,
                            [Low] [varchar](50) NULL,
                            [Close] [varchar](50) NULL,
                            [Volume] [varchar](50) NULL
                            )''')
    
    columns = list(stockPrices)
    column_names = stockPrices.columns.tolist()
    chunksize = 1000
    for i in range(0, len(stockPrices), chunksize):
        chunk = stockPrices.iloc[i:i+chunksize]
        sql_query = f"INSERT INTO [dbo].[StockPrices] ([Symbol],[Date],[Open],[High],[Low],[Close],[Volume]) VALUES ({','.join(['?'] * len(column_names))})"
        value_list = chunk.values.tolist()  # Convert chunk to list of values
        cursor.executemany(sql_query, value_list)
        connection.commit()
    return

def insertPredictions(predictions):
    executeSQL('''  IF NOT EXISTS (SELECT * FROM sysobjects WHERE id = object_id(N'[dbo].[Predictions]'))
                    CREATE TABLE dbo.Predictions (
	                        [Symbol] [varchar](50) NOT NULL,
                            [Date] [varchar](50) NULL,
                            [Close] [varchar](50) NULL,
                            [MA25] [varchar](50) NULL,
                            [MA50] [varchar](50) NULL,
                            [MA100] [varchar](50) NULL,
                            [MA200] [varchar](50) NULL,
                            [MA500] [varchar](50) NULL,
                            [MA1000] [varchar](50) NULL,
                            )''')
    
    column_names = predictions.columns.tolist()
    chunksize = 1000
    for i in range(0, len(predictions), chunksize):
        chunk = predictions.iloc[i:i+chunksize]
        sql_query = f"INSERT INTO [dbo].[Predictions] ([Symbol],[Date],[Close],[MA25],[MA50],[MA100],[MA200],[MA500],[MA1000]) VALUES ({','.join(['?'] * len(column_names))})"
        value_list = chunk.values.tolist()  # Convert chunk to list of values
        cursor.executemany(sql_query, value_list)
        connection.commit()
    return

#Get all rows from a specified SQL table
def queryStockPrices(stock=""):
    query = "SELECT * FROM dbo.StockPrices"
    if stock != "":
        query = query + " WHERE Symbol = '" + stock + "'"
    queryRows = pd.read_sql(query, connection)
    return queryRows

#Get all rows from a specified SQL table
def getMericaStonks(stock=""):
    query = "EXEC dbo.stonks"
    queryRows = pd.read_sql(query, connection)
    return queryRows

#Get all rows from a specified SQL table
def queryStocks():
    query = "SELECT * FROM dbo.Stocks"
    cursor.execute(query)
    data = cursor.fetchall()
    return data

def createSQLConnection(fullReload=1):
    global connection
    global cursor
    #global engine
    server = 'BRUCE'
    database = 'Prod'
    connection_string = 'Driver=SQL Server;Server=' + server + ';Database=' + database + ';Trusted_Connection=True;'
    connection = pyodbc.connect(connection_string)
    cursor = connection.cursor()
    return

def closeSqlConnection():
    cursor.close()
    connection.close()
    return