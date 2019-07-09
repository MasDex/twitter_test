from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API
from tweepy import Cursor
import pandas as pd
import numpy as np
import os
from persistence import Persistence
from twitter_client import TwitterClient
from textblob import TextBlob

from tweet_analyzer import TweetAnalyzer


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
