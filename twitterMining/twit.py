import json
import twitter
import matplotlib.pyplot as plt
from collections import Counter
from prettytable import PrettyTable

CONSUMER_KEY = ''
CONSUMER_SECRET = ''
OAUTH_TOKEN = ''
OAUTH_SECRET = ''

auth = twitter.OAuth(OAUTH_TOKEN, OAUTH_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
twitter_api = twitter.Twitter(auth=auth)

q = '#respectdiversity'
count = 100
search_results = twitter_api.search.tweets(q=q, count=count)
statuses = search_results['statuses']
total_tweets = len(statuses)

while True:
    try:
        next_results = search_results['search_metadata']['next_results']
    except KeyError as e:
        print('total {} twits collected'.format(total_tweets))
        with open('keyword_tweets.json', 'w', encoding='utf8') as makefile:
            json.dump(statuses, makefile, ensure_ascii=False, indent=4)
        break
    search_args = dict([kv.split('=') for kv in next_results[1:].split('&')])
    search_results = twitter_api.search.tweets(**search_args)
    statuses += search_results['statuses']
    total_tweets += len(search_results['statuses'])

status_texts = [status['text'] for status in statuses]
screen_names = [
    user_mention['screen_name']
    for status in statuses
    for user_mention in status['entities']['user_mentions']
]
hashtags = [
    hashtag['text']
    for status in statuses
    for hashtag in status['entities']['hashtags']
]
words = [
    word for text in status_texts
    for word in text.split()
]

for item in [words, screen_names, hashtags]:
    c = Counter(item)
    # top ten
    print(c.most_common()[:10])
    print()

for label, data in (('Word', words), ('Screen Name', screen_names), ('Hashtag', hashtags)):
    pt = PrettyTable(field_names=[label, 'Count'])
    c = Counter(data)
    for kv in c.most_common()[:10]:
        pt.add_row(kv)
    pt.align[label], pt.align['count'] = 'l', 'r'
    print(pt)


def lexical_diversity(tokens):
    """
    calculates lexical diversity of tokens
    """
    return len(set(tokens)) / len(tokens)


def average_words(statuses):
    """
    computes average words for tweet
    """
    total_words = sum([len(s.split()) for s in statuses])
    return total_words / len(statuses)

print(lexical_diversity(words))
print(lexical_diversity(screen_names))
print(lexical_diversity(hashtags))
print(average_words(status_texts))

# examining retweets
retweets = [
    (status['retweet_count'],
    status['retweeted_status']['user']['screen_name'],
    status['text'])
    for status in statuses if 'retweeted_status' in status
]

with open('retweets.json', 'w', encoding='utf8') as makefile:
    json.dump(retweets, makefile, indent=4, ensure_ascii=False)

pt = PrettyTable(field_names=['Count', 'Screen Name', 'Text'])
for row in sorted(retweets, reverse=True)[:10]:
    pt.add_row(row)
pt.align = 'l'
print(pt)

counts = [count for count, _, _ in retweets]
plt.hist(counts)
plt.title('retweets')
plt.xlabel('Bins(number of times retweeted)')
plt.ylabel('Number of tweets in bin')

plt.show()
