from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API
from tweepy import Cursor

import credentials

#### Twitter Client #####

class TwitterClient():

    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)

        self.twitter_user = twitter_user


    def get_user_timeline_tweets(self, num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline, id = self.twitter_user).items(num_tweets):
            tweets.append(tweet)
        return tweets

    def get_friend_list(self, num_friends):
        friend_list = []
        for friend in Cursor(self.twitter_client.friends).items(num_friends):
            friend_list.append(friend)
        return friend_list

    def get_home_timeline_tweets(self, num_tweets):
        home_tweets = []
        for tweet in Cursor(self.twitter_client.home_timeline).items(num_tweets):
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

if __name__ == "__main__":
    hash_tag_list = ['Donald Trump']
    fetched_tweets_filename = 'tweets.json'

    #twitter_streamer = TwitterStreamer()
    #twitter_streamer.stream_tweets(fetched_tweets_filename,hash_tag_list)

    twitter_client = TwitterClient('baloise_ch')
    print(twitter_client.get_user_timeline_tweets(5))



