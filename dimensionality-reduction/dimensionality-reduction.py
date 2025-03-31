# %%
import pandas as pd
import numpy as np

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

from sklearn import set_config
set_config(transform_output='pandas')

from sklearn.model_selection import train_test_split

from sklearn.neighbors import KNeighborsClassifier

from sklearn.pipeline import make_pipeline

import matplotlib.pyplot as plt

# %%
# read data

mnist = pd.read_csv('mnist.csv')

# %%
# head check

mnist.head()

# %%
# info check

mnist.info()

# %%
# dupe check

mnist.duplicated().sum()

# %%
# null check

mnist.isna().sum().sum()

# %%
# train test split

X = mnist.drop(columns='label')
y = mnist['label'].copy()

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# %%
# head check

X_train.head()

# %%
# Scale data

scaler = StandardScaler()
x_train_scaled = scaler.fit_transform(X_train)

# %%
# make model, pipeline and fit pipeline

knn_nopca = KNeighborsClassifier()
knn_nopca_pipe = make_pipeline(scaler, knn_nopca)
knn_nopca_pipe.fit(x_train_scaled, y_train)

# %%
# Run prediction to make sure the pipeline worked

knn_nopca_pipe.predict(X_test)

# %%
# Creates scores table and run scores


scores = pd.DataFrame()

scores.loc['no_pca', 'test_accuracy'] = knn_nopca_pipe.score(X_test, y_test)
scores.loc['no_pca', 'train_accuracy'] = knn_nopca_pipe.score(X_train, y_train)
scores

# %%
# Create PCA pipeline and fit data

pca = PCA(n_components=.9, random_state=42)

knn_pca = KNeighborsClassifier()

knn_pca_pipe = make_pipeline(scaler, pca, knn_pca)

knn_pca_pipe.fit(x_train_scaled, y_train)

# %%
# Check scores for PCA pipeline

scores.loc['pca_knn', 'test_accuracy'] = knn_pca_pipe.score(X_test, y_test)
scores.loc['pca_knn', 'train_accuracy'] = knn_pca_pipe.score(X_train, y_train)
scores

# %%
# Look for ideal number of components

plt.plot(pca.explained_variance_ratio_)
plt.grid()

# %%
# try with 25 components

pca_25 = PCA(n_components = 25, random_state=42)

# %%
# Make and fit 25 component pipeline

pca_25_pipe = make_pipeline(scaler, pca_25, knn_pca)
pca_25_pipe.fit(x_train_scaled, y_train)

# %%
# score 25 component pipeline

scores.loc['pca25_knn', 'test_accuracy'] = pca_25_pipe.score(X_test, y_test)
scores.loc['pca25_knn', 'train_accuracy'] = pca_25_pipe.score(X_train, y_train)
scores

# %%
# Try with 50 componets


pca_50 = PCA(n_components = 50, random_state=42)
pca_50_pipe = make_pipeline(scaler, pca_50, knn_pca)
pca_50_pipe.fit(x_train_scaled, y_train)
scores.loc['pca50_knn', 'test_accuracy'] = pca_50_pipe.score(X_test, y_test)
scores.loc['pca50_knn', 'train_accuracy'] = pca_50_pipe.score(X_train, y_train)
scores

# %%
