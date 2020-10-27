
import tweepy #https://github.com/tweepy/tweepy
import csv
import io
import time
import pandas as pd
import re
import numpy as np

# Twitter API credentials
consumer_key = ""
consumer_secret = ""
access_key = ""
access_secret = ""


'''
    This step creates your CSV file to store poems (only run it the first time, if you run it again, it will be overwritten with no poems saved)
'''
# with io.open('Poems.csv', "w", newline='' , encoding="utf-8") as f:       
#         writer = csv.writer(f, quoting=csv.QUOTE_ALL)
#         writer.writerow(("Title",'Text'))

#%%

'''
    Manually load poems in your file
'''
title=('''REMORSE FOR ANY DEATH''')

text=('''Free of memory and of hope,
limitless, abstract, almost future,
the dead man is not a dead man: he is death.
Like the God of the mystics,
of Whom anything that could be said must be denied,
the dead one, alien everywhere,
is but the ruin and absence of the world.
We rob him of everything,
we leave him not so much as a color or syllable:
here, the courtyard which his eyes no longer see,
there, the sidewalk where his hope lay in wait.
Even what we are thinking,
he could be thinking;

we have divvied up like thieves
the booty of nights and days.''')

poem=[title,text]
with io.open('Poems.csv', "a", newline='' , encoding="utf-8") as f:       
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        writer.writerows([poem])   

#%%
'''
    Tweet a poem
'''
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

data_poems = pd.read_csv(r'Poems.csv',encoding='utf-8',sep=',')

# Choose a random poem to tweet
r = np.random.randint(len(data_poems.index))
line=data_poems.Title[r] + '\n'+df.Text[r]  

# Separate your poem in lines so it will not be cut in between sentences
if len(line)>275:  # If the poem is too long it will be tweeted as a thread
    tuit=line
    end_lines = [m.start() for m in re.finditer('\n', tuit)]  # Find the position where the lines end
    number_tweets = len(tuit)//275
    cut=[j for j in end_lines if j<275][-1]
    tweet_1=api.update_status(tuit[:cut])   # Tweet the first part
    for i in range(1,number_tweets):        # Tweet the rest
        time.sleep(4) 
        tuit=tuit[cut+1:]
        end_lines = [m.start() for m in re.finditer('\n', tuit)]
        cut = [k for k in end_lines if k<275][-1]
        tweet_1=api.update_status(status=tuit[:cut], in_reply_to_status_id=tweet_1.id, auto_populate_reply_metadata=True)
    time.sleep(4)
    api.update_status(status=tuit[cut+1:], in_reply_to_status_id=tweet_1.id, auto_populate_reply_metadata=True)
elif len(line)<=275:
    tweet_1=api.update_status(line)
    time.sleep(2) 
print(line)
print ("All done!")










