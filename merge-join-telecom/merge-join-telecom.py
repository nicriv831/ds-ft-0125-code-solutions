# %%
import pandas as pd

# %%
#read all tables into dataframe

m_j_path = '../ds-ft-0125-code-solutions/merge-join-telecom/Telstra Competition Data/'

event_type = pd.read_csv(m_j_path + 'event_type.csv')
event_type.head(2)

# %%
log_feature = pd.read_csv(m_j_path + 'log_feature.csv')
log_feature.head(2)

# %%
resource_type = pd.read_csv(m_j_path + 'resource_type.csv')
resource_type.head(2)

# %%
severity_type = pd.read_csv(m_j_path + 'severity_type.csv')
severity_type.head(2)

# %%
train = pd.read_csv(m_j_path + 'train.csv')
train.head(5)

# %%
#1 Merge Tables

merged1 = pd.merge(train, event_type, how = 'inner', on  = 'id')

frames_to_merge = [severity_type, resource_type, log_feature]

for frame in frames_to_merge:
  merged1 = pd.merge(merged1, frame, how = 'inner', on = 'id')

merged1

# %%
#2 Explain the difference between inner and outer merge

# Outer join will take every row from both tables whether or not there is any overlap between each table. There may be NaaNs

# Inner join will take common rows from each table and make a new table. There should not be any NaaNs as only the common items remain


# %%
#3 Explain the difference between merge and join

# Join defaults to left join and using indexes to determine what to keep. It is good when the items to merge share the same index in each dataframe

# Merge defaults to inner join and you can specify which column to use as the ker for merging -- merged table above is using "id" as the key for merge


# %%
#4 Divide the dataset into to two dataframes

merged_split1 = merged1.iloc[:(merged1.shape[0] // 2)]
merged_split2 = merged1.iloc[(merged1.shape[0] // 2):]

# %%
# #checking work for splits above

merged_split1.tail()


# %%
merged_split2.head()

# %%
#5 Concatenate both dataframes

merged_concatenated = pd.concat([merged_split1, merged_split2])

merged_concatenated

# %%
# Handle Duplicates

merged_concatenated[merged_concatenated.duplicated()]

# %%
# Per above there are no duplicates. If there were, would drop this way

merged_concatenated = merged_concatenated.drop_duplicates()

# %%
# Final Output

merged_concatenated
