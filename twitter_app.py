from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API
from tweepy import Cursor
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

import credentials

#### Twitter Client #####

class TwitterClient():

    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)

        self.twitter_user = twitter_user

    def get_twitter_client_api(self):
        return self.twitter_client


    def get_user_timeline_tweets(self, num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline, id = self.twitter_user).items(num_tweets):
            tweets.append(tweet)
        return tweets

    def get_friend_list(self, num_friends):
        friend_list = []
        for friend in Cursor(self.twitter_client.friends, id= self.twitter_user).items(num_friends):
            friend_list.append(friend)
        return friend_list

    def get_home_timeline_tweets(self, num_tweets):
        home_tweets = []
        for tweet in Cursor(self.twitter_client.home_timeline, id = self.twitter_user).items(num_tweets):
            home_tweets.append(tweet)
        return home_tweets




#####Twitter Authenticator ###
class TwitterAuthenticator():

    def authenticate_twitter_app(self):
        auth = OAuthHandler(credentials.CONSUMER_KEY, credentials.CONSUMER_SECRET)
        auth.set_access_token(credentials.API_TOKEN, credentials.API_TOKEN_SECRET)
        return auth

####Twitter Streamer####

class TwitterStreamer():
    def __init__(self):
        self.twitter_authenticator = TwitterAuthenticator()


    def stream_tweets(self, fetched_tweets_filename, hash_tag_list):
        """
        Class for Streaming and processing live tweets
        """
        #This handles Twitter Authentication and connection to twitter streaming API
        listener = TwitterListener(fetched_tweets_filename)

        auth = self.twitter_authenticator.authenticate_twitter_app()

        stream = Stream(auth, listener)
        stream.filter(track=hash_tag_list)



class TwitterListener(StreamListener):

    """This is a baisc listener class that just print received tweets to stdout"""
    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename

    def on_data(self, data):
        try:
            print(data)
            with open(self.fetched_tweets_filename, 'a') as tf:
                tf.write(data)
        except BaseException as e:
            print('Error on data %s' % str(e))
        return True

    def on_error(self, status):
        if status == 420:
            #Returning False on_data method in case rate limit occurs.
            return False
        print(status)


class TwwetAnalyzer():
    """
    Functionality to analyze and categorize content from tweets.
    """
    def tweets_to_dataframe(self, tweets):

        df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['Tweets'])
        df['id'] = np.array([tweet.id for tweet in tweets])
        df['len'] = np.array([len(tweet.text) for tweet in tweets])
        df['created'] = np.array([tweet.created_at for tweet in tweets])
        df['source'] = np.array([tweet.source for tweet in tweets])
        df['likes'] = np.array([tweet.favorite_count for tweet in tweets])
        df['retweet'] = np.array([tweet.retweet_count for tweet in tweets])

        return df
if __name__ == "__main__":
    #Set Pandas Options to see all Coloumns of a data frame
    pd.set_option('display.max_rows', 500)
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.width', 1000)

    tweet_analyzer = TwwetAnalyzer()

    twitter_client = TwitterClient()
    api = twitter_client.get_twitter_client_api()

    tweets = api.user_timeline(screen_name="baloise_ch", count=370)
    df = tweet_analyzer.tweets_to_dataframe(tweets)

    #Average length over al tweets
    print(np.mean(df['len']))

    #Get Number of likes for the most liked tweets
    print(np.max(df['likes']))

    #Get the Number of Rewteets for nost retweetet
    print(np.max(df['retweet']))

    #Time Series
    #time_likes = pd.Series(data=df['likes'].values, index=df['created'])
    #time_likes.plot(figsize=(16,4), color='r')
    #plt.show()
    #Time Retweet
    #time_likes = pd.Series(data=df['retweet'].values, index=df['created'])
    #time_likes.plot(figsize=(16,4), color='r')
    #plt.show()

    time_likes = pd.Series(data=df['likes'].values, index=df['created'])
    time_likes.plot(figsize=(16,4), color='r', label="likes", legend = True, )

    time_likes = pd.Series(data=df['retweet'].values, index=df['created'])
    time_likes.plot(figsize=(16,4), color='g',label="retweets", legend = True,)
    plt.show()
