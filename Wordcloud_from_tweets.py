# Make a wordcloud of the most used words across all downloaded tweets
    
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


def wordcloud(tweets,col,idgraf,mask):
	# Creates the image with the most used words
    wordcloud = WordCloud(background_color="white",stopwords=stop_words,random_state = 1020,mask=mask).generate(" ".join([i for i in tweets[col]]))
    plt.figure(num=idgraf, figsize=(5,5), facecolor='k')
    plt.imshow(wordcloud.recolor(color_func=image_colors), interpolation="bilinear")
    plt.axis("off")

def tweetprocess(tweets,idgraf,mask):
	print(idgraf)
	tweets['tweetos'] = '' 

	#add tweetos first part
	for i in range(len(tweets['text'])):
	    try:
	        tweets['tweetos'][i] = tweets['text'].str.split(' ')[i][0]
	    except AttributeError:    
	        tweets['tweetos'][i] = 'other'

	# Preprocess tweets with 'RT @'
	for i in range(len(tweets['text'])):
	    if tweets['tweetos'].str.contains('@')[i]  == False:
	        tweets['tweetos'][i] = 'other'
	        
	# Remove URLs, RTs, and tweet handles
	for i in range(len(tweets['text'])):
	    tweets['text'][i] = " ".join([word for word in tweets['text'][i].split()
	                                if 'http' not in word and '@' not in word and '<' not in word and 'RT' not in word])

	#Remove puntuaction
	tweets['text'] = tweets['text'].apply(lambda x: re.sub('[¡!@#$:).;,¿?&]', '', x.lower()))
	tweets['text'] = tweets['text'].apply(lambda x: re.sub('  ', ' ', x))
	# Make wordcloud
	wordcloud(tweets,'text',idgraf,mask)


# Create a mask for your wordcloud
d = os.path.dirname(__file__) if "__file__" in locals() else os.getcwd()
image = np.array(Image.open(os.path.join(d, "my_mask.png")))    # The white parts (where there will be no words) must be set to 255
mask=image
plt.grid('off)')
plt.imshow(mask)

# Example to make white parts into 255:
# mask1 = mask.copy() 
# mask1[mask1.sum(axis=2) == 0] = 255
# plt.imshow(mask1)

# To define the colors of your wordcloud you can use the colors from an existing image or defina a pallet:
# Use color from an image:
mask_color = np.array(Image.open(os.path.join(d, "imagecolors.png")))
color_mask= mask_color.copy()
image_colors = ImageColorGenerator(color_mask) # Generate the pallet of colors

# Create specific pallet:
def color_func(word, font_size, position, orientation, random_state=None,**kwargs):
    return "hsl(35, %d%%, %d%%)" % (random.randint(40,85) ,random.randint(40, 80) )     # The most important number is the first one ('h'), the one asociated with the hue (0:red; 120:green; 240:blue)
image_colors= color_func



# Finally make the wordcloud
tweetprocess(tweets,1,mask)
