# %%
from bs4 import BeautifulSoup as beauty
import requests
import pandas as pd

# %%
f1_url = 'https://www.formula1.com/en/results/2022/drivers'

# %%
#1 connect to server and recieve "ok" code

f1_site = requests.get(f1_url)
f1_site.status_code

# %%
#2 scrape page for statistics stored  in table

f1_soup = beauty(f1_site.content)
f1_tables = f1_soup.find_all('table')
f1_tables

# %%
#3 save the table as a dataframe

from io import StringIO
f1_df = pd.read_html(StringIO(str(f1_tables)))
f1_df = f1_df[0]
f1_df

# %%
#4 save as a csv, then reread to make sure it saved correctly

f1_df.to_csv('f1_table.csv', index=False)

pd.read_csv('f1_table.csv')


# %%
#5 Scrape using pd.read_html

f1_scrape_no_beauty = pd.read_html('https://www.formula1.com/en/results/2022/drivers')
f1_scrape_no_beauty = f1_scrape_no_beauty[0]
f1_scrape_no_beauty
