import telepot
import os
import re
import random
import string
from flask import Flask, request
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = os.environ.get("(8804083457:AAFVXlNEvvuQxwyLskKOoRjvtd_Dq6eV8OU)")

SECRET = ''.join(random.choice(string.ascii_letters) for _ in range(20))

app = Flask(__name__)

bot = telepot.Bot(TOKEN)

regex = [
    r'^[!/](start)',
    r'^[!/](echo) (.*)'
]


def parser(msg, matches):
    usr = msg['from']

    if msg['type'] == "text":

        if matches[0] == 'start':
            text = "Welcome!"

            markup = InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text='BTN1',
                            callback_data='btn1'
                        ),
                        InlineKeyboardButton(
                            text='BTN2',
                            callback_data='btn2'
                        )
                    ]
                ]
            )

            bot.sendMessage(
                usr['id'],
                text,
                reply_markup=markup
            )
            return

        if matches[0] == 'echo' and matches[1]:
            bot.sendMessage(
                usr['id'],
                matches[1]
            )
            return


def processing(msg):

    if 'chat' in msg and msg['chat']['type'] == 'channel':
        return

    if 'text' in msg:
        msg['text'] = str(msg['text'])
        msg['type'] = 'text'

    elif 'data' in msg:
        msg['type'] = 'callback'
        msg['text'] = f"%callback {msg['data']}"

    else:
        msg['type'] = 'nontext'

        types = [
            'audio',
            'voice',
            'document',
            'photo',
            'video',
            'contact',
            'location'
        ]

        for t in types:
            if t in msg:
                msg['text'] = f'%{t}'
                break

    if 'text' in msg:

        for entry in regex:

            m = re.match(entry, msg["text"])

            if m:
                parser(msg, list(m.groups()))
                return


@app.route("/", methods=["GET"])
def home():
    return "Bot running"


@app.route("/webhook", methods=["POST"])
def webhook():

    update = request.get_json()

    if "message" in update:
        processing(update["message"])

    elif "callback_query" in update:
        processing(update["callback_query"])

    return "OK"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
