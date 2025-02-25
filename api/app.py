from flask import Flask, request, jsonify,abort
from dateutil.relativedelta import relativedelta
from api.lotto_history import fetch_history_data
from linebot.v3.webhooks import MessageEvent, PostbackEvent,TextMessageContent
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage,
    ShowLoadingAnimationRequest
)
from linebot.v3.webhook import WebhookParser
from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import InvalidSignatureError
import os
from dotenv import load_dotenv
from api.message import time_range_message,lottery_type_message
from api.llm import get_groq_completion

app = Flask(__name__)
load_dotenv()
access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
channel_secret = os.getenv("LINE_CHANNEL_SECRET")  # 添加 channel_secret
configuration = Configuration(access_token=access_token)
api_client = ApiClient(configuration)
messaging_api = MessagingApi(api_client)  # 創建 messaging api 實例
handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))
user_states = {}

@app.route("/", methods=['GET'])
def root():
    return {"message": "LINE Bot API is running"}

@app.route("/callback", methods=['POST'])
def callback():
    # 取得 X-Line-Signature header 的值
    signature = request.headers['X-Line-Signature']

    # 取得請求內容
    body = request.get_data(as_text=True)

    try:
        # 驗證簽章
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'
def callback():
    # 取得 X-Line-Signature header 的值
    signature = request.headers['X-Line-Signature']

    # 取得請求內容
    body = request.get_data(as_text=True)

    try:
        # 驗證簽章
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'
@handler.add(MessageEvent, message=TextMessageContent)
def handle_text_message(event):
    user_id = event.source.user_id
    message_text = event.message.text
    if "預測樂透" in message_text:
        buttons = lottery_type_message()
    # 設置使用者狀態為等待選擇彩券類型
        user_states[user_id] = {"state": "waiting_lottery_type"}
        
        messaging_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[buttons]
            )
        )
        return
    # 處理彩券類型選擇
    if user_id in user_states and user_states[user_id]["state"] == "waiting_lottery_type":
        if message_text in ["大樂透", "威力彩"]:
            lottery_type = message_text
            seqNo = "649" if lottery_type == "大樂透" else "638"
            
            # 更新使用者狀態
            user_states[user_id].update({
                "state": "waiting_time_range",
                "lottery_type": lottery_type,
                "seqNo": seqNo
            })
            time_range = time_range_message(lottery_type)
            messaging_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[time_range]
                )
            )
            return
   # 處理時間範圍選擇
    if user_id in user_states and user_states[user_id]["state"] == "waiting_time_range":
        period = None
        if "半年" in message_text:
            period = "半年"
        elif "一年" in message_text:
            period = "一年"
        elif "三年" in message_text:
            period = "三年"
        
        if period:
            seqNo = user_states[user_id]["seqNo"]
            lottery_type = user_states[user_id]["lottery_type"]
            messaging_api.show_loading_animation(ShowLoadingAnimationRequest(chatId=event.source.user_id, loadingSeconds=10))
            # 根據指令抓取歷史資料
            results = fetch_history_data(period, seqNo)
            if results:
                reply_lines = [f"抓取{lottery_type} {period}資料，共 {len(results)} 筆:"]
                for draw in results:
                    reply_lines.append(
                        f"期號：{draw['period']} | 開獎號碼：{draw['winning_numbers']} |特別號:{draw['special_number']}| 開獎日期：{draw['draw_date']}")
                reply_message = "\n".join(reply_lines)
                
                # 使用LLM模型進行分析
                analysis_result = get_groq_completion(reply_message)
                reply_message = analysis_result
            else:
                reply_message = f"{period}期間內無{lottery_type}資料。"

            # 清除使用者狀態
            del user_states[user_id]
            
            messaging_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text=reply_message)]
                )
            )
            return
    
    else:
        reply_message = "請輸入有效指令"
        messaging_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=reply_message)]
            )
        )
    





