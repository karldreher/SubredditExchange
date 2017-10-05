from flask import Flask, request, render_template
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


def user_agent():
    return app_user_agent

def base_headers():
    return {"User-Agent": user_agent()}

def save_created_state(state):
    pass
def is_valid_state(state):
    return True


app = Flask(__name__)
@app.route("/")

def make_authorization_url():
    # Generate a random string for the state parameter
    # Save it for use later to prevent xsrf attacks
    state = str(uuid4())
    save_created_state(state)
    params = {"client_id": app_client_id,
              "response_type": "code",
              "state": state,
              "redirect_uri": app_redirect_uri,
              "duration": "temporary",
              "scope": "identity,mysubreddits"}
    url = "https://www.reddit.com/api/v1/authorize?" + urllib.parse.urlencode(params)
    return url


def subreddit_exchange_app():
    return render_template('index.html', url=make_authorization_url())



@app.route("/reddit_callback")
def reddit_callback():
    error = request.args.get('error', '')
    if error:
        return "Error: " + error
    state = request.args.get('state', '')
    if not is_valid_state(state):
        # Uh-oh, this request wasn't started by us!
        abort(403)
    code = request.args.get('code')
    access_token = get_token(code)
    return "Your reddit username is: %s" % get_username(access_token)

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


def get_username(access_token):
    headers = base_headers()
    headers.update({"Authorization": "bearer " + access_token})
    response = requests.get("https://oauth.reddit.com/api/v1/me", headers=headers)
    me_json = response.json()
    return me_json['name']




if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)



