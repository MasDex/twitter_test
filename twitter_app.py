from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import credentials

class TwitterStreamer():
    def stream_tweets(self, fetched_tweets_filename, hash_tag_list):
        """
        Class for Streaming and processing live tweets
        """
        #This handles Twitter Authentication and connection to twitter streaming API
        listener = StdOutListener(fetched_tweets_filename)
        auth = OAuthHandler(credentials.CONSUMER_KEY, credentials.CONSUMER_SECRET)
        auth.set_access_token(credentials.API_TOKEN, credentials.API_TOKEN_SECRET)

        stream = Stream(auth, listener)
        stream.filter(track=hash_tag_list)


class StdOutListener(StreamListener):

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
        print(status)

if __name__ == "__main__":
    hash_tag_list = ['Donald Trump']
    fetched_tweets_filename = 'tweets.json'

    twitter_streamer = TwitterStreamer()
    twitter_streamer.stream_tweets(fetched_tweets_filename,hash_tag_list)


