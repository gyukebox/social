import json
import twitter
import matplotlib.pyplot as plt
from collections import Counter
from prettytable import PrettyTable


class Mining:
    def __init__(self, consumer_key, consumer_secret, oauth_token, oauth_secret):
        self.auth = twitter.OAuth(consumer_key, consumer_secret, oauth_token, oauth_secret)
        self.api = twitter.Twitter(auth=self.auth)

    def search_trends(self, loc_id):
        trends = self.api.trends.place(_id=loc_id)
        return trends

    def search_by_keyword(self, keyword, count=100):
        initial_search = self.api.search.tweets(q=keyword, count=count)
        statuses = initial_search['statuses']
        total_tweets = len(statuses)
        while True:
            try:
                next_results = initial_search['search_metadata']['next_results']
            except KeyError:
                print('total {} twits collected'.format(total_tweets))
                return statuses
            search_args = dict([kv.split('=') for kv in next_results[1:].split('&')])
            initial_search = self.api.search.tweets(**search_args)
            statuses += initial_search['statuses']
            total_tweets += len(initial_search['statuses'])


    @staticmethod
    def store_json(result, filename):
        json_file = '{}.json'.format(filename)
        with open(json_file, 'w', encoding='utf8') as makefile:
            json.dump(result, makefile, ensure_ascii=False, indent=4)
