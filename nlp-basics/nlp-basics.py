# %%
# Imports

import pandas as pd
import nltk
import spacy
from nltk import PorterStemmer

# %%
# Read CSV

df = pd.read_csv('winemag-data.csv', index_col=0)

# %%
# Head check

df.head()

# %%
# Dupe check

df.duplicated().sum()

# %%
# Drop 9983 duplicates

df = df.drop_duplicates()
df.duplicated().sum()

# %%
# Info check

df.info()

# %%
# Keep only text and rating column

df = df[['description', 'points']]
df

# %%
# NA check -- 0 nans

df.isna().sum()

# %%
# Take a look at points counts

df['points'].value_counts().sort_index(ascending=False)

# %%
# Plot points counts -- distribution looks very close to normal

df['points'].hist()

# %%
# Look at character counts of reviews

df['char_count'] = df['description'].str.len()
df.head()

# %%
# Look at character count distribution

df['char_count'].hist()

# %% [markdown]
# # 1 Tokenize description feature
#

# %%
# downloads for tokenizer

nltk.download('punkt')
nltk.download('punkt_tab')

# %%
# make description lowercase

df['lower'] = df['description'].str.lower()
df.head()

# %%
# make tokened column

df['tokens'] = df['lower'].apply(nltk.word_tokenize)
df.head()

# %% [markdown]
# # 2 Remove Stopwords

# %%
# stopwords imports

nltk.download('stopwords')
from string import punctuation


# %%
# Make stopwords list and check work

stopwords = nltk.corpus.stopwords.words('english')
stopwords

# %%
# Check punctuation

punctuation

# %%
# create stopword list

# make punctution into list

punc = [p for p in punctuation]

# Combine stopwords and puctuTION

stopwords = stopwords + punc
stopwords


# %%
# remove stops and punctuation

def remove_stopwords(text):
  return [word for word in text if word not in stopwords]

df['no_stop'] = df['tokens'].apply(remove_stopwords)
df.head()

# %% [markdown]
# # 3 Stem the tokens

# %%
# create porter stemmer instance

stems = PorterStemmer()

# %%
# Create stemmer function

def stemmer(text):
  return [stems.stem(word) for word in text]

# %%
# apply stemmer function to text

df['stemmed'] = df['no_stop'].apply(stemmer)
df

# %%
# rename column to match assignment

df = df.rename(columns={'stemmed':'Cleaned_Stem_Description'})
df

# %% [markdown]
# # 4 Lemmatize tokens

# %%
# Make model

nlp_model = spacy.load('en_core_web_sm')

# %%
# Make lemmatizer fuction

def lemmatizer(text):
  doc = nlp_model(text)
  processed_doc = [token.lemma_ for token in doc
                   if not token.is_stop and not token.is_punct
                   and not token.is_space]

  return processed_doc

# %%
# apply lemmatizer function to text

df['Cleaned_Lemma_Description'] = df['lower'].apply(lemmatizer)
df.head()

# %% [markdown]
# # 5 Build a wordcloud based on Cleaned_Lemma_Description

# %%
# import

from wordcloud import WordCloud

# %%
# make one list with all words

lemma_words = df['Cleaned_Lemma_Description'].explode().astype(str).to_list()
lemma_words = ' '.join(lemma_words)

# %%
# create wordcloud with word list

lemma_cloud = WordCloud(min_word_length=2).generate(lemma_words)

# %%
# plot word cloud

import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(10,10))

ax.imshow(lemma_cloud)
ax.axis('off')
ax.set_title('Words in Positive Tweets')

# %%
