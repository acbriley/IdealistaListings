from dotenv import load_dotenv
import json
import requests


load_dotenv()
# Sets the name to look for enviroment variables


def get_oauth_token():
    """Gets oauth2 token from the API Key and Secret provided by idealista
    """
    oauth_url = "https://api.idealista.com/oauth/token"
    payload = "grant_type=client_credentials&scope=read"
    headers = {}
    headers["Authorization"] = "API_KEY"
    headers["Content-Type"] = "application/x-www-form-urlencoded"
    r = requests.post(oauth_url, headers=headers, data=payload)
    return r.text


# Fix Search Function. Returning a 405 error
def search(token):
    url = 'http://api.idealista.com/3.5/es/search?center=41.387471,2.169743&country=es&maxItems=500&numPage=1&distance=452&propertyType=homes&operation=sale&minSize=60&bedrooms=2'
    headers = {"Authorization": "Bearer " + token}
    r = requests.post(url, headers=headers)
    # print(r.text)
    return r.text


token_json = get_oauth_token()
token_resp = json.loads(token_json)
access_token = token_resp["access_token"]

search_json = search(access_token)
search_resp = json.loads(search_json)
print(search_resp)
