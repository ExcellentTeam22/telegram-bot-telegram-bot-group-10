import flask
from flask import Flask, Response
import requests
import math

app = Flask(__name__)
URL = "https://67f9-82-80-173-170.ngrok.io"
TOKEN = '5631145263:AAF9gy8BDngcB1otAMC_P-a1ro1r3AIbxGA'
TELEGRAM_INIT_WEBHOOK_URL = f'https://api.telegram.org/bot{TOKEN}/setWebhook?url={URL}/message'

requests.get(TELEGRAM_INIT_WEBHOOK_URL)


@app.route('/message', methods=["POST"])
def handle_message():

    try:
        flask.request.get_json()['message']["entities"][0]["type"]
    except:
        return Response("202")

    message = flask.request.get_json()['message']['text']

    answer = "Operation is not allowed"

    split_message = message.split()
    if message[0] == '/':
        answer = function_pointers[split_message[0]](int(split_message[1]))

    chat_id = flask.request.get_json()['message']['chat']['id']
    res = requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={answer}")
    return Response("202")


def prime(user_num):
    is_prime = True

    if user_num % 2 == 0:
        return "not prime!"

    for divider in range(3, int(math.sqrt(user_num)) + 1):
        if user_num % divider == 0:
            is_prime = False

    if is_prime:
        return "prime"
    else:
        return "not prime"


def factorial(n):
    i = 1
    while True:
        if n % i == 0:
            n //= i

        else:
            break

        i += 1

    if n == 1:
        return "Is factorial"

    else:
        return "Is not factorial"


def sqrt(n):
    i = 1
    while i * i <= n:
        if (n % i == 0) and (n / i == i):
            return "Is a perfect square"

        i = i + 1
    return "Is not a perfect square"


def palindrome(n):
    temp = n
    rev = 0
    while n > 0:
        dig = n % 10
        rev = rev * 10 + dig
        n = n // 10
    if temp == rev:
        return "The number is a palindrome!"
    return "The number isn't a palindrome!"


function_pointers = {"/prime": prime,
                     "/sqrt": sqrt,
                     "/factorial": factorial,
                     "/palindrome": palindrome}

if __name__ == '__main__':
    app.run(port=5002)
