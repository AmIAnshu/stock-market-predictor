# 📈 Interactive Stock Market Analysis App

## Project Overview

This project is an interactive web application that provides predictive analytics for the stock market. Built with Python and Streamlit, it allows users to enter a stock ticker and receive several analytical outputs, including a next-day price prediction and short-term momentum analysis.

The app demonstrates a full data science pipeline, from real-time data acquisition via API to model training, prediction, and presentation in a user-friendly GUI.



---

## 🛠️ Tech Stack & Features

* **App Framework:** Streamlit
* **Programming Language:** Python
* **Key Libraries:** `yfinance`, `pandas`, `scikit-learn`, `statsmodels`, `matplotlib`
* **Features:**
    * **Interactive GUI:** Users can input any stock ticker to get a custom analysis.
    * **Next-Day Prediction:** A Linear Regression model predicts the closing price for the next trading day.
    * **30-Day Forecast:** A statistical ARIMA model provides a longer-term forecast with confidence intervals.
    * **Intraday Momentum Analysis:** Calculates the 1-minute Relative Strength Index (RSI) to gauge short-term market sentiment ("overbought" or "oversold").

---

## 🚀 How to Run the App Locally

1.  **Clone the Repository:**
    ```bash
    git clone <your-repository-url>
    cd <repository-name>
    ```

2.  **Create and Activate a Virtual Environment:**
    ```bash
    # Create the environment
    python -m venv venv

    # Activate it (Windows)
    .\venv\Scripts\activate

    # Activate it (Mac/Linux)
    source venv/bin/activate
    ```

3.  **Install the Required Packages:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Streamlit App:**
    ```bash
    streamlit run app.py
    ```
    The application will automatically open in your web browser.

---

## 📂 Project Files

* `app.py`: The main Streamlit application script containing all logic.
* `requirements.txt`: A list of all necessary Python packages.
* `.gitignore`: Specifies files for Git to ignore (e.g., the `venv` folder).
* _The original analysis scripts (`01_get_data.py`, etc.) can be kept for reference._