import streamlit as st
import pandas as pd
import yfinance as yf
from sklearn.linear_model import LinearRegression
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA

# --- Page Configuration ---
st.set_page_config(
    page_title="Stock Market Predictor",
    page_icon="📈",
    layout="wide"
)

# --- App Title and Description ---
st.title("📈 Simple Stock Market Predictor")
st.markdown("""
This app uses historical data to make a simple prediction about a stock's closing price for the next day.
**Disclaimer:** This is an educational tool and not financial advice.
""")

# --- Sidebar for User Input ---
st.sidebar.header("User Input")
stock_ticker = st.sidebar.text_input("Enter Stock Ticker (e.g., AAPL, GOOGL)", "AAPL").upper()
run_button = st.sidebar.button("Run Analysis")

# --- Clarify Timeframe ---
st.info("💡 **Important:** This app predicts the **closing price for the next day**, not price movements within the next few minutes. Short-term trading is much more complex!")

# --- Main App Logic ---
if run_button:
    # --- 1. Data Fetching ---
    st.header(f"Analysis for {stock_ticker}")
    data_load_state = st.text(f"Loading data for {stock_ticker}...")
    try:
        df = yf.download(stock_ticker, start="2015-01-01", end="2025-09-20")
        if df.empty:
            st.error("No data found for this ticker. Please check the ticker symbol.")
            st.stop()
        data_load_state.text("Loading data... done!")
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        st.stop()

    # --- 2. Display Historical Data Plot ---
    st.subheader("Looking at the Past")
    st.markdown("This chart shows the stock's historical closing price. This helps us see the overall trend.")
    fig, ax = plt.subplots(figsize=(14, 7))
    ax.plot(df['Close'], label='Close Price')
    ax.set_title(f'{stock_ticker} Historical Close Price', fontsize=16)
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Price (USD)', fontsize=12)
    ax.legend()
    st.pyplot(fig)

    # --- 3. Python Linear Regression Model ---
    st.header("Prediction 1: The 'Simple Trend' Guess")
    st.markdown("This first prediction is like drawing a straight line through the recent price points to guess the next one. It's a simple, baseline prediction.")

    # Prepare data
    df_lr = df[['Close']].copy()
    df_lr['Prediction'] = df_lr['Close'].shift(-1)
    df_lr.dropna(inplace=True)

    X = np.array(df_lr[['Close']])
    y = np.array(df_lr['Prediction'])

    # Train model
    model = LinearRegression()
    model.fit(X, y)

    # Make prediction for the next day
    last_price_val = df['Close'].iloc[-1].item()
    last_price_2d = np.array([last_price_val]).reshape(1, -1)
    prediction = model.predict(last_price_2d)

    # --- The Verdict ---
    st.subheader("So, will the price go up or down?")
    if prediction[0] > last_price_val:
        st.success(f"🔼 **UP**: The model predicts the price will rise from ${last_price_val:.2f} to **${prediction[0]:.2f}**.")
    else:
        st.warning(f"🔽 **DOWN**: The model predicts the price will fall from ${last_price_val:.2f} to **${prediction[0]:.2f}**.")

    # --- 4. ARIMA Model (Python version of the R model) ---
    st.header("Prediction 2: The 'Pattern Expert' Guess")
    st.markdown("This second model, ARIMA, is more sophisticated. It's an expert at finding repeating patterns, trends, and 'memory' in the price history to forecast the future.")
    with st.spinner('Fitting ARIMA model... This may take a moment.'):
        try:
            ts_data = df['Close'][-500:]
            arima_model = ARIMA(ts_data, order=(5, 1, 0))
            arima_result = arima_model.fit()
            
            forecast = arima_result.get_forecast(steps=30)
            forecast_index = pd.date_range(start=ts_data.index[-1], periods=31)[1:]
            forecast_series = pd.Series(forecast.predicted_mean.values, index=forecast_index)
            conf_int = forecast.conf_int()
            conf_int.index = forecast_index

            st.subheader("30-Day Forecast")
            fig_arima, ax_arima = plt.subplots(figsize=(14, 7))
            ax_arima.plot(ts_data, label='Historical Price (Last 500 days)')
            ax_arima.plot(forecast_series, label='Forecast', color='red')
            ax_arima.fill_between(forecast_index, conf_int.iloc[:, 0], conf_int.iloc[:, 1], color='pink', alpha=0.5)
            ax_arima.set_title('ARIMA Forecast with 95% Confidence Interval', fontsize=16)
            ax_arima.legend()
            st.pyplot(fig_arima)
            
            st.markdown("""
            - The **red line** is the model's forecast.
            - The **pink area** is the 'Confidence Interval'. It shows the range of uncertainty. The model is 95% confident the actual price will stay within this pink zone. Notice how it gets wider? That's because it's harder to be certain about predictions far in the future.
            """)
        except Exception as e:
            st.error(f"ARIMA model failed. Error: {e}")

# --- 5. Intraday Momentum Analysis (Educational Demo) ---
    st.header("Short-Term Momentum (Educational Demo)")
    st.markdown("This section analyzes the last few days of minute-by-minute data to check for short-term momentum using the Relative Strength Index (RSI). This is **not a prediction**, but a common technical indicator.")

    with st.spinner("Loading intraday data and calculating RSI..."):
        try:
            # Fetch intraday data (1-minute interval for the last 5 days)
            intraday_df = yf.download(stock_ticker, period="5d", interval="1m")

            if intraday_df.empty:
                st.warning("Could not retrieve intraday data for this ticker.")
            else:
                # Calculate RSI
                delta = intraday_df['Close'].diff()
                gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                rs = gain / loss
                rsi = 100 - (100 / (1 + rs))
                
                # --- THIS IS THE FIX ---
                last_rsi = rsi.iloc[-1].item() # .item() extracts the single number

                st.subheader(f"Current 1-Minute RSI: {last_rsi:.2f}")

                # Give a simple verdict based on RSI
                if last_rsi > 70:
                    st.warning("Status: **Overbought**. The RSI suggests the price has risen quickly and may be due for a pullback (a drop).")
                elif last_rsi < 30:
                    st.success("Status: **Oversold**. The RSI suggests the price has fallen quickly and may be due for a bounce (a rise).")
                else:
                    st.info("Status: **Neutral**. The RSI is between 30 and 70, indicating no strong short-term momentum in either direction.")

                # Plot the recent intraday price and RSI
                st.markdown("The charts below show the price and RSI for the most recent trading day.")
                today_data = intraday_df.last('1D') # Get data for the last day

                fig_intraday, ax1 = plt.subplots(figsize=(14, 7))
                ax1.set_title(f"{stock_ticker} Intraday Price and RSI")
                ax1.plot(today_data.index, today_data['Close'], 'b-', label='Price')
                ax1.set_xlabel('Time')
                ax1.set_ylabel('Price (USD)', color='b')
                ax1.tick_params(axis='y', labelcolor='b')

                ax2 = ax1.twinx() # Create a second y-axis
                ax2.plot(today_data.index, rsi.loc[today_data.index], 'r-', label='RSI')
                ax2.set_ylabel('RSI', color='r')
                ax2.tick_params(axis='y', labelcolor='r')
                ax2.axhline(70, color='r', linestyle='--', alpha=0.5)
                ax2.axhline(30, color='g', linestyle='--', alpha=0.5)
                
                st.pyplot(fig_intraday)

        except Exception as e:
            st.error(f"Could not perform intraday analysis. Error: {e}")


# --- THE FIX IS HERE ---
# This 'else' statement is now correctly unindented to match the 'if run_button:'
else:
    st.info("Enter a stock ticker on the left and click 'Run Analysis' to begin.")