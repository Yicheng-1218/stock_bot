import os
from web_crawler import *
from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)

# Linebot sdk models
# https://github.com/line/line-bot-sdk-python
from linebot.models import (
    MessageEvent, TextMessage, StickerMessage, TextSendMessage, StickerSendMessage, LocationSendMessage, ImageSendMessage, TemplateSendMessage, ButtonsTemplate, PostbackAction, MessageAction, URIAction, CarouselTemplate, CarouselColumn
)

app = Flask(__name__)

# LINE API為辨識開發者身份所需的資料
CHANNEL_ACCESS_TOKEN = 'SJSoAEGKK4nj58UHAluyb6y18wAdeOUn/F163A1BEHGjI7BLUaFz/2rnRhskf2k9w/7XzOpwsCnZTcztjxjOEv/c2J0GuUd0RPcyQIfNLMzPt6WWxJ5XnMoYp4uBCsNJ7iG95AIAursQ/5xbpyq7aQdB04t89/1O/w1cDnyilFU='
CHANNEL_SECRET = '1a3c17ab604b6365246d4d6fe5f4c7e8'

# ************ X-LINE-SIGNATURE START ************
line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)


@app.route("/webhook", methods=['POST'])
def callback():
    # 當LINE發送訊息給機器人時，從header取得 X-Line-Signature
    # X-Line-Signature 用於驗證頻道是否合法
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'
# ************ X-LINE-SIGNATURE END ************


@app.route('/')
def home():
    return 'linebot on working'


# Text message handler
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print('[使用者傳入文字訊息]')
    print(str(event))
    # 取得使用者說的文字
    user_msg = event.message.text
    stock_report = get_stock_info(user_msg)
    # 準備要回傳的文字訊息
    reply = stock_report
    line_bot_api.reply_message(
        event.reply_token,
        reply)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    dev_host = "127.0.0.1"
    heroku_host = "0.0.0.0"
    host = heroku_host
    print(f"[Application running on {host}:{port}]")
    app.run(host=host, port=port, debug=True)
