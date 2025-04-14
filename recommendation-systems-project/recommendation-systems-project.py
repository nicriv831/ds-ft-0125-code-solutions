# %% [markdown]
# # Imports

# %%
# Imports

import pandas as pd
import numpy as np
import scipy.sparse as sp
from sklearn.neighbors import NearestNeighbors

# %% [markdown]
# # Initial Read

# %%
# PD read

recipes = pd.read_csv('Data/RAW_interactions.csv', usecols=[0,1,3])

# %%
# Head check

recipes.head()

# %%
# Info/shape check

recipes.info()
print(recipes.shape)

# no nulls - three columns - 1,132,367 rows

# %%
# Dupe check

recipes.duplicated().sum()

# no dupes

# %%
# How many unique user id - 226570

recipes['user_id'].nunique()


# %%
# How many unique recipe id - 231637

recipes['recipe_id'].nunique()


# %% [markdown]
# _Upon first glance, sampling 10% of the dataset would leave us with approx. 20,000 unique user IDs and 20,000 unique recipe IDs. Upon attempting to create recommendation models using the truncated dataset, was unable to find a way that didn't result in the kernel crashing or much too much data for computer memory._
#
# **Due to this I will use a nearest neighbors algorithm to find similarities on the fly within the function, rather than creating a covariance matrix for every user and recipe in advance**

# %%
# Create dictionaries with user/recipe IDs and their indices

user_indices = {u: i for i, u in enumerate(recipes['user_id'].unique())}
recipe_indices = {r: i for i, r in enumerate(recipes['recipe_id'].unique())}

# Pull out rows, cols and ratings for creation of sparse matrix

rows = [user_indices[u] for u in recipes['user_id']]
cols = [recipe_indices[r] for r in recipes['recipe_id']]
ratings = recipes['rating'].values

# %%
# Create sparse matrix

matrix = sp.csr_matrix((ratings, (rows, cols)),
                           shape=(len(user_indices), len(recipe_indices)))


# %%
# Fit nearest neighbors model for item-item similarity

items_nn_model = NearestNeighbors(n_neighbors=50, metric='cosine', algorithm='brute')
items_nn_model.fit(matrix.T)


# %%
# Build nearest neighbors model for user-user similarity

user_nn_model = NearestNeighbors(n_neighbors=50, metric='cosine', algorithm='brute')
user_nn_model.fit(matrix)

# %%
# Get recommendations for a specific user

def recommend_for_user(n_recommendations=3):

     # Prompt user for their user ID
    user_id_input = input("Please enter your user ID: ").strip()

    #Convert to int
    user_id = int(user_id_input)

    # Check if the user ID exists in user_indices
    if user_id not in user_indices:
        print(f"User ID {user_id} not found. Please enter a valid user ID.")
        return None

    user_idx = user_indices[user_id]
    user_ratings = matrix[user_idx].toarray().flatten()
    rated_items = np.where(user_ratings > 0)[0]

    # Get similar items to those the user has rated highly
    similar_items = []
    for item_idx in rated_items:
        if user_ratings[item_idx] >= 4:
            distances, indices = items_nn_model.kneighbors(matrix.T[item_idx].reshape(1, -1))
            similar_items.extend([(idx, user_ratings[item_idx] * (1 - dist))
                                 for dist, idx in zip(distances[0], indices[0])
                                 if idx not in rated_items])

    # Sort by similarity
    similar_items.sort(key=lambda x: x[1], reverse=True)

    # Get top rec
    top_recs = similar_items[:n_recommendations]

    # Create DataFrame
    recipe_ids = [list(recipe_indices.keys())[rec[0]] for rec in top_recs]
    similarity_scores = [rec[1] for rec in top_recs]

    recommendations_df = pd.DataFrame({
        'recipe_id': recipe_ids,
        'similarity_score': similarity_scores
    })

    return recommendations_df

# %%
recommend_for_user()

# %%
