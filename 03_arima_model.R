install.packages("forecast")
install.packages("ggplot2")
install.packages("RSQLite")
install.packages("lubridate")

# --- 1. Load Libraries ---
library(forecast)
library(ggplot2)
library(RSQLite)
library(lubridate)

# --- 2. Load Data from SQLite Database ---
# This ensures we are using the exact same data as our Python model
db_path <- "stock_data.db"
stock_ticker <- "AAPL"

# Connect to the database
con <- dbConnect(RSQLite::SQLite(), dbname = db_path)

# Create the query
query <- paste("SELECT Date, \"Close\" FROM", stock_ticker)

# Execute the query and fetch the results
stock_data <- dbGetQuery(con, query)

# Disconnect from the database
dbDisconnect(con)

# --- 3. Prepare the Time Series Data ---
# Convert the 'Date' column to a Date object
stock_data$Date <- as.Date(stock_data$Date)

# Create a time series object ('ts') which is required by the forecast package.
# We specify the frequency as 252, which is the approx. number of trading days in a year.
ts_data <- ts(stock_data$Close, frequency = 252, start = c(year(stock_data$Date[1]), month(stock_data$Date[1])))


# --- 4. Build and Train the ARIMA Model ---
# Teaching Moment: The auto.arima() function is amazing. It automatically
# tests different combinations of ARIMA parameters and selects the best one for our data.
print("Finding the best ARIMA model...")
arima_model <- auto.arima(ts_data)

# Print a summary of the model
summary(arima_model)


# --- 5. Forecast Future Prices ---
# Let's forecast the next 90 days
print("Forecasting future prices...")
forecast_values <- forecast(arima_model, h = 90)

# --- 6. Visualize the Forecast ---
# The autoplot() function creates a beautiful plot of our forecast.
print("Generating plot...")
autoplot(forecast_values) +
  labs(title = paste(stock_ticker, "Stock Price Forecast (ARIMA)"),
       x = "Year",
       y = "Price (USD)") +
  theme_minimal()

print("R script finished.")