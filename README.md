# 📊 Financial Forecasting & Analysis Dashboard

This is a simple and interactive Streamlit dashboard that helps forecast financial data like Revenue, COGS, Operating Expenses, and Net Income. It uses ARIMA for time series forecasting and includes anomaly detection and basic visualizations.

---

## Features

- Forecasts Revenue, COGS, Operating Expenses, Net Income
- Calculates accuracy metrics (MAE, RMSE, MSE)
- Shows profit margin and revenue growth
- Compares Actual vs Budget vs Forecast
- Detects anomalies and shows alerts
- Simple and clean Streamlit interface

---

## Tech Used

- Python
- Streamlit
- Pandas, NumPy
- Matplotlib, Seaborn
- Statsmodels (ARIMA)

---

## Dataset details
   The dataset used in this project is synthetically generated but closely follows realistic financial growth patterns for a company over a 5-year period. It includes monthly financial metrics with progressive growth to mimic business scaling.
   The data is generated as follows:

   - 5 years of monthly data: January 2020 to December 2024

   - Revenue, Cost of Goods Sold (COGS), and Operating Expenses are linearly increased month-over-month.

   - Net Income is computed as:

   - Net Income = Revenue - COGS - Operating Expenses

   - Forecast period: 24 months ahead (2025–2026)
   
---

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/fpna-dashboard.git
   cd fpna-dashboard
2. Run the app:

   streamlit run main.py



<h2>Actual vs Forecast Comparison</h2>
<img src="https://github.com/user-attachments/assets/7973ffab-d867-42dc-ada1-53f9383b4a66" alt="Actual vs Forecast Comparison - Chart 1" width="100%" />

<h2>Actual vs Forecast Comparison</h2>
<img src="https://github.com/user-attachments/assets/14dd12d6-d6dd-4d85-a7fd-eaed418e3ea4" alt="Actual vs Forecast Comparison - Chart 2" width="100%" />


<h2>Metrics</h2>
<img width="1578" height="806" alt="image" src="https://github.com/user-attachments/assets/9841d7cb-b531-4936-a652-1d34b8cb506d" />

<h2>Variance Analysis</h2>
<img width="1586" height="791" alt="image" src="https://github.com/user-attachments/assets/11ade13c-999a-49ff-a28e-58674a436d5f" />

<h2>Forecasted data</h2>
<img width="1582" height="842" alt="image" src="https://github.com/user-attachments/assets/9a3d349a-e329-4a9c-9cbf-4ba7e8f91e6b" />





