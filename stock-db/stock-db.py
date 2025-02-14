# %%
import pandas as pd
import sqlite3

# %%
# Connect to local database

filepath = 'stock-db/'

conn = sqlite3.connect(filepath + 'stocks.sqlite')

# %%
# List all tables in stocks database

q = """
SELECT name FROM sqlite_master WHERE type='table'
"""

pd.read_sql(q, conn)

# %%
# .head() equivalent to see what's in the table

q = """
SELECT *
FROM STOCK_DATA
LIMIT 5
"""

pd.read_sql(q, conn)

# %%
# create MSFT table

conn.execute("""
CREATE TABLE msft_only
('index' SMALLINT,
Date TEXT,
Open REAL,
High REAL,
Low REAL,
Close REAL,
Volume SMALLINT,
Adj Close REAL,
Symbol VARCHAR(5))
""")


# %%
# insert data into MSFT table

conn.execute ("""
INSERT INTO msft_only
  ("index", Date, Open, High, Low, Close, Volume, Adj, SYMBOL)
SELECT sd."index", sd.Date, sd.Open, sd.High, sd.Low, sd.Close, sd.Volume, sd."Adj Close", sd.SYMBOL
FROM STOCK_DATA as sd
WHERE sd.Symbol = 'MSFT'
""" )


# %%
msft_q = """
SELECT *
FROM msft_only
"""

# %%

pd.read_sql(msft_q, conn)


# %%
# create AAPL table

conn.execute("""
CREATE TABLE aapl_only
('index' SMALLINT,
Date TEXT,
Open REAL,
High REAL,
Low REAL,
Close REAL,
Volume SMALLINT,
Adj_Close REAL,
Symbol VARCHAR(5))
""")


# %%

appl_q = """
SELECT *
FROM aapl_only
"""

# %%
conn.execute ("""
INSERT INTO aapl_only
  ("index", Date, Open, High, Low, Close, Volume, Adj_Close, Symbol)
SELECT sd."index", sd.Date, sd.Open, sd.High, sd.Low, sd.Close, sd.Volume, sd."Adj Close", sd.SYMBOL
FROM STOCK_DATA as sd
WHERE sd.Symbol = 'AAPL'
""" )


# %%
pd.read_sql(appl_q, conn)

# %%
msft_minmax = """
SELECT *
FROM msft_only
WHERE Date = (SELECT MIN(Date) FROM msft_only)
   OR Date = (SELECT MAX(Date) FROM msft_only);
"""

df_msft_minmax = pd.read_sql(msft_minmax, conn)

# %%
df_msft_minmax

# %%
aapl_minmax = """
SELECT *
FROM aapl_only
WHERE Date = (SELECT MIN(Date) FROM aapl_only)
   OR Date = (SELECT MAX(Date) FROM aapl_only);
"""

df_aapl_minmax = pd.read_sql(aapl_minmax, conn)

# %%
df_aapl_minmax

# %%
msft_open50 = """
SELECT *
FROM msft_only
WHERE Open > 50
"""
df_msft_open50 = pd.read_sql(msft_open50, conn)


# %%
df_msft_open50

# %%
aapl_open50 = """
SELECT *
FROM aapl_only
WHERE Open > 50
"""
df_aapl_open50 = pd.read_sql(aapl_open50, conn)

# %%
df_aapl_open50
