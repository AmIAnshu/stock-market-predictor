import sqlite3
import pandas as pd

DB_NAME = "stock_data.db"
STOCK_TICKER = "AAPL" # Make sure this matches your table name

# Connect to the database
conn = sqlite3.connect(DB_NAME)

# Read the first 5 rows of the table
df = pd.read_sql_query(f"SELECT * FROM {STOCK_TICKER} LIMIT 5", conn)

conn.close()

# Print the first few rows to see the data
print("--- First 5 Rows in the Database ---")
print(df)
print("\n" + "="*30 + "\n")

# The most important part: Print the exact column names
print("--- EXACT COLUMN NAMES ---")
print(df.columns.tolist())