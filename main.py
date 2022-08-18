import flask
from flask import Flask, Response
import requests
app = Flask(__name__)

TOKEN = '5631145263:AAF9gy8BDngcB1otAMC_P-a1ro1r3AIbxGA'
TELEGRAM_INIT_WEBHOOK_URL = 'https://api.telegram.org/bot{}/setWebhook?url=https://ac84-82-80-173-170.ngrok.io/message'.format(TOKEN)

requests.get(TELEGRAM_INIT_WEBHOOK_URL)


@app.route('/')
def home():
    return "Welcome Home"


@app.route('/sanity')
def sanity():
    return "Server is running"


@app.route('/message', methods=["POST"])
def handle_message():
    message = flask.request.get_json()['message']['text']
    chat_id = flask.request.get_json()['message']['chat']['id']
    res = requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
                       .format(TOKEN, chat_id, "Got it"))
    return Response("202")
    

if __name__ == '__main__':
    app.run(port=5002)
