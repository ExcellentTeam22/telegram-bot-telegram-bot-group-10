import telegram
from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CommandHandler


telegram_bot_token = '5305762324:AAFQ91-TWlw-Bu9V258WEdYcC16OzL5c7xU'

updater = Updater(token=telegram_bot_token, use_context=True)
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

def inet(update, context):
    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id=chat_id, text="Please provide me some data:\n"
                                                   "1)/start\n"
                                                   "2)/help")


# set up the introductory statement for the bot when the /start command is invoked
def start(update, context):
    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id=chat_id, text="Please provide me some data:\n"
                                                   "1)/gameplay\n"
                                                   "2)/trailer")


def game_play(update, context):
    context.user_data['key'] = "gameplay"
    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id=chat_id, text="Hello there.\nplease provide me with game name to get gameplay "
                                                   "videos")


def trailer(update, context):
    context.user_data['key'] = 'trailer'
    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id=chat_id, text="Hello there.\nplease provide me with game name to get trailer "
                                                   "videos")


def get_game_info(update, context):
    if context.user_data['key'] == 'trailer':
        update.message.reply_text(f"You will get the trailer for gta{update.message.text}")
    elif context.user_data['key'] == 'gameplay':
        update.message.reply_text(f"You will get the game play for gta{update.message.text}")
    else:
        update.message.reply_text("please chose first what did you want")

# dispatcher.add_handler(CommandHandler("", inet))

# run the start function when the user invokes the /start command
dispatcher.add_handler(CommandHandler("start", start))

dispatcher.add_handler(CommandHandler("gameplay", game_play))

dispatcher.add_handler(CommandHandler("trailer", trailer))
# invoke the get_word_info function when the user sends a message
# that is not a command.
dispatcher.add_handler(MessageHandler(Filters.text, get_game_info))
updater.start_polling()
