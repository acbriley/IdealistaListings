from dotenv import load_dotenv
import json
import requests
import time


load_dotenv()
# Sets the name to look for enviroment variables

# get the Oauth token from API


def get_oauth_token():
    """Gets oauth2 token from the API Key and Secret provided by idealista
    """
    oauth_url = "https://api.idealista.com/oauth/token"
    payload = "grant_type=client_credentials&scope=read"
    headers = {}
    headers["Authorization"] = 'APIKEY'
    headers["Content-Type"] = "application/x-www-form-urlencoded"
    r = requests.post(oauth_url, headers=headers, data=payload)

    return r.text


# Search Idealista API using parameters
def search(token):
    url = 'https://api.idealista.com/3.5/es/search?center=41.387471,2.169743&country=es&maxItems=500&numPage=(1,2,3,4,5,6,7,8,9,10)&distance=452&propertyType=homes&operation=sale&minSize=60&bedrooms=2'
    headers = {"Authorization": "Bearer " + token}
    r = requests.post(url, headers=headers)
    # print(r.text)
    return r.text


token_json = get_oauth_token()
token_resp = json.loads(token_json)
access_token = token_resp["access_token"]

search_json = search(access_token)
search_resp = json.loads(search_json)
search_pretty = json.dumps(search_resp, indent=4, sort_keys=True)


# dump json data into a json file
with open("data/idealista_json_" + time.strftime("%Y-%m-%d") + ".json", 'w') as export:
    json.dump(search_pretty, export)
