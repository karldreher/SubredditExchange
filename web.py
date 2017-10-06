from flask import Flask, request, render_template
import SubredditExchange as srx


app = Flask(__name__)
@app.route("/")

def subreddit_exchange_app():
    return render_template('index.html', url=srx.make_authorization_url())


@app.route("/reddit_callback")

def reddit_callback():
    error = request.args.get('error', '')
    if error:
        return "Error: " + error
    code = request.args.get('code')
    access_token = srx.get_token(code)
    return srx.get_userdata(access_token)




if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)



