# %%
# initial module import

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# %%
# initial data check  - describe info shape head pairplot correlation heat map

laptops_df = pd.read_csv('Sales_data.txt')
laptops_df.head()

# %%
#shape

laptops_df.shape

# %%
#describe

laptops_df.describe()

# %%
#info

laptops_df.info()


# %%
#NaaN check

laptops_df.isna().sum()

# %%
#Dupes check

laptops_df.duplicated().sum()

# %%
# make numbers only dataframe -- I did this for heatmap sake

laptops_nums = laptops_df.select_dtypes(include='number')
laptops_nums.head()

# %%
sns.pairplot(laptops_df);

# %%
laptops_corr = laptops_nums.corr()

sns.heatmap(laptops_corr, cmap = 'icefire', annot=True);

# %% [markdown]
# # 1) What is target market? Male or female?
#
# ## ANSWER - MALE
#
# ### Though females have a higher average profit, males have a higher average profit margin AND higher total profit. This means that the business tends to profit more for every dollar they spend when a male makes a purchase AND males are also generating more absolute profit than females

# %% [markdown]
#

# %%
# Make a new column with profit margin as this is a better gauge than pure profit, will also run a plot for pure profit

laptops_df['Profit Margin - %'] = (laptops_df['Profit'] / laptops_df['Sale Price']) * 100


# %%
laptops_df.head()

# %%
# I did all the work below individually and then remembered I can put all the plots together instead of in separate cells, so I made this cell that includes everything

fig, axes = plt.subplots(1,3)

sns.barplot(data=laptops_df, x='Contact Sex', y='Profit Margin - %', estimator = np.mean, ax=axes[0])
axes[0].set_title('Avg Profit Margin by Sex')

sns.barplot(data=laptops_df, x='Contact Sex', y='Profit', estimator = np.mean, ax=axes[1]);
axes[1].set_title('Avg Profit by Sex')

sns.barplot(data=laptops_df, x='Contact Sex', y='Profit', estimator = np.sum, ax=axes[2])
axes[2].set_title('Total Profit by Sex')

plt.tight_layout()

# %%
# Avergae profit margin by sex

sns.barplot(data=laptops_df, x='Contact Sex', y='Profit Margin - %', estimator = np.mean);

# %%
# Average pure profit by sex

sns.barplot(data=laptops_df, x='Contact Sex', y='Profit', estimator = np.mean);

# %%
# Total pure profit by sex -- since males had higher average margin and females had higher pure profit, I decided to use total profit to break the tie to determine which was best target between the two

sns.barplot(data=laptops_df, x='Contact Sex', y='Profit', estimator = np.sum);

# %% [markdown]
# # 2) If business is cash-constrained, which gender should be targeted?
#
# ## ANSWER - MALE
#
# ### Cost Margin and Avergae cost by gender are both lower for males, so a cash-strapped business would want to market to them first. Total cost is being ignored because if there is more revenue to a certain gender then the total cost would generally also be higher for that gender. AKA a higher total cost does't drill down the actual cost of that gender to the business

# %%
# Add cost margin column

laptops_df['COGS Margin - %'] = (laptops_df['Our Cost'] / laptops_df['Sale Price']) * 100

laptops_df.head()

# %%
## Same as above, did all the individual work but now makign a cell with all charts together

fig, axes = plt.subplots(1,2)

sns.barplot(data=laptops_df, x='Contact Sex', y='COGS Margin - %', estimator = np.mean, ax=axes[0]);
axes[0].set_title('Avg COGS Margin by Sex')

sns.barplot(data=laptops_df, x='Contact Sex', y='Our Cost', estimator = np.mean, ax=axes[1]);
axes[1].set_title('Avg Cost by Sex')

plt.tight_layout;

# %%
# Average COGS Margin by Gender

sns.barplot(data=laptops_df, x='Contact Sex', y='COGS Margin - %', estimator = np.mean);

# %%
# Average cost by gender

sns.barplot(data=laptops_df, x='Contact Sex', y='Our Cost', estimator = np.mean);

# %% [markdown]
# # 3) If consumer is cash-constrained, which gender should be targeted?
#
# ## ANSWER - MALES
#
# ### Males spend less on average per purchase than females, so if cash is tight then looking for those consumers that spend less on balance is a good start

# %%
# New column that is shipping plus revenue (this is cost to customer)

laptops_df['Consumer Total'] = laptops_df['Sale Price'] + laptops_df['Shipping Cost']

laptops_df.head()

# %%
# Average Consumer Total by gender

sns.barplot(data=laptops_df, x='Contact Sex', y='Consumer Total', estimator = np.mean);

# %% [markdown]
# # 4) What is our target age to maximize profit?
#
# ## ANSWER - 50-60 year olds, closely followed by 40-50 year olds
#
# ### 50-60 shows highest total profit, pure profit, and profit margin of all observed groups. 40-50 year olds are second in pure profit and margin, and substantially higher than younger peers in total profit so that group probably warrants being part of a target group as well

# %%
# # Average Margin by Individual Age

# profm_by_age = laptops_df.groupby('Contact Age')['Profit Margin - %'].mean()

# plt.bar(profm_by_age.index, profm_by_age.values)


# %%
# # Total Profit by Individual Age

# tprof_by_age = laptops_df.groupby('Contact Age')['Profit'].mean()

# plt.bar(tprof_by_age.index, tprof_by_age.values)

# %%
# Average profit by individual age

sns.barplot(data=laptops_df, x='Contact Age', y='Profit', estimator = np.mean);

# %%
#profit Margin by invidivual age

sns.barplot(data=laptops_df, x='Contact Age', y='Profit Margin - %', estimator = np.mean);

# %%
# Add a column with age groups

def assign_age_group(age):
    if age < 20:
        return 'Under 20'
    elif 20 <= age < 30:
        return '20-30'
    elif 30 <= age < 40:
        return '30-40'
    elif 40 <= age < 50:
        return '40-50'
    elif 50 <= age < 60:
        return '50-60'
    else:
        return 'Over 60'

laptops_df['Age Group'] = laptops_df['Contact Age'].apply(assign_age_group)

laptops_df.head()

# %%
# Now that we have age group column, run same plots by age group

# %%
#Pure profit by group

# I added this line because the age groups were out of order
age_groups_order = ['20-30', '30-40', '40-50', '50-60',]

sns.barplot(data=laptops_df, x='Age Group', y='Profit', estimator = np.mean, order = age_groups_order);

# %%
#Profit margin by group


sns.barplot(data=laptops_df, x='Age Group', y='Profit Margin - %', estimator = np.mean, order = age_groups_order);

# %%
#Total profit by age group

sns.barplot(data=laptops_df, x='Age Group', y='Profit', estimator = np.sum, order = age_groups_order);

# %% [markdown]
# # 5) Which product should we feature?
#
# ## ANSWER
# ## If by specific product - M01F0024 -- has the highest profit margin by far, and is middle of the road for absolute profit
# ### If we want to choose by absolute profit, GT13-0024 has the highest absolute profit
#
# ## If by product type -- Desktop -- has the highest profit margin and highest absolute profit out of the three choices in product type
#

# %%
laptops_df.head()


# %%
# Not sure if we should be looking at specific product or type, a couple quick checks

# %%
laptops_df['Product Type'].unique()

# %%
laptops_df['Product ID'].unique()

# %%
fig, axes = plt.subplots(2, 1, figsize=(12, 12))

sns.barplot(data=laptops_df, x='Product ID', y='Profit', estimator = np.mean, ax=axes[0])
axes[0].set_title('Avg Profit by Product ID')

sns.barplot(data=laptops_df, x='Product ID', y='Profit Margin - %', estimator = np.mean, ax=axes[1])
axes[1].set_title('Avg Profit Margin by Product ID')
plt.tight_layout()

# %%
fig, axes = plt.subplots(2, 1, figsize=(5,10))

sns.barplot(data=laptops_df, x='Product Type', y='Profit', estimator = np.mean, ax=axes[0])
axes[0].set_title('Avg Profit by Product Type')

sns.barplot(data=laptops_df, x='Product Type', y='Profit Margin - %', estimator = np.mean, ax=axes[1])
axes[1].set_title('Avg Profit Margin by Product Type')
plt.tight_layout()

# %% [markdown]
# # 6) What lead sources have worked in the past: website, flyer, or email?
#
# ## ANSWER - I would choose flyer 2 as it has the second highest profit margin and the third highest average profit. Though it is numbers two and three, it is just behind the omnes in front of it on both categories so it would make sense to use thus one as it covers the most bases

# %%
# Check value counts

laptops_df['Lead Source'].value_counts()

# %%
fig, axes = plt.subplots(2, 1, figsize=(8, 8))

sns.barplot(data=laptops_df, x='Lead Source', y='Profit', estimator = np.mean, ax=axes[0])
axes[0].set_title('Avg Profit by Lead Source')

sns.barplot(data=laptops_df, x='Lead Source', y='Profit Margin - %', estimator = np.mean, ax=axes[1])
axes[1].set_title('Avg Profit Margin by Lead Source')
plt.tight_layout()

# %% [markdown]
# # 7) When is the best time to do email marketing?
#
# ## ANSWER - This one is tough because there is A -- not a ton of data related specifically to email marketing (aka 7 samples with email marketing and that is it) and B -- a variance in metrics between profit margin and absoliute profit
# ## That said, I will say Juky is the best month to market in an email -- the profit margin is far and away the highest for email marketing done in July, and the absolute profit is the thrid highest in July
# ## To reiterate, more data would be good here

# %%
email_df = laptops_df[laptops_df['Lead Source'] == 'Email']
email_df

# %%
fig, axes = plt.subplots(2, 1, figsize=(8, 12))

sns.barplot(data=email_df, x='Sale Month', y='Profit', estimator = np.mean, ax=axes[0])
axes[0].set_title('Avg Profit by Email Month')

sns.barplot(data=email_df, x='Sale Month', y='Profit Margin - %', estimator = np.mean, ax=axes[1])
axes[1].set_title('Avg Profit Margin by Email Month')
plt.tight_layout()

# %%
