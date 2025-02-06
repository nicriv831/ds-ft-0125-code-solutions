# %%
import pandas as pd

#MTcars

#1 Read into data frame
mtcars_fp = 'mtcars.csv'
mtcars_df = pd.read_csv(mtcars_fp)

#2 Save to same file type, different name
mtcars_df.to_csv('mtcars_edited.csv', index=False)

#3 Reread to ensure proper save

pd.read_csv('mtcars_edited.csv')


# %%
#u.data

#1 Read into data frame
udata_fp = 'u.data'
udata_df = pd.read_csv(udata_fp, sep='\t', header=None)
udata_df

#2 Save to same file type, different name
udata_df.to_csv('udata_edited.data', index=False)

#3 Reread to ensure proper save

pd.read_csv('udata_edited.data')


# %%
#beer.txt

#1 Read into data frame
beer_fp = 'beer.txt'
beer_df = pd.read_csv(beer_fp, sep=" ")

#2 Save to same file type, different name
beer_df.to_csv('beer_edited.txt', index=False)

#3 Reread to ensure proper save

pd.read_csv('beer_edited.txt')


# %%
#u.item

#pd.read_csv for u.item throws encoding error, need to determine which encoding is being used so will install chardet
!pip install chardet
import chardet


# %%
#installed chardet to determine encoding, used internet to figure out what exactly this was doing to get the right result

with open('u.item', 'rb') as file:
  uitem_data = file.read()

print(chardet.detect(uitem_data))
#print(encoding_result)

# %%
#1 Read into data frame
#Per python documentation, ISO8859-1 is "latin-1", so this is the encoding to be specified

uitem_fp = 'u.item'

uitem_df = pd.read_csv(uitem_fp, sep="|", encoding='latin_1', header=None)
uitem_df

#2 Save to same file type, different name
uitem_df.to_csv('ui_edited.item', index=False)

#3 Reread to ensure proper save

pd.read_csv('ui_edited.item')

# %%
#NHL 2015-16.xlsx

#1 Read into data frame

nhlxcel_fp = 'NHL 2015-16.xlsx'

nhlxcel_df = pd.read_excel(nhlxcel_fp)
nhlxcel_df

#2 Save to same file type, different name
nhlxcel_df.to_excel('nhlxcel_edited.xlsx', index=False)

#3 Reread to ensure proper save

pd.read_excel('nhlxcel_edited.xlsx')

# %%
#4 - Write a function that reads all five with no exceptions

def read_all(filename):
  fn, ext = filename.split('.')
  if ext == 'csv':
    return pd.read_csv(filename)
  elif ext == 'txt':
    return pd.read_csv(filename, sep=' ')
  elif ext == 'xlsx':
    return pd.read_excel(filename)
  elif ext == 'data':
    return pd.read_csv(filename, sep='\t', header=None)
  elif ext == 'item':
    return pd.read_csv(filename, sep='|', encoding='latin_1', header=None)


# %%
# I ran these with all the original files and it worked for each one

read_all('u.data')

# %%
