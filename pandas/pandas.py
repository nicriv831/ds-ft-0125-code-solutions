# %% [markdown]
# # Pandas Exercises
#
# ### 1. Import numpy, pandas, etc
#

# %%
import numpy as np

import pandas as pd


# %% [markdown]
# ### 2. Load the data from the file `"Loan payments data.csv"` into a variable called `"loans"`

# %%
loans = pd.read_csv('Loan payments data.csv')

# %% [markdown]
# ### 3. Display the first 7 rows of the data

# %%
loans.head(7)

# %% [markdown]
# ### 4. Display the last 3 rows of the data

# %%
loans.tail(3)

# %% [markdown]
# ### 5. Select 25% of the data, picked randomly and display the first 5 rows

# %%
loans.shape # to see total rows
loans_25_sample = loans.sample(int(500*.25))
loans_25_sample.head()

# %% [markdown]
# ### 6. Sample 10 rows and display it

# %%
loans_10_sample = loans.sample(10)
loans_10_sample

# %% [markdown]
# ### 7. Display the value counts of the `loan_status` column and the `City` column

# %%
loans.value_counts('loan_status')

# %%
loans.value_counts('City')

# %% [markdown]
# ### 8. Display only the 201st row

# %%
loans.iloc[200]

# %% [markdown]
# ### 9. Display only the `education` column

# %%
loans['education']

# %% [markdown]
# ### 10. Display only the `loan_status` column

# %%
loans['loan_status']

# %% [markdown]
# ### 11. Display only the 9th column by index
#
# ***(hint: remember that Python is 0-indexed!)***

# %%
loans.iloc[:, 8]

# %% [markdown]
# ### 12. Display the 3rd through 7th rows by index slicing

# %%
loans.iloc[2:7]

# %% [markdown]
# ### 13. Display the last 3 columns by index slicing

# %%
loans.iloc[:,-3:]

# %% [markdown]
# ### 14. Display only the rows where `Gender` is `female`

# %%
loans.loc[loans['Gender'] == 'female']

# %% [markdown]
# ### 15. Display only the rows where `education` is `college` AND `City` is `NYC`

# %%
loans.loc[(loans['education'] == 'college') & (loans['City'] == 'NYC')]

# %% [markdown]
# ### 16. Display only the rows where `age` is larger than 32

# %%
loans.loc[loans['age'] > 32]

# %% [markdown]
# ### 17.  Display the rows where there is a past-due of larger than a week and only display the `due_date` and `past_due_days` columns

# %%
loans_past_seven = loans.loc[loans['past_due_days'] > 7, ['due_date', 'past_due_days']]
loans_past_seven
