from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API
from tweepy import Cursor
import pandas as pd
import numpy as np
import os
import re
from persistence import Persistence
from twitter_client import TwitterClient


from textblob import TextBlob





class TweetAnalyzer():
    """
    Functionality to analyze and categorize content from tweets.
    """
    def clean_tweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def analyze_sentiment(self, tweet):
        analysis = TextBlob(self.clean_tweet(tweet))

        if analysis.sentiment.polarity > 0:
            return 1
        elif analysis.sentiment.polarity == 0:
            return 0
        elif analysis.sentiment.polarity > 0:
            return -1

    def tweets_to_dataframe(self, tweets):

        df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['tweets'])
        df['id'] = np.array([tweet.id for tweet in tweets])
        df['len'] = np.array([len(tweet.text) for tweet in tweets])
        df['created'] = np.array([tweet.created_at for tweet in tweets])
        df['source'] = np.array([tweet.source for tweet in tweets])
        df['likes'] = np.array([tweet.favorite_count for tweet in tweets])
        df['retweet'] = np.array([tweet.retweet_count for tweet in tweets])

        return df

#class Persistence():
#    def __init__(self):
#            self.client = MongoClient('mongodb://localhost:27017')
#            self.db = self.client['twitter-database']
#            self.tweets = self.db.tweets
#
#    def save_tweets(self, df):
#        data = df.to_dict(orient='records')
#        self.tweets.insert_many(data)
#        print(data)




if __name__ == "__main__":
    #Set Pandas Options to see all Coloumns of a data frame
    pd.set_option('display.max_rows', 500)
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.width', 1000)

    tweet_analyzer = TweetAnalyzer()

    twitter_client = TwitterClient()
    api = twitter_client.get_twitter_client_api()

    persistence = Persistence()

    tweets = api.user_timeline(screen_name="abockelm", count=10)
    df = tweet_analyzer.tweets_to_dataframe(tweets)
    df['sentiment'] = np.array([tweet_analyzer.analyze_sentiment(tweet) for tweet in df['tweets']])

    persistence.save_tweets(df)

    #print(df.head())

    #Timeow()

    time_likes = pd.Series(data=df['likes'].values, index=df['created'])
    time_likes.plot(figsize=(16,4), color='r', label="likes", legend = True, )

    time_likes = pd.Series(data=df['retweet'].values, index=df['created'])
    time_likes.plot(figsize=(16,4), color='g',label="retweets", legend = True,)
    #plt.show()

    print(df[:21])
