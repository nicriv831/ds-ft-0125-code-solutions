# Recommendation System Project

## Table of Contents

1. [Introduction](#introduction)
2. [Data](#data)
3. [Process Outline](#process-outline)
   1. [Initial Observation/Clean](#clean-data)
   2. [Preprocess Data for Model](#preprocess-data-for-model)
   3. [Model Analysis/Prediction](#model-prediction/analysis)
4. [Next Steps](#next-steps)
5. [References](#references)

## 1 - Introduction <a name="introduction"></a>

I used item-item similarity scores on a dataset of recipe reviews from food.com to come up with recipe recommendations for the user.

## 2 - Data <a name="data"></a>

The data was downloaded from https://cseweb.ucsd.edu/~jmcauley/datasets.html#foodcom. It is a set with user reviews of recipes from food.com (and also Geniues Kitchen, which eventually turned into food.com)

## 3 - Process Outline <a name="process-outline"></a>

My process consisted of trying the mnay different ways to use such a large dataset for an item-item similairty martrix. I found success by foregoing a similiarity matrix up front. Instead, I chose to use a nearest neighbors algorithm on a sparse matrix to determine similairty scores on the fly as the user was input.

The downside to this method is the calculation time increases a bit. However, my opther methdos were not successful in generating a prediciton as the kernal crashes or my memory wa not sifficient to proceed.

### 3i - Initial Observations/Clean <a name="clean-data"></a>

The dataset consists of approximately 1.13 million recipe reviews. There are approximately 226,000 unique users and appriximately 230,000 unique recipes.

There are no duplicates and no nulls in the raw data.

### 3ii - Preprocess Data for Model <a name="preprocess-data-for-model"></a>

To try and get around the size of the dataset, I first removed recipes with 11 or less reviews. I ended up with approximately 550,000 rows of information, but still kept 90% of the recipe IDs.

However, this created problems as there were too many recipes left to create a matrix.

My next move was to take a random sample of 10% of the data. This resultred in approximately 25,000 users and recipes respectively. The resulting matrix was still too large for the kernal/computer memory. I decided to use a nearest neighbors algorithm to calculate similarities and use this within my recommendation function to make recs on the fly using similar items, rather than calculating the matrix ahead of time.

### 3iii - Model Analysis/Prediction <a name="model-prediction/analysis"></a>

Once the method of reducing data complexity was resolved, I created a function that allows user to enter their user ID and get three similar recipes recommended in return.

## 4 - Next Steps <a name="next-steps"></a>

1. See if there is a way to make faster predictions than with a nearest neigbors model
2. Try an SVD reduction to see if this comes up with a faster prediciton
3. Add recipe names to recommendations

## References <a name="references"></a>

**Food Review Dataset** Generating Personalized Recipes from Historical User Preferences Bodhisattwa Prasad Majumder*, Shuyang Li*, Jianmo Ni, Julian McAuley EMNLP, 2019

Claude 3.7 Sonnet
