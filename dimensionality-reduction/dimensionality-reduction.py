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
# Make scaler for pipeline

scaler = StandardScaler()


# %%
# make model, pipeline and fit pipeline

knn_nopca = KNeighborsClassifier()
knn_nopca_pipe = make_pipeline(scaler, knn_nopca)
knn_nopca_pipe.fit(X_train, y_train)

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

knn_pca_pipe.fit(X_train, y_train)

# %%
# Check scores for PCA pipeline

scores.loc['pca_knn - 90%', 'test_accuracy'] = knn_pca_pipe.score(X_test, y_test)
scores.loc['pca_knn - 90%', 'train_accuracy'] = knn_pca_pipe.score(X_train, y_train)
scores

# %%
# Look for ideal number of components

plt.plot(pca.explained_variance_ratio_)
plt.grid()

# %%
# Use loop in increments of 5 to go over above for highest accuracy score

components = range(1,175,5)
score_check = []

for component in components:
  pca = PCA(n_components = component)
  knn_pca = KNeighborsClassifier()
  pca_pipe = make_pipeline(scaler, pca, knn_pca)
  pca_pipe.fit(X_train, y_train)
  test_score = pca_pipe.score(X_test, y_test)
  train_score = pca_pipe.score(X_train, y_train)
  score_check.append((component, test_score, train_score))

score_df = pd.DataFrame(score_check, columns=['component #', 'test_accuracy', 'train_accuracy'])

# %%
# Show list and sort by highest test score, top 10 results

score_df.sort_values(ascending=False, by='test_accuracy').head(10)\

# 51 components is the highest accuracy and lowest bias

# %%
