from datetime import datetime
import pandas as pd

# Simulate 5 years of monthly data (60 months)
months = pd.date_range(start='2020-01-01', periods=60, freq='M')

BUDGET = {
    'Revenue': pd.Series([100000 + i * 1500 for i in range(60)], index=months),
    'Cost_of_Goods_Sold': pd.Series([50000 + i * 800 for i in range(60)], index=months),
    'Operating_Expenses': pd.Series([20000 + i * 600 for i in range(60)], index=months),
}
BUDGET['Net_Income'] = BUDGET['Revenue'] - BUDGET['Cost_of_Goods_Sold'] - BUDGET['Operating_Expenses']

# Historical data
HISTORICAL_REVENUE = BUDGET['Revenue']
HISTORICAL_COSTS = BUDGET['Cost_of_Goods_Sold']
HISTORICAL_OPERATING_EXPENSES = BUDGET['Operating_Expenses']

# Forecast period (e.g. next 24 months)
FORECAST_PERIOD_YEARS = 2
FORECAST_PERIOD = 12 * FORECAST_PERIOD_YEARS
