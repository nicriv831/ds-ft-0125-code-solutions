# %%
import pandas as pd
import sqlite3

# %%
filepath = 'human-resources-db/'

conn = sqlite3.connect(filepath + 'hr.db')

# %%
#1 Retrieve table names from the database (hr.db)

q = """
SELECT name FROM sqlite_master WHERE type='table'
"""

pd.read_sql(q, conn)

# %%
# Retrieve EmployeeNumber, Department, Age, Gender, and Attrition for employees in sales department from the Employee table; save that information into a dataframe named ‘sales’

q = """
Select *
from employee
LIMIT 5"""

pd.read_sql(q, conn)


# %%
#Retrieve EmployeeNumber, Department, Age, Gender, and Attrition for employees in sales department from the Employee table; save that information into a dataframe named ‘sales’.

sales_q ="""
SELECT EmployeeNumber, Department, Age, Gender, Attrition
FROM employee
WHERE Department = 'Sales'
"""

sales = pd.read_sql(sales_q, conn)

sales


# %%
##Retrieve EmployeeNumber, EducationField, Age, Gender, and Attrition for employees in the Life Sciences field from the Employee table, save that information into a dataframe named ‘field’

field_q ="""
SELECT EmployeeNumber, EducationField, Age, Gender, Attrition
FROM employee
WHERE EducationField = 'Life Sciences'
"""

field = pd.read_sql(field_q, conn)

field


# %%
# Save the two dataframes as tables in the database

sales.to_sql('sales', conn, index=False)

pd.read_sql("SELECT * FROM sales", conn)

# %%
#Save the two dataframes as tables in the database

field.to_sql('field', conn, index=False)

pd.read_sql("SELECT * FROM field", conn)

# %% [markdown]
# ## I am assuming that if we wanted a table with people who worked in sales with a life sciences education, we would just do a "where/and" filter and there would not be any need to create two separate tables to join
#
# ### However, if we do an inner join, we throw out lots of data
#
# #### Based on this, I chose full outer join and did not drop duplicate columns to preserve as much data as possible. For a project I would have knowledge of what exactly this would be used for in order to better choose join type

# %%
# join the tables on the primary key

sf_join_q ="""
    SELECT *
    FROM sales
    FULL OUTER JOIN field
    on sales.EmployeeNumber = field.EmployeeNumber
    """

sf_merged = pd.read_sql(sf_join_q, conn)

sf_merged
