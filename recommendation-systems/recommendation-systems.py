# %% [markdown]
# # recommendation-systems
#
# Write a function that recommends 5 beauty products for each user based on popularity among other users.
#
# Write a function that recommends 5 beauty products for each user based on next items purchased by other users.

# %% [markdown]
# pd.read_json
#
# lines=True

# %%
import pandas as pd
import numpy as np
import random

# %%
# Read data

beauty_df = pd.read_json('Beauty.json', lines=True)

# %%
# head check

beauty_df.head()

# %%
# Make new df with only columns to use

pop_df = beauty_df[['overall', 'reviewerID', 'asin']]

pop_df.head()

# %%
# Check for how many unique products

pop_df['asin'].nunique()

# %%
# Make new dataframe grouped by each product with size mean and sum of ratings for each product, for ranking popularity

grouped_pop = pop_df.groupby('asin').agg({'overall' : [np.size, np.mean, np.sum]})
grouped_pop.head()

# %%
# Sort to see what is most "popular"

grouped_pop.sort_values(('overall', 'sum'), ascending=False)


# %%
# Assign ranks to all products based on aggregated popularity values

grouped_pop['rank'] = grouped_pop[('overall', 'sum')].rank(ascending=False)

# %%
# sort by rank

grouped_pop.sort_values(by='rank', ascending=True).head(50)

# %%
# Make function to return top 5 most popular products for recommendation, do not include products someone has already reviewed

def popularity(reviewer_id, pop_df, df, n_recs):
  reviewed = pop_df.loc[pop_df['reviewerID'] == reviewer_id, 'asin']
  not_reviewed = df[~df.index.isin(reviewed)]
  top_n = not_reviewed.sort_values(by='rank', ascending=True).head(n_recs)
  top_n = top_n.reset_index()
  most_pop = pd.DataFrame({
    'asin' : top_n['asin'],
    'average_rating' : top_n[('overall', 'mean')],
    'rank' : top_n['rank']
  })
  return most_pop


# %%
# test function

popularity('A3PQ3YQZYJ66HK', pop_df, grouped_pop, 5)

# %%
# Create dataframe with timestamp information to start building recommendations based on last reviewed product

reviewed = beauty_df[['reviewerID', 'asin', 'overall', 'unixReviewTime']]
reviewed.head()

# %%
# Sort values so IDs are grouped and sorted by time

reviewed = reviewed.sort_values(by=['reviewerID', 'unixReviewTime', 'asin'], ascending=True)
reviewed.head(10)

# %%
# make empty column for next product reviewed

reviewed['next_product'] = np.nan
reviewed.head()

# %%
# Loop over all products reviwed and add next product reviewed for each client to the new product column

for i, product in enumerate(reviewed['asin'][:-1]):
  if reviewed.iloc[i]['reviewerID'] == reviewed.iloc[i+1]['reviewerID']:
    reviewed.loc[reviewed.index[i], 'next_product'] = reviewed.iloc[i+1]['asin']

reviewed[50:100]

# %%
# Take a look at value counts for a specific product to test and see what the next top reviewed products are

reviewed.loc[reviewed['asin'] == 'B0012Y0ZG2', 'next_product'].value_counts()

# %%
# Function to return the next top products based on a spefiic product

def rec_next_prod(ordered_next_df, product, n_recs=None) -> pd.Series:
  """
  Enter ASIN in quotes, plus a number (n). This will return the N products reviewed after the ASIN that was entered

  I.E -- Enter B0012Y0ZG2 and the number 5, you will get a list of the 5 most common movies watched after Star Wars (1977)
  """
  rec_prod =  ordered_next_df.loc[ordered_next_df['asin'] == product, 'next_product'].value_counts()
  if n_recs is not None:
    rec_prod = rec_prod.head(n_recs)
  return rec_prod

# %%
# Test function

rec_next_prod(reviewed, 'B0012Y0ZG2', 5)

# %%
# Make function to recommend next 5 products based on user and product reviewed

def rec_for_user(reviewer_id, n_recs, ordered_next_df):
  user_prods = ordered_next_df.loc[ordered_next_df['reviewerID'] == reviewer_id]
  last_prod = user_prods.sort_values(by='unixReviewTime')['asin'].tail(1).values[0]
  next_prod = rec_next_prod(ordered_next_df, last_prod, n_recs=None)
  next_prod = next_prod[~next_prod.index.isin(user_prods['asin'])]
  return next_prod.head(n_recs)

# %%
# Test function

rec_for_user('A12BLGAAZBUU96', 5 , reviewed)

# %%
# Make function that combines both, gives top 5 most reviewed first if they have reviewed already, gives most popular if they have not

def full_rec(reviewer_id, n_recs, ordered_next_df):
  if reviewer_id in ordered_next_df['reviewerID'].values:
    return rec_for_user(reviewer_id, n_recs, ordered_next_df)
  else:
    return popularity(reviewer_id, pop_df, grouped_pop, n_recs)

# %%
# test with unknown user ID

full_rec('test', 5, reviewed)

# %%
# test with known user ID

full_rec('A12BLGAAZBUU96', 5, reviewed)

# %%
