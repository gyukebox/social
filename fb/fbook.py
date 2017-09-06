import facebook
import json
import requests
from util import Utils

APP_ID = ''
APP_SECRET = ''
ACCESS_TOKEN = ''


def pp(material):
    print(json.dumps(material, indent=2, ensure_ascii=False))

# Create a connection to the Graph API with your access token
g = facebook.GraphAPI(ACCESS_TOKEN)  # Execute a few sample queries
result = g.get_object('me', fields='id, name, likes')['likes']
data = result['data']

while True:
    try:
        nexturl = result['paging']['next']
        result = requests.get(nexturl).json()
        for element in result['data']:
            data.append(element)
        print(result)
        print('--------------------')
    except KeyError:
        count = len(data)
        json_packed = {
            "data": data,
            "element_count": count
        }
        Utils.store_json(json_packed, 'result.json')
        break
