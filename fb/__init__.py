import facebook
import requests
from util import Utils

APP_ID = ''
APP_SECRET = ''
ACCESS_TOKEN = ''

g = facebook.GraphAPI(ACCESS_TOKEN)

friends_likes = g.get_object('me', fields='friends.fields(id, name, likes)')
while 'paging' in friends_likes['friends']:
    friends_likes = g.get_connections('me', 'friends&after={}'.format(friends_likes['friends']['paging']['cursors']['after']))
    print(friends_likes)
