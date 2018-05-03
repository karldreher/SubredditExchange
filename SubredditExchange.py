from flask import jsonify
from uuid import uuid4
import requests
import requests.auth
import urllib
import yaml

with open("config.yaml", 'r') as config:
    try:
        config = yaml.load(config)

        app_client_id = config['app_client_id']
        app_client_secret = config['app_client_secret']
        app_user_agent = config['app_user_agent']
        app_redirect_uri = config['app_redirect_uri']
        
    except yaml.YAMLError as exc:
        print('Error opening config file: '.config(exc))


def base_headers():
    return {"User-Agent": app_user_agent}


def make_authorization_url():
    # Generate a random string for the state parameter
    # Save it for use later to prevent xsrf attacks
    state = str(uuid4())
    params = {"client_id": app_client_id,
              "response_type": "code",
              "state": state,
              "redirect_uri": app_redirect_uri,
              "duration": "temporary",
              "scope": "identity,mysubreddits"}
    url = "https://www.reddit.com/api/v1/authorize?" + urllib.parse.urlencode(params)
    return url


def get_token(code):
    client_auth = requests.auth.HTTPBasicAuth(app_client_id, app_client_secret)
    post_data = {"grant_type": "authorization_code",
                 "code": code,
                 "redirect_uri": app_redirect_uri}
    headers = base_headers()
    response = requests.post("https://ssl.reddit.com/api/v1/access_token",
                             auth=client_auth,
                             headers=headers,
                             data=post_data)
    token_json = response.json()
    return token_json["access_token"]


def get_userdata(access_token):
    headers = base_headers()
    headers.update({"Authorization": "bearer " + access_token})
    username_response = requests.get("https://oauth.reddit.com/api/v1/me", headers=headers)
    me_json = username_response.json()
    subreddit_response = requests.get("https://oauth.reddit.com/subreddits/mine/subscriber", headers=headers)
    subreddits = subreddit_response.json()
    return jsonify(subreddits)


def parse(jsondata):
    subreddit_list = set()
    for item in jsondata['data']['children']:
        subreddit = {}
        subreddit['name']=item['data']['display_name_prefixed']
        subreddit_list.add(subreddit['name'])
    return subreddit_list

