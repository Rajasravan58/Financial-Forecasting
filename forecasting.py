# forecasting.py
import numpy as np
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from config import HISTORICAL_REVENUE, HISTORICAL_COSTS, HISTORICAL_OPERATING_EXPENSES, FORECAST_PERIOD

def forecast_series(series, steps):
    model = ExponentialSmoothing(series, trend='add', seasonal=None, damped_trend=True)
    model_fit = model.fit()
    return model_fit.forecast(steps=steps)

def forecast_revenue():
    return forecast_series(HISTORICAL_REVENUE, FORECAST_PERIOD)

def forecast_costs():
    return forecast_series(HISTORICAL_COSTS, FORECAST_PERIOD)

def forecast_operating_expenses():
    return forecast_series(HISTORICAL_OPERATING_EXPENSES, FORECAST_PERIOD)

def forecast_net_income(forecasted_revenue, forecasted_costs, forecasted_operating_expenses):
    return forecasted_revenue - forecasted_costs - forecasted_operating_expenses
