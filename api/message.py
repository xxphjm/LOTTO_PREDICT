#這些是LINE官方開放的套件組合透過import來套用這個檔案上
from linebot.v3.messaging import TemplateMessage, ButtonsTemplate, MessageAction



#TemplateSendMessage - ButtonsTemplate (按鈕介面訊息)
def time_range_message(lottery_type):
    message = TemplateMessage(
            alt_text=f"{lottery_type}預測時間範圍選擇",
            template=ButtonsTemplate(
                title=f"選擇{lottery_type}預測時間範圍",
                text=f"請選擇{lottery_type}分析的歷史資料範圍",
                actions=[
                    MessageAction(
                        label="半年",
                        text="半年"
                    ),
                    MessageAction(
                        label="一年",
                        text="一年"
                    ),
                    MessageAction(
                        label="二年",
                        text="二年"
                    )
                ]
            )
        )
    return message
def lottery_type_message():
    message=TemplateMessage(
            alt_text="選擇彩券類型",
            template=ButtonsTemplate(
                title="選擇彩券類型",
                text="請選擇要預測的彩券類型",
                actions=[
                    MessageAction(
                        label="大樂透",
                        text="大樂透"
                    ),
                    MessageAction(
                        label="威力彩",
                        text="威力彩"
                    )
                ]
            )
        )
    return message

# #TemplateSendMessage - ConfirmTemplate(確認介面訊息)
# def Confirm_Template():

#     message = TemplateSendMessage(
#         alt_text='是否註冊成為會員？',
#         template=ConfirmTemplate(
#             text="是否註冊成為會員？",
#             actions=[
#                 PostbackTemplateAction(
#                     label="馬上註冊",
#                     text="現在、立刻、馬上",
#                     data="會員註冊"
#                 ),
#                 MessageTemplateAction(
#                     label="查詢其他功能",
#                     text="查詢其他功能"
#                 )
#             ]
#         )
#     )
#     return message

