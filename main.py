from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

import os

import reply_message


app = Flask(__name__)

CHANNEL_ACCESS_TOKEN = os.environ["CHANNEL_ACCESS_TOKEN"]
CHANNEL_SECRET = os.environ["CHANNEL_SECRET"]

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handoler = WebhookHandler(CHANNEL_SECRET)


@app.route('/callback', methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handoler.handle(body, signature)
    except InvalidSignatureError:
        print('Invalid signature. Please check your channel access token/channel secret.')
        abort(400)

    return 'OK'

@handoler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_message.make_reply(event.message.text)))



if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
