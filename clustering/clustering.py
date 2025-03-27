# %%
# imports

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import numpy as np

from sklearn import set_config
set_config(transform_output='pandas')

import plotly.express as px

from sklearn.metrics import silhouette_score

from sklearn.neighbors import NearestNeighbors

from sklearn.cluster import DBSCAN


# %%
# read file

import_85 = pd.read_csv('imports-85.data', header=None)
import_85.head()

# %%
# retitle columns to use

import_85 = import_85.rename(columns={21:'horsepower', 25:'price'})
import_85.head()

# %%
# check for dupes

import_85.duplicated().sum()

# %%
# pick columns to use

for_model = import_85[['horsepower', 'price']]
for_model.head()

# %%
# info check

for_model.info()

# %%
# Data type is object but they should be numbers do value checks

for_model['price'].value_counts()

# %%
for_model['horsepower'].value_counts()

# %%
# Replace ? with nan

for_model['horsepower'] = for_model['horsepower'].replace('?', np.nan)
(for_model['horsepower'] == '?').sum()


# %%
# change datatype to numeric

for_model['horsepower'] = for_model['horsepower'].astype('float')

# %%
# compute mean and impute

hp_mean = for_model['horsepower'].mean()
for_model['horsepower'] = for_model['horsepower'].fillna(hp_mean)

# %%
# Replace price ? with nan

for_model['price'] = for_model['price'].replace('?', np.nan)
(for_model['price'] == '?').sum()

# %%
# change datatype to numeric

for_model['price'] = for_model['price'].astype('float')

# %%
# compute mean and impiute for nan

price_mean = for_model['price'].mean()
for_model['price'] = for_model['price'].fillna(price_mean)

# %%
# check all work above

for_model.info()

# %%
# scale numbers for model

scaled_df = StandardScaler().fit_transform(for_model)

scaled_df.head()

# %%
# make model with scaled data

kmeans = KMeans(n_clusters=2, random_state=42)

kmeans.fit(scaled_df)

# %%
# Create dataframe with cluster column for charts

charter = scaled_df.copy()

charter['cluster'] = kmeans.labels_

charter.head()

# %%
# Plot clusters

plt.scatter(charter['horsepower'], charter['price'], c=charter['cluster'])

# %%
# Make loop to check for best value of k

ks = range(2,16)
s_scores = []
inertias = []

for k in ks:
  kmeans = KMeans(n_clusters=k)
  kmeans.fit(scaled_df)
  s_scores.append(silhouette_score(scaled_df, kmeans.labels_))
  inertias.append(kmeans.inertia_)


# %%
##Plot variables above to visualize best values of K

fig, axes = plt.subplots(1, 2, figsize=(10, 5))

axes[0].plot(ks, inertias)
axes[0].set_title('Inerts/k')

axes[1].plot(ks, s_scores)
axes[1].set_title('Silhos/k')

# %%
# add cluster centers to cluster plot above

kmeans6 = KMeans(n_clusters=6, random_state=42).fit(scaled_df)
plt.scatter(charter['horsepower'], charter['price'], c=charter['cluster'])
plt.scatter(kmeans6.cluster_centers_[:,0], kmeans6.cluster_centers_[:,1], marker='d')

# %%
# Generate DB Scan model -- first determine min sample and epsilon

# Determine distance between each point and the next three closest (4 neighbors means reference point plus three closest -- 4 neighbors)

min_samples = 4
neighbors = NearestNeighbors(n_neighbors=min_samples)
neighbors.fit(scaled_df)
distances, indices = neighbors.kneighbors(scaled_df)
distances

# %%
# make array with furthest point from each datapoint above -- each row above is the distances to each point in the cluster, array below plots this out

n_th_neighbor = distances[:, min_samples -1]
n_th_neighbor

# %%
# sort values for plotting

n_th_neighbors_sorted = np.sort(n_th_neighbor)
n_th_neighbors_sorted

# %%
# Plot with epsilon to visualize

epsilon = .77
plt.plot(n_th_neighbors_sorted)
plt.ylabel(f'distance to {min_samples}th neighbor')
plt.xlabel('sorted data points')
plt.axhline(y=epsilon, color='r')
plt.grid()

# %%
# Create dbscan model

dbs = DBSCAN(eps=epsilon, min_samples=min_samples).fit(scaled_df)

# %%
# Check how many clusters there are

np.unique(dbs.labels_)

# there are three clusters -- -1 is noise, 0 and 1 are the others

# %%
# Plot to visualize outliers

plt.scatter(scaled_df.iloc[:,0], scaled_df.iloc[:,1], c=dbs.labels_)
