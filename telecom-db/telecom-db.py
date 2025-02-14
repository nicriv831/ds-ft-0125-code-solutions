# %%
import pandas as pd
import sqlite3

filepath = 'telecom-db/'

conn = sqlite3.connect(filepath + 'telecom.db')

# %%
# Retrieve table names from the database (telecom.db).

q = """
SELECT name FROM sqlite_master WHERE type='table'
"""

pd.read_sql(q, conn)

# %%
q = """
SELECT * FROM event_type limit 5
"""

pd.read_sql(q, conn)

# %%
# Join all tables in the database on the primary key

join_q = """
SELECT t.id, t.location, t.fault_severity, et.event_type, st.severity_type, rt.resource_type, lf.log_feature, lf.volume
FROM train t
LEFT JOIN event_type et
ON t.id = et.id
LEFT JOIN severity_type as st
ON t.id = st.id
LEFT JOIN resource_type as rt
ON t.id = rt.id
LEFT JOIN log_feature as lf
ON t.id = lf.id
"""

pd.read_sql(join_q, conn)


# %%
#Find unique occurrences of event_type and severity in the table from #2 using an SQL query

# My understanding is this is showing me each unique combination of the two. If I wanted to list each unique type separately i would need to run two separate lines of code, one for unique event type and another for unique severity type

join_q = """
WITH join_all AS (
SELECT t.id, t.location, t.fault_severity, et.event_type, st.severity_type, rt.resource_type, lf.log_feature, lf.volume
FROM train t
LEFT JOIN event_type et
ON t.id = et.id
LEFT JOIN severity_type as st
ON t.id = st.id
LEFT JOIN resource_type as rt
ON t.id = rt.id
LEFT JOIN log_feature as lf
ON t.id = lf.id)

SELECT DISTINCT event_type AS unq_event, severity_type as unq_fault_sev
FROM join_all;
"""

pd.read_sql(join_q, conn)

# %%
##Find how many occurrences there are of each fault_severity in the table from #2 using an SQL query

join_q = """
WITH join_all AS (
SELECT t.id, t.location, t.fault_severity, et.event_type, st.severity_type, rt.resource_type, lf.log_feature, lf.volume
FROM train t
LEFT JOIN event_type et
ON t.id = et.id
LEFT JOIN severity_type as st
ON t.id = st.id
LEFT JOIN resource_type as rt
ON t.id = rt.id
LEFT JOIN log_feature as lf
ON t.id = lf.id)

SELECT fault_severity, COUNT(*) AS fault_sev_counts
FROM join_all
GROUP BY fault_severity
"""

pd.read_sql(join_q, conn)
