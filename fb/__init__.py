import facebook
import requests
from util import Utils

APP_ID = '1904193739907094'
APP_SECRET = 'c5eaa6d673acd89bf037e32210e77e01'
ACCESS_TOKEN = 'EAACEdEose0cBAOGaGTaC7MwvPGV9wIXG3xbosZBogcXxaZCggMSiSCJF1YijQqhf0ULZAGr3CN2GFSwZBTgPraiMV8qxKxWgK5ScDX4SwX7k9gfhhgZAxeSXc1cEiC0NSOPMcYHnzkLJDGJ5MgIcVGsJ6aic2sINcxKYyPPr33vcdeuec5GJpfjxGV8WzDZCJKB7Hk8sPJXgZDZD'

g = facebook.GraphAPI(ACCESS_TOKEN)

friends_likes = g.get_object('me', fields='friends.fields(id, name, likes)')
while 'paging' in friends_likes['friends']:
    friends_likes = g.get_connections('me', 'friends&after={}'.format(friends_likes['friends']['paging']['cursors']['after']))
    print(friends_likes)
