# %%
import pandas as pd
import numpy

# %%
stroke_data = pd.read_csv("healthcare-dataset-stroke-data.csv")
stroke_data

# %%
#1 Use .describe() to compute a variety of statistics on the whole data set at once.

stroke_data.describe()

# %%
#2 Filter .describe() to only compute statistics on factors with floating point number values.

stroke_data.describe(include='float64')

# %%
#3 Use .groupby() to create a data frame grouping by the "stroke" factor.

stroke_factor_grp = stroke_data.groupby('stroke')
stroke_factor_grp

# %%
#4 Use the "stroke" grouping to get only group where "stroke" is 1

stroke1_grp = stroke_factor_grp.get_group(1)
stroke1_grp

# %%
#5 Use .describe() to compute statistics on factors with floating point values for the data where "stroke" is 1.

stroke1_grp.describe(include='float64')

#could also use  -- stroke_factor_grp.get_group(1).describe(include='float64') -- if a new variable wasn't the best route

# %%
#6 Filter .describe() to only compute statistics on factors with integer values, removing as much percentile data as possible.

stroke1_grp.describe(include='int')

# %%
#7 Create a data frame grouping by both the "hypertension" and "heart_disease" factors

heart = stroke1_grp.groupby(['hypertension', 'heart_disease'])

# %%
#Get the group where both "hypertension" and "heart_disease" are 1.

with_heart = heart.get_group((1, 1))
with_heart

# %%
#Count the number of "id"s per group

stroke_data.groupby('stroke')[['hypertension', 'heart_disease']].value_counts()


# %%
#10 Aggregate both the mean and standard deviation of "stroke" per group

# Hypertension - stroke mean

# What do I think this means? Per teh observations, 13.2530% of those who have hypertension have also had a stroke, and 3.9679% of those without hypertension have also had a stroke

stroke_data.groupby("hypertension")['stroke'].mean()


# %%
# Heart Disease - stroke mean

# For

stroke_data.groupby('heart_disease')['stroke'].mean()


# %%

# Hypertension - stroke st dev

stroke_data.groupby('hypertension')['stroke'].std()

# %%
# Heart Disease - stroke st dev

stroke_data.groupby('heart_disease')['stroke'].std()
