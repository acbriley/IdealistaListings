from dotenv import load_dotenv
import os
import json
import requests
import time
import pandas as pd

load_dotenv()
# Sets the name to look for enviroment variables
API_KEY = os.getenv('API_KEY')
# get the Oauth token from API


def get_oauth_token():
    """Gets oauth2 token from the API Key and Secret provided by idealista
    """
    oauth_url = "https://api.idealista.com/oauth/token"
    payload = "grant_type=client_credentials&scope=read"
    headers = {}
    headers["Authorization"] = 'Basic ' + API_KEY
    headers["Content-Type"] = "application/x-www-form-urlencoded"
    r = requests.post(oauth_url, headers=headers, data=payload)

    return r.text


url = 'https://api.idealista.com/3.5/es/search?center=41.387471,2.169743&country=es&maxItems=500&distance=3000&propertyType=homes&operation=sale&minSize=60&bedrooms=2&numPage='

# Search Idealista API using parameters


def search(url, token):
    headers = {"Authorization": "Bearer " + token}
    r = requests.post(url, headers=headers)
    # print(r.text)
    return r.text


token_json = get_oauth_token()
token_resp = json.loads(token_json)
access_token = token_resp["access_token"]

# search_json = search(url, access_token)
# search_resp = json.loads(search_json)
# search_list = search_resp['elementList']

search_list = []
for i in range(1, 6):
    url = url + 'i'

    search_json = search(url, access_token)
    search_resp = json.loads(search_json)
    search_list.append(search_resp['elementList'])

results = []
for i in search_list:
    for item in i:
        results.append(item)

# dump json data into a json file
with open("data/idealista_json_" + time.strftime("%Y-%m-%d") + ".json", 'w') as export:
    json.dump(results, export)

# turn search list into an excel file indexed at 1
df = pd.DataFrame(results)
df.index = df.index + 1

# clean data by dropping unwatned columns
to_drop = ['has360', 'hasPlan', 'suggestedTexts', 'status', 'description', 'showAddress', 'topNewDevelopment', 'superTopHighlight', 'hasStaging', 'propertyCode', 'numPhotos', 'externalReference', 'operation', 'province', 'country',
           'distance', 'hasVideo', 'newDevelopment', 'detailedType', 'has3DTour', 'municipality', 'topNewDevelopment', 'superTopHighlight']

df.drop(columns=to_drop, inplace=True, axis=1)

df.to_excel('./data/data.xlsx', index=True)
