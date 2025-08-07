from sklearn.metrics import mean_squared_error, mean_absolute_error
import numpy as np

def calculate_metrics(actual, predicted):
    actual = np.array(actual)
    predicted = np.array(predicted)
    mse = mean_squared_error(actual, predicted)
    rmse = mse ** 0.5
    mae = mean_absolute_error(actual, predicted)
    return mse, rmse, mae
