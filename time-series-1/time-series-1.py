# %%
# imports

import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller

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
# Try different levels of difference and plot with rolling numbers

passengers['#Pass One Diff'] = passengers['#Passengers'].diff()
passengers['#Pass One Diff_rolling mean'] = passengers['#Pass One Diff'].rolling(12).mean()
passengers['#Pass One Diff_rolling std'] = passengers['#Pass One Diff'].rolling(12).std()
passengers[['#Pass One Diff', '#Pass One Diff_rolling mean', '#Pass One Diff_rolling std']].plot()

# with one order of diff, the results are not stationary -- mean is constant but not variance, autocovariance is seasonal like raw numbers

# %%
# Try with two orders of diff

passengers['#Pass Two Diff'] = passengers['#Passengers'].diff().diff()
passengers['#Pass Two Diff_rolling mean'] = passengers['#Pass Two Diff'].rolling(12).mean()
passengers['#Pass Two Diff_rolling std'] = passengers['#Pass Two Diff'].rolling(12).std()
passengers[['#Pass Two Diff', '#Pass Two Diff_rolling mean', '#Pass Two Diff_rolling std']].plot()

# One order of difference makes the mean constant so there is no need to go through using two orders since we lose data and do not gain any information over using one order

# %%
# Try logging data to smooth variance

passengers['#Pass_logged'] = np.log(passengers['#Passengers'])
passengers['#Pass_logged_diff'] = passengers['#Pass_logged'].diff()
passengers['#Pass_logged_diff_rolling mean'] = passengers['#Pass_logged_diff'].rolling(12).mean()
passengers['#Pass_logged_diff_rolling std'] = passengers['#Pass_logged_diff'].rolling(12).std()
passengers[['#Pass_logged_diff','#Pass_logged_diff_rolling mean','#Pass_logged_diff_rolling std']].plot()

# Now both mean and variance are constant, but we still have seasonality that needs to be addressed

# %%
# Seasonal variation is roughly 12 months apart, see if diff(12) smooths out

passengers['#Pass_stationary'] = passengers['#Pass_logged_diff'].diff(12)
passengers['#Pass_stat_one_rolling mean'] = passengers['#Pass_stationary'].rolling(12).mean()
passengers['#Pass_stat_one_rolling std'] = passengers['#Pass_stationary'].rolling(12).std()
passengers[['#Pass_stationary','#Pass_stat_one_rolling mean','#Pass_stat_one_rolling std']].plot()

# %%
# Check with second order of diff

passengers['#Pass_stationary_two'] = passengers['#Pass_logged_diff'].diff(12).diff(12)
passengers['#Pass_stat_two_rolling mean'] = passengers['#Pass_stationary_two'].rolling(12).mean()
passengers['#Pass_stat_two_rolling std'] = passengers['#Pass_stationary_two'].rolling(12).std()
passengers[['#Pass_stationary_two','#Pass_stat_two_rolling mean','#Pass_stat_two_rolling std']].plot()

# %%
# Check ad fuller value

ad_results = adfuller(passengers['#Pass_stationary'].dropna())
ad_results

# P value of 0.000248 is sufficient

# %%
# check ad fuller value with second order of difference, assignment calls to check difference levels with transformed data

ad2_results = adfuller(passengers['#Pass_stationary_two'].dropna())
ad2_results
