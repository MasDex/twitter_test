from tweepy import API, OAuthHandler
from tweepy import Cursor
import os


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
        auth = OAuthHandler(os.environ['CONSUMER_KEY'], os.environ['CONSUMER_SECRET'])
        auth.set_access_token(os.environ['API_TOKEN'], os.environ['API_TOKEN_SECRET'])
        return auth





