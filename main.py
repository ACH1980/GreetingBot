#!/usr/bin/env python3

from telegram.ext import CommandHandler, MessageHandler, Filters, Updater
from telegram import Message, Update
from telegram.ext import BaseFilter
import string
import json
import time
import logging
import signal
import sys

try:
    file = open("config.json", "r")
    conf_raw = file.read()
    file.close()
except FileNotFoundError:
    exit(1)
j = json.loads(conf_raw)
if "token" not in j or len(j["token"]) <= 0:
    print("no token in config.json")
    exit(1)
if "msg" not in j or len(j["msg"]) <= 0:
    print("no msg in config.json")
    exit(1)


class GreetFilter(BaseFilter):
    def filter(self, message: Message):
        if len(message.new_chat_members) > 0:
            return True
        return False

def greet(bot, update: Update):
    for user in update.message.new_chat_members:
        tmp_msg = j["msg"].replace("$FIRSTNAME", user.first_name)
        bot.send_message(chat_id=update.message.chat_id, text=tmp_msg)

# bot
updater = Updater(token=j["token"])
dispatcher = updater.dispatcher
# logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Remember to initialize the class.
greet_handler = MessageHandler(GreetFilter(), greet)
dispatcher.add_handler(greet_handler)

# start bot
updater.start_polling()
print("Bot is running.")
# wait till sigint
def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        updater.stop()
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)
print('Press Ctrl+C')
signal.pause()
