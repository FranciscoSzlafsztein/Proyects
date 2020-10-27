# Analysze the the use of words on twiter 
    
import numpy as np
import pandas as pd
import re
from PIL import Image
import imageio
import os
import random

# Visualization
import matplotlib.pyplot as plt
import matplotlib
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

import nltk  # Lenguage analysis library
from nltk import tokenize
nltk.download('stopwords')  # Download words that we will ignore
from nltk.corpus import stopwords
stop_words_sp = set(stopwords.words('spanish'))
stop_words_en = set(stopwords.words('english'))
stop_words = stop_words_sp | stop_words_en    # Make a list of words to ignore from english and spanish

stop_words.add('gracia')     # Add a stopword manually

matplotlib.style.use('ggplot')
pd.options.mode.chained_assignment = None

# Load tweets
tweets = pd.read_csv('user tweets.csv')

# Function to collect all the texts from the tweets under the 'text' column of tweets
def tweet_texts(tweets):
    tweets['tweetos'] =''
	# Add tweetos first part
    for i in range(len(tweets['text'])):
        try:
            tweets['tweetos'][i] = tweets['text'].str.split(' ')[i][0]
        except AttributeError:    
            tweets['tweetos'][i] = 'other'
	# Preprocess tweets with '@'
    for i in range(len(tweets['text'])):
        if tweets['tweetos'].str.contains('@')[i]== False:
            tweets['tweetos'][i] = 'other'      
    # Remove URLs, RTs, y twitter handles
    for i in range(len(tweets['text'])):
        tweets['text'][i] = " ".join([word for word in tweets['text'][i].split()
	                                if 'http' not in word and '@' not in word and '<' not in word and 'RT' not in word])
    # Remove punctuation
    tweets['text'] = tweets['text'].apply(lambda x: re.sub('[¡!@#$:).;,¿?&]', '', x.lower()))
    tweets['text'] = tweets['text'].apply(lambda x: re.sub('  ', ' ', x))

tweet_texts(tweets)
# Make a counter of the words used and the amount of times it was used
words = Counter(" ".join([i for i in tweets['text']]).split(" "))

# Ignore Stopwords
for word in list(words):
    if word in stop_words_sp:
        del words[word]
    if word in stop_words_sp:
        del words[word]

# Plot a histogram of the most used words
most_used_words=words.most_common(30)

labels, values = zip(*most_used_words)

fig, ax = plt.subplots(nrows=1, ncols=1)
indexes = np.arange(len(labels))
width = .6
plt.bar(indexes, values, width,color=['crimson']*3 + ['tab:blue']*(len(labels)-3))
plt.xticks(indexes , labels,rotation=50,ha='right')
plt.grid(False)
ax.set_facecolor('whitesmoke')   # Color of background
# ax.set_facecolor((1.0, 0.47, 0.42))
plt.ylabel('Times used')
plt.tight_layout(True)
plt.show()

