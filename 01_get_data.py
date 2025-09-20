import yfinance as yf
import sqlite3
import pandas as pd

# --- 1. Fetching the Data ---
# Define the stock ticker and the date range
STOCK_TICKER = "AAPL" # Apple Inc.
START_DATE = "2015-01-01"
END_DATE = "2025-09-20" # Use current date or a recent one

print(f"Fetching data for {STOCK_TICKER} from {START_DATE} to {END_DATE}...")

# Use yfinance to download the stock data
stock_data = yf.download(STOCK_TICKER, start=START_DATE, end=END_DATE)

stock_data = yf.download(STOCK_TICKER, start=START_DATE, end=END_DATE)

# --- NEW FIX: Add these 3 lines ---
if isinstance(stock_data.columns, pd.MultiIndex):
    stock_data.columns = stock_data.columns.droplevel(1)
# --- END FIX ---

# Teaching Moment: The data you get is a Pandas DataFrame.
print("Data fetched successfully. Here are the first 5 rows:")

# Teaching Moment: The data you get is a Pandas DataFrame.
# It's like a spreadsheet in Python. It has rows (dates) and columns (Open, High, Low, Close, etc.).
print("Data fetched successfully. Here are the first 5 rows:")
print(stock_data.head())

# --- 2. Storing the Data in a SQL Database ---
# We use SQLite for simplicity. It creates a database in a single file.
DB_NAME = "stock_data.db"
TABLE_NAME = STOCK_TICKER

print(f"\nStoring data in database '{DB_NAME}' in table '{TABLE_NAME}'...")

# Connect to the SQLite database (it will be created if it doesn't exist)
conn = sqlite3.connect(DB_NAME)

# Write the data from the DataFrame to the SQL table
# `if_exists='replace'` will drop the table first if it exists and create a new one.
# This is useful for rerunning the script to get fresh data.
stock_data.to_sql(TABLE_NAME, conn, if_exists='replace', index=True)

# Close the connection
conn.close()

print("Data stored successfully.")