####Twitter Streamer####

from twitter_client import TwitterAuthenticator

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