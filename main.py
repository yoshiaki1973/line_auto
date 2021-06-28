from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
import os

app = Flask(__name__)

#環境変数
YOUR_CHANNEL_ACCESS_TOKEN = "'fWpix0KEHR8g63I7ZIcwG8ykFMaU9W3Dn5CUO5j53aSS7zf085ismul+VXf18X7eq3fVo5oG+2SxjB+HygboMexznrAQcxla8Cu2uNTwYxEIGJbmflsSJXvw/DXxzr22A8ie148FcmErbK0i7h9yugdB04t89/1O/w1cDnyilFU="
YOUR_CHANNEL_SECRET = "b7fd868e3294cb9b4b0c3561c3434d1f"

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

#Webhookからのリクエストをチェックします。
@app.route("/callback", methods=['POST'])
def callback():
    # リクエストヘッダーから署名検証のための値を取得します。
    signature = request.headers['X-Line-Signature']
 
    # リクエストボディを取得します。
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
 
    # handle webhook body
    # 署名を検証し、問題なければhandleに定義されている関数を呼び出す。
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

#LINEのメッセージの取得と返信内容の設定 
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(event.reply_token,TextSendMessage(text="『{0}』".format(event.message.text))) 

#-------------------------------------------------------------------------------------------------
# ポート番号の設定
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

