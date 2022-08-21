import telegram
from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CommandHandler
import requests

GAME_SPOT_TOKEN = '80c9a7077dc128cce43c6b68296faea8b7fc2324'
GAMES_API = 'https://www.gamespot.com/api/games/?api_key={}'.format(GAME_SPOT_TOKEN)
TOKEN = '5631145263:AAF9gy8BDngcB1otAMC_P-a1ro1r3AIbxGA'

updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

var = {
    "commands": [
        {
            "command": "start",
            "description": "Start using bot"
        },
        {
            "command": "help",
            "description": "Display help"
        },
        {
            "command": "menu",
            "description": "Display menu"
        }
    ],
    "language_code": "en"
}


# setup the introductory statement for the bot when the /start command is invoked
def start(update, context):
    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id=chat_id, text="What's the name of the game?")


def game_play(update, context):
    chat_id = update.effective_chat.id

    res = requests.get('{}&format=json&limit=5&filter=name:{}'.format(GAMES_API, context.user_data["key"]),
                       headers={'User-agent': 'Mozilla/5.0'})
    if not res.json()["results"]:
        context.bot.send_message(chat_id=chat_id,
                                 text="We dont find a game called " +
                                      context.user_data["key"] + "."
                                                                 " Please provide the full name of the game")
        return

    video_api = res.json()["results"][0]["videos_api_url"] + \
                ",title:gameplay&api_key={}&format=json&limit=5".format(GAME_SPOT_TOKEN)

    res = requests.get(video_api, headers={'User-agent': 'Mozilla/5.0'})

    for video in res.json()["results"]:

        try:
            trailer_low_quality = video["low_url"]
        except:
            context.bot.send_message(chat_id=chat_id,
                                     text="We dont find a gameplay for " + context.user_data["key"])
            return

        context.bot.send_message(chat_id=chat_id, text=trailer_low_quality)


def trailer(update, context):
    chat_id = update.effective_chat.id

    res = requests.get('{}&format=json&limit=1&filter=name:{}'.format(GAMES_API, context.user_data["key"]),
                       headers={'User-agent': 'Mozilla/5.0'})
    if not res.json()["results"]:
        context.bot.send_message(chat_id=chat_id,
                                 text="We dont find a game called " +
                                      context.user_data["key"] + "."
                                                                 " Please provide the full name of the game")
        return

    video_api = res.json()["results"][0]["videos_api_url"] + \
                ",title:trailer&api_key={}&format=json&limit=1".format(GAME_SPOT_TOKEN)

    res = requests.get(video_api, headers={'User-agent': 'Mozilla/5.0'})

    trailer_object = res.json()["results"][0]

    try:
        trailer_low_quality = trailer_object["low_url"]
    except:
        context.bot.send_message(chat_id=chat_id,
                                 text="We dont find a trailer for " + context.user_data["key"])
        return

    context.bot.send_message(chat_id=chat_id, text=trailer_low_quality)


def description(update, context):
    res = requests.get('{}&format=json&limit=10&filter=name:{}'.format(GAMES_API, context.user_data["key"]),
                       headers={'User-agent': 'Mozilla/5.0'})
    chat_id = update.effective_chat.id

    descrip = res.json()["results"][0]["description"]

    if not descrip:
        descrip = "There is no description for {}".format(context.user_data["key"])

    context.bot.send_message(chat_id=chat_id, text=descrip)


def get_game_info(update, context):
    context.user_data['key'] = update.message.text
    chat_id = update.effective_chat.id

    context.bot.send_message(chat_id=chat_id,
                             text="Please provide what service you want, /gameplay, /trailer, /description")


# dispatcher.add_handler(CommandHandler("", inet))

# run the start function when the user invokes the /start command
dispatcher.add_handler(CommandHandler("start", start))

dispatcher.add_handler(CommandHandler("gameplay", game_play))

dispatcher.add_handler(CommandHandler("trailer", trailer))

dispatcher.add_handler(CommandHandler("description", description))
# invoke the get_word_info function when the user sends a message
# that is not a command.
dispatcher.add_handler(MessageHandler(Filters.text, get_game_info))
updater.start_polling()
