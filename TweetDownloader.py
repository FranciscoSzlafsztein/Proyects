import tweepy #https://github.com/tweepy/tweepy
import csv
import io

# Twiter API credentials
consumer_key = ""
consumer_secret = ""
access_key = ""
access_secret = ""

# Function to remove un-printable characters
def strip_undesired_chars(tweet):
    stripped_tweet = tweet.replace('\n', ' ').replace('\r', '')
    char_list = [stripped_tweet[j] for j in range(len(stripped_tweet)) if ord(stripped_tweet[j]) in range(65536)]
    stripped_tweet=''
    for j in char_list:
        stripped_tweet=stripped_tweet+j
    return stripped_tweet

def get_all_tweets(screen_name):
    limit_number = 3200  # Number of tweets to download (from last) (Twiter only allows 3240 tweets max)
    
    # Authorizarion step
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
    
    alltweets = []    
    
    # Initial petition for the last 200 tweets ('extended' means up to 280 character per tweet)
    new_tweets = api.user_timeline(screen_name = screen_name,count=200, tweet_mode='extended' )
    
    # Store tweets
    alltweets.extend(new_tweets)
    
    # Store the id of the last tweet downloaded
    oldest = alltweets[-1].id - 1
    
    # Download the rest
    while len(new_tweets) > 0 and len(alltweets) <= limit_number:
        print ("getting tweets before" + str(oldest))
        
        new_tweets = api.user_timeline(screen_name = screen_name,count=200, tweet_mode='extended' ,max_id=oldest)
        
        alltweets.extend(new_tweets)
        
        oldest = alltweets[-1].id - 1
        
        print (str(len(alltweets)) + " downloaded tweets so far...")
    
    # Keep only the tweets (remove the retweets) and make them a 2D array
    outtweets = [(tweet.id_str, tweet.created_at, strip_undesired_chars(tweet.full_text),tweet.retweet_count,str(tweet.favorite_count)+'') for tweet in alltweets if 'RT @' not in tweet.full_text]
    
    # Write the CSV    
    with io.open('%s tweets(no retweets).csv' % screen_name, "w", newline='' , encoding="utf-8") as f:       
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        writer.writerow(['id','created_at','text','retweet_count','favorite_count'''])
        writer.writerows(outtweets)    
    pass

if __name__ == '__main__':
    # Specify the twitter account (without "@")
    get_all_tweets("twiiter_account")



