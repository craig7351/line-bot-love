from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os
from dotenv import load_dotenv
from bot_logic import process_message

load_dotenv()

app = Flask(__name__)

# Line Bot Configuration
CHANNEL_ACCESS_TOKEN = os.getenv('CHANNEL_ACCESS_TOKEN')
CHANNEL_SECRET = os.getenv('CHANNEL_SECRET')

if not CHANNEL_ACCESS_TOKEN or not CHANNEL_SECRET:
    print("Warning: Line Bot credentials not found in environment variables.")

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers.get('X-Line-Signature')

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    original_text = event.message.text
    
    # Optional logic: Only reply if mentioned or in specific mode? 
    # For this request, the bot is "adding to chat" so maybe it replies to everything?
    # Or maybe it proactively translates only "harsh" messages?
    # For simplicity based on prompt: "Machine: ..." implies a reply.
    
    warm_text = process_message(original_text)
    
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=warm_text)
    )

if __name__ == "__main__":
    app.run(port=5000, debug=True)
