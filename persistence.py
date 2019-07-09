from pymongo import MongoClient

class Persistence():
    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017')
        self.db = self.client['twitter-database']
        self.tweets = self.db.tweets


    def save_tweets(self, df):
        data = df.to_dict(orient='records')
        self.tweets.insert_many(data)
        print(data)
