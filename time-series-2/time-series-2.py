# %%
# imports

import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.model_selection import train_test_split
from statsmodels.tsa.stattools import adfuller
from sklearn.metrics import root_mean_squared_error
import pmdarima as pm
import numpy as np


# %%
# read and head check

passengers = pd.read_csv('AirPassengers.csv')
passengers.head()

# %%
# Convert appropriate column to datetime and info check dtype

passengers['Month'] = pd.to_datetime(passengers['Month'])
passengers.info()

# %%
# change index to datetime column

passengers = passengers.set_index('Month')

# %%
# Sort index ascending to make chronological

passengers.sort_index(inplace=True, ascending=True)

# %%
# look at frequency

passengers.index

# %%
# Update frequency pn pandas object to monthly

passengers.index.freq="MS"
passengers.index

# %%
# Make rolling std dev and mean colukns for plot

passengers['rolling_mean12'] = passengers['#Passengers'].rolling(12).mean()
passengers['rolling_std12'] = passengers['#Passengers'].rolling(12).std()
passengers

# %%
# Make plot using new columns above

passengers.plot()

# Data is NOT stationary

# %%
# Add diff columns to smooth mean

passengers['#Pass One Diff'] = passengers['#Passengers'].diff()
passengers['#Pass One Diff_rolling mean'] = passengers['#Pass One Diff'].rolling(12).mean()

# %%
# Log data to take diff and smooth variance

passengers['#Pass_logged'] = np.log(passengers['#Passengers'])
passengers['#Pass_logged_diff'] = passengers['#Pass_logged'].diff()
passengers['#Pass_logged_diff_rolling mean'] = passengers['#Pass_logged_diff'].rolling(12).mean()
passengers['#Pass_logged_diff_rolling std'] = passengers['#Pass_logged_diff'].rolling(12).std()
passengers[['#Pass_logged_diff','#Pass_logged_diff_rolling mean','#Pass_logged_diff_rolling std']].plot()

# %%
# Seasonal exists, use seasonal diff to smooth

passengers['#Pass_stationary'] = passengers['#Pass_logged_diff'].diff(12)
passengers['#Pass_stat_seadiff_rolling mean'] = passengers['#Pass_stationary'].rolling(12).mean()
passengers['#Pass_stat_seadiff_rolling std'] = passengers['#Pass_stationary'].rolling(12).std()
passengers[['#Pass_stationary','#Pass_stat_seadiff_rolling mean','#Pass_stat_seadiff_rolling std']].plot()

# %%
#Check AD Fuller to make sure it is stationary

ad_results = adfuller(passengers['#Pass_stationary'].dropna())
ad_results


# %%
# Plot ACF -- Q value is 1 1 because the very first lag on the plot is outside of the confidence intervals and is cutoff at the second lag

plot_acf(passengers['#Pass_stationary'].dropna());

# %%
# Plot PACF -- P value is 1 because the very first lag on the plot is outside of the confidence intervals and is cutoff at the second lag

plot_pacf(passengers['#Pass_stationary'].dropna());

# %%
# Set values for pdq

p = 1
d = 0
q = 1

# %%
# train test split

train, test = train_test_split(passengers['#Pass_stationary'], test_size=12, shuffle=False)
display(train.tail())
display(test.head())

# %%
# Make model

model1_0_1 = ARIMA(train, order=(p, d, q))


# %%
# Fit model and display results

results = model1_0_1.fit()
results.summary()

# %%
# Generate forecasts

forecast_12_year = results.forecast(steps=len(test))
forecast_12_year


# %%
# Make dataframe to plot results

test_results = pd.DataFrame(columns=['test', 'test_pred'])
test_results['test'] = test
test_results['test_pred'] = forecast_12_year

# %%
# Show plot

test_results.plot()

# %%
# Get RMSE

print('RMSE', root_mean_squared_error(test_results['test'], test_results['test_pred']))

# %%
# Try Auto model to find best combo of PQE

aut_arim = pm.AutoARIMA(start_p=0, max_p=5, start_d=0, max_d=2, start_q=0, max_q=5, seasonal=False,
                        random_state=42, stepwise=False, suppress_warnings=True,
                        max_order=None)

aut_arim.fit(train.dropna())

# %%
# See what params were used for PDQ (3, 0, 2)

aut_arim.model_.get_params()

# %%
# Fit model and pull summary

model = aut_arim.model_
pm_results = model.fit(train)
pm_results.summary()

# %%
# Make predictions

pm_test_pred, confs = model.predict(n_periods=len(test), return_conf_int=True)
pm_test_pred

# %%
# Make dataframe to plot results

pm_test_results = pd.DataFrame(columns=['test', 'pm_test_pred'])
pm_test_results['test'] = test
pm_test_results['pm_test_pred'] = pm_test_pred

# %%
# SHow both RMSEs for comparison

print(f'Self-Picked RMSE - {root_mean_squared_error(test_results['test'], test_results['test_pred'])}')
print(f'Auto RMSE - {root_mean_squared_error(pm_test_results['test'], pm_test_results['pm_test_pred'])}')

# %%
# Use sarimax on data that hasn't been adjusted for seasonality

seas_train, seas_test = train_test_split(passengers['#Pass_logged_diff'], test_size=12, shuffle=False)
display(seas_train.tail())
display(seas_test.head())

# %%
# Make and fit seasonal model

seas_model = SARIMAX(seas_train, order=(p,d,q), seasonal_order=(p,d,q,12))
seas_results = seas_model.fit()
seas_results.summary()

# %%
# Make forecast

forecast_seas = seas_results.forecast(steps=len(test))
forecast_seas

# %%
# Make dataframe to plot

seas_test_results = pd.DataFrame(columns=['test', 'seas_test_pred'])
seas_test_results['test'] = seas_test
seas_test_results['seas_test_pred'] = forecast_seas

# %%
# Plot forecast

seas_test_results.plot()

# %%
# Show all three RMSE for comparison

print(f'Self-Picked RMSE - {root_mean_squared_error(test_results['test'], test_results['test_pred'])}')
print(f'Auto RMSE - {root_mean_squared_error(pm_test_results['test'], pm_test_results['pm_test_pred'])}')
print(f'Seasonal Model RMSE - {root_mean_squared_error(seas_test_results['test'], seas_test_results['seas_test_pred'])}')


# %%
# All metrics are better for SARIMAX model
