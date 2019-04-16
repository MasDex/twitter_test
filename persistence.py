from pymongo import MongoClient

class Persistence():
    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017')
        self.db = self.client['twitter-database']
        self.course = self.db.tweets


    def save_tweets(self, df):
        for tweet in df:
            dict = {}
            dict['text'] = tweet['text']
            dict['id'] = tweet['id']
            dict['len'] = tweet['len']
            dict['created'] = tweet['created']
            dict['source'] = tweet['source']
            dict['likes'] = tweet['likes']
            dict['retweet'] = tweet['retweet']
