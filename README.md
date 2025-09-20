# Predictive Analytics for Stock Market

## 📈 Project Overview

This project aims to predict the future closing price of a stock using historical data. It employs both a machine learning approach with Python and a statistical time-series analysis with R to forecast trends and provide a comprehensive analytical view.

The primary goal is to build a baseline model that can serve as a foundation for more complex trading algorithms, demonstrating a full data science pipeline from data acquisition to model evaluation and presentation.

---

## 🛠️ Tech Stack

* **Programming Languages:** Python, R
* **Data Storage:** SQLite
* **Python Libraries:** `pandas`, `numpy`, `scikit-learn`, `matplotlib`, `seaborn`, `yfinance`
* **R Libraries:** `forecast`, `ggplot2`, `RSQLite`, `lubridate`
* **Environment:** VS Code, Git & GitHub

---

## 📂 Project Structure

stock-market-predictor/
│
├── .gitignore
├── 01_get_data.py            # Python script to fetch data and store in SQLite
├── 02_model_training.ipynb   # Jupyter Notebook for EDA and Python ML model
├── 03_arima_model.R          # R script for statistical ARIMA modeling
├── stock_data.db             # The SQLite database with our stock data
└── README.md                 # This file

---

## 🚀 How to Run this Project

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd stock-market-predictor
    ```

2.  **Set up the Python environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: .\venv\Scripts\activate
    pip install -r requirements.txt # (We will create this file in the next step!)
    ```

3.  **Run the scripts in order:**
    * Fetch the data: `python 01_get_data.py`
    * Run the Python model notebook: Open `02_model_training.ipynb` in VS Code and run the cells.
    * Run the R model: Open `03_arima_model.R` and run the source.

---

## 📊 Results & Findings

* **Python (Linear Regression Model):**
    * The model was trained on historical data for AAPL, using features like the Close price and moving averages.
    * When tested on unseen data, the model achieved a **Root Mean Squared Error (RMSE) of $X.XX**. **(<- Replace this with your actual RMSE value from the notebook!)**
    * The visualization shows the predicted price follows the actual price trend very closely, indicating it's a strong baseline model.

* **R (ARIMA Model):**
    * The `auto.arima()` function identified the optimal statistical model for the time-series data.
    * The model produced a forecast for the next 90 days, complete with 80% and 95% confidence intervals. This visualization effectively captures the inherent uncertainty in stock market prediction.

---

## 💡 Future Improvements

* **Advanced Models:** Implement more sophisticated models like LSTM (a type of neural network) which are well-suited for sequence data.
* **More Features:** Incorporate sentiment analysis from financial news or use more technical indicators.
* **Hyperparameter Tuning:** Fine-tune the model parameters to potentially improve accuracy.

