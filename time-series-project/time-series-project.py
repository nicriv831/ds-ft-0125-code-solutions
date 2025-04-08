# %% [markdown]
# # RDDT Time Series Analysis

# %% [markdown]
# ## Imports

# %%
# Imports

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import yfinance as yf
from pandas.tseries.offsets import CustomBusinessDay
import pandas_market_calendars as mcal
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from sklearn.model_selection import train_test_split
from statsmodels.tsa.arima.model import ARIMA
import pmdarima as pm
from sklearn.metrics import root_mean_squared_error
import itertools
import warnings
warnings.filterwarnings('ignore')

# %% [markdown]
# ## EDA

# %% [markdown]
# ### Initial Data Checks

# %%
# Make ticker object

rddt = yf.Ticker('RDDT')

# %%
# Dataframe with prices

prices = rddt.history(period='1y', interval='1d')
prices.info()

# %%
# head check

prices.head(25)

# %%
# Make df with only close prices

close_prices = prices[['Close']]

# %%
#head check

close_prices.head(50)

# %%
# Set custom frequency to account for holidays and business days

from pandas.tseries.offsets import CustomBusinessHour
nyse = mcal.get_calendar('NYSE')
market_holidays = nyse.holidays().holidays
cbd = CustomBusinessDay(holidays=market_holidays)
close_prices.index.freq = cbd

# %%
#info check

close_prices.info()

# %%
# Plot prices

close_prices.plot()

# %% [markdown]
# ### Stationarity

# %% [markdown]
# #### Mean and Variance

# %%
# Log close price to smooth variance, and difference logged prices to smooth mean

close_prices['close_log'] = np.log(close_prices['Close'])
close_prices['close_diff_log'] = close_prices['close_log'].diff()

# %%
# Check rolling average and std dev for constant

close_prices['rolling_mean_7'] = close_prices['close_diff_log'].rolling(7).mean()
close_prices['rolling_std_7'] = close_prices['close_diff_log'].rolling(7).std()
close_prices[['close_diff_log', 'rolling_mean_7', 'rolling_std_7']].plot()

# %%
# Head check

close_prices.head(20)

# %%
# Check ad fuller for stationary

close_adf = adfuller(close_prices['close_diff_log'].dropna())
close_adf

# %% [markdown]
# #### Seasonality

# %%
# Check for seasonal variation - make weekly monthly and quarterly period objects

season_check_week = seasonal_decompose(close_prices['close_log'], period = 5)
season_check_mnth = seasonal_decompose(close_prices['close_log'], period = 21)
season_check_qtr = seasonal_decompose(close_prices['close_log'], period = 63)


# %% [markdown]
# _**Plot isn't able to be resized on its own, need to manually make so it can be resized for readability**_
#

# %%
# Weekly

fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(16, 10), sharex=True)

season_check_week.observed.plot(ax=ax1)
ax1.set_ylabel('Observed')
ax1.set_title('Seasonal Decomposition')

season_check_week.trend.plot(ax=ax2)
ax2.set_ylabel('Trend')

season_check_week.seasonal.plot(ax=ax3)
ax3.set_ylabel('Seasonal')

season_check_week.resid.plot(ax=ax4)
ax4.set_ylabel('Residual')

plt.tight_layout();


# %% [markdown]
# _**Magnitude of "seasonal" moves is de minimis**_

# %%
# Monthly

fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(16, 10), sharex=True)

season_check_mnth.observed.plot(ax=ax1)
ax1.set_ylabel('Observed')
ax1.set_title('Seasonal Decomposition')

season_check_mnth.trend.plot(ax=ax2)
ax2.set_ylabel('Trend')

season_check_mnth.seasonal.plot(ax=ax3)
ax3.set_ylabel('Seasonal')

season_check_mnth.resid.plot(ax=ax4)
ax4.set_ylabel('Residual')

plt.tight_layout();

# %% [markdown]
# _**Magnitude of "seasonal" moves is de minimis**_

# %%
# Quarterly

fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(16, 10), sharex=True)

season_check_qtr.observed.plot(ax=ax1)
ax1.set_ylabel('Observed')
ax1.set_title('Seasonal Decomposition')

season_check_qtr.trend.plot(ax=ax2)
ax2.set_ylabel('Trend')

season_check_qtr.seasonal.plot(ax=ax3)
ax3.set_ylabel('Seasonal')

season_check_qtr.resid.plot(ax=ax4)
ax4.set_ylabel('Residual')

plt.tight_layout();

# %% [markdown]
# _**Magnitude of "seasonal" moves is de minimis**_

# %% [markdown]
# ### Modeling

# %% [markdown]
# #### ACF/PACF Plots

# %%
# Plot ACF to find value of Q for model

plot_acf(close_prices['close_diff_log'].diff().dropna());

# Q equals 1

# %%
# Plot PACF to find value of P for model

plot_pacf(close_prices['close_diff_log'].diff().dropna());

# P equals 6

# %%
# Set Values for models

p = 6
d = 1
q = 1

# %% [markdown]
# #### Fit and Analyze

# %%
# Train test split, using logged but undifferenced prices

train_log, test_log = train_test_split(close_prices['close_log'], test_size=50, shuffle=False)
display(train_log.tail())
display(test_log.head())

# %%
# fit model with parameters above

model6_1_1 = ARIMA(train_log, order=(p, d, q))
results = model6_1_1.fit()
results.summary()

# %%
# Make forecast

forecast = results.forecast(steps=len(test_log))
forecast

# %%
# Make dataframe for charting and comparison

test_results = pd.DataFrame(columns=['test', 'test_pred'])
test_results['test'] = np.exp(test_log)
test_results['test_pred'] = np.exp(forecast)
test_results.plot()


# %%
# make table with results

rmse_results = pd.DataFrame(columns=['model', 'rmse'])
rmse_results.loc[len(rmse_results)] = ['6/1/1 ARIMA', root_mean_squared_error(forecast, test_log)]
rmse_results

# %% [markdown]
# _**Forecasts are a stright line and don't look to be fit correctly. Will try some other options to get better forecasts**_

# %%
# Use autoArima to find best PDQ combination

pmarima = pm.AutoARIMA(start_p=0, max_p=12, start_d=0, max_d=3, start_q=0, max_q=8, seasonal=False,
                        random_state=42, stepwise=False, suppress_warnings=True,
                        max_order=None)
auto_fitted = pmarima.fit(train_log.dropna())

# %%
# Check params for best combo

auto_fitted.model_.get_params()

# %%
# Check summary

auto_fitted.summary()

# %%
# Make predictions and confidence interval for auto fitted

auto_test_pred, confs = auto_fitted.model_.predict(n_periods=len(test_log), return_conf_int=True)
auto_test_pred

# %%
# Plot predictions and actual numbers from auto ARIMA

auto_test_results = pd.DataFrame(columns=['test_log', 'auto_test_pred'])
auto_test_results['test_log'] = np.exp(test_log)
auto_test_results['auto_test_pred'] = np.exp(auto_test_pred)
auto_test_results.plot()

# %%
# Add auto ARIMA RMSE to RMSE table

rmse_results.loc[len(rmse_results)] = ['2/1/0 autoARIMA', root_mean_squared_error(auto_test_pred, test_log)]
rmse_results

# %% [markdown]
# _**Both versions (brute force PDQ and auto-ARIMA) gave forecasts that were not in line with the actual results. Will run a loop over various combinations of PDQ to determine if there is a version out there with a better RMSE**_

# %%
# Make P and Q ranges thru 9, D thru 2
p_values = range(0, 10)
d_values = range(0, 3)
q_values = range(0, 10)

# Make empty lists for saving results
best_rmse = float('inf')
best_params = None
results = []

# Loop through combos

for p, d, q in itertools.product(p_values, d_values, q_values):
    try:
        # Fit ARIMA model
        model = ARIMA(train_log, order=(p, d, q))
        model_fit = model.fit()

        # Make forecast
        forecast = model_fit.forecast(steps=len(test_log))

        # Calculate RMSE
        rmse = root_mean_squared_error(test_log, forecast)

        # Save results
        results.append({
            'p': p,
            'd': d,
            'q': q,
            'rmse': rmse
        })

        # Tag best model
        if rmse < best_rmse:
            best_rmse = rmse
            best_params = (p, d, q)

        print(f"ARIMA({p},{d},{q}) - RMSE: {rmse:.4f}, AIC: {model_fit.aic:.2f}")

    except Exception as e:
        print(f"ARIMA({p},{d},{q}) - Error: {str(e)}")
        continue

# Create DataFrame of results
results_df = pd.DataFrame(results)
results_df = results_df.sort_values('rmse')

print(f"BEST MODEL: ARIMA{best_params} with RMSE of {best_rmse:.4f}")


# Fit best model and plot forecast vs actual
best_model = ARIMA(train_log, order=best_params)
best_model_fit = best_model.fit()
forecast = best_model_fit.forecast(steps=len(test_log))


# %%
# Plot best model vs actual results with exponentiated targets and predictions

plt.figure(figsize=(12, 6))
plt.plot(test_log.index, np.exp(test_log), label='Actual')
plt.plot(test_log.index, np.exp(forecast), label='Forecast', color='red')
plt.title(f'Forecast vs Actual - ARIMA{best_params}')
plt.legend()
plt.show()

# %% [markdown]
# _**This set of predictions moves in the same direction as the actual prices and has the lowest RMSE of all the tested iterations**_

# %%
# look at dataframe with RMSE results

results_df.head(50)

# %%
# Look at forecasts

np.exp(forecast)

# %%
# add results to RMSE dataframe for comparison

rmse_results.loc[len(rmse_results)] = ['2/2/0 ARIMA', root_mean_squared_error(forecast, test_log)]

# %%
# SHow RMSE list

rmse_results.sort_values(by='rmse', ascending=True)
