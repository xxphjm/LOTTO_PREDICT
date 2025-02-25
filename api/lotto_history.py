import requests
import datetime
import time
from dateutil.relativedelta import relativedelta
from datetime import datetime as dt
def fetch_superlotto_data(year, month,seqNo):
    """
    根據指定的年與月，呼叫大樂透 API。
    API 格式： https://api.taiwanlottery.com/TLCAPIWeB/Lottery/SuperLotto{seqNo}Result?period&month=YYYY-MM
    """
    if seqNo == "649":
        base_url = f"https://api.taiwanlottery.com/TLCAPIWeB/Lottery/Lotto{seqNo}Result"
    else:
        base_url = f"https://api.taiwanlottery.com/TLCAPIWeB/Lottery/SuperLotto{seqNo}Result"

    month_str = f"{year}-{month:02}"
    params = {
        "month": month_str
    }
    print(f"正在抓取 {month_str} 資料...")
    try:
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()   # 若狀態碼非 200，則拋出例外
        data = response.json()
        return data
    except Exception as e:
        print(f"取得 {month_str} 資料時發生錯誤：{e}")
        return None

def process_superlotto_json(json_data,seqNo):
    """
    處理 API 回傳的 JSON，僅提取「當期期號」、「開獎號碼」以及「開獎日期」。
    假設 JSON 結構包含一個清單，內部每筆資料為字典，鍵值分別可能為：
      - 'period' 或 '期別'
      - 'Numbers' 或 '開獎號碼'
      - 'DrawDate' 或 '開獎日期'
    如有需要，請依據實際情況調整此解析邏輯。
    """
    results = []
    
    # 依據實際回傳的 JSON 結構做調整，本範例假設資料位於 "Data" -> "LotteryResult" -> "List"
    draws = json_data.get("content", {}).get("superLotto638Res"if seqNo == "638" else"lotto649Res", [])

    if not draws:
        # 若找不到上述層級，嘗試查看最外層清單
        draws = json_data.get("content", [])
    
    for draw in draws:
        period = draw.get("period")
        winning_numbers = draw.get("drawNumberSize")
        draw_date =  draw.get("lotteryDate")
        results.append({
            "period": period,
            "winning_numbers": winning_numbers[0:6],
            "special_number": winning_numbers[-1],
            "draw_date":dt.fromisoformat(draw_date).strftime('%Y-%m-%d')
        })
    return results

def fetch_history_data(period_range,seqNo):
    """
    根據使用者輸入的時間範圍（半年、一年、二年），計算起始日期與結束日期，
    並依月份呼叫 API 取得大樂透歷史資料，僅保留期號、開獎號碼與開獎日期。
    """
    period_options = {"半年": 6, "一年": 12, "二年": 24}
    if period_range not in period_options:
        raise ValueError("請輸入有效的時間範圍：半年、一年、二年")
    
    months_range = period_options[period_range]
    # 結束月份以目前月份為準
    end_date = datetime.datetime.now().replace(day=1)
    # 起始日期即為結束月份往前推相應月份數
    start_date = end_date - relativedelta(months=months_range - 1)  # 包含結束月
    
    all_results = []
    current_date = start_date
    while current_date <= end_date:
        year = current_date.year
        month = current_date.month
        json_data = fetch_superlotto_data(year, month,seqNo)
        if json_data:
            draws_info = process_superlotto_json(json_data,seqNo)
            if draws_info:
                all_results.extend(draws_info)
            else:
                print(f"{year}-{month:02} 無開獎資料。")
        current_date += relativedelta(months=1)
        time.sleep(0.2)  # 避免過於頻繁請求
    return all_results

if __name__ == "__main__":
    # 請使用者輸入欲取得的歷史時段（半年、一年、二年）
    user_input = input("請輸入欲抓取的歷史時段（半年、一年、二年）：").strip()
    seqNo=input("請輸入要查詢的類型：").strip()
    try:
        history_data = fetch_history_data(user_input,seqNo)
        print("\n抓取結果：\n")
        print(history_data)
        for draw in history_data:
            print(f"期號：{draw['period']} | 開獎號碼：{draw['winning_numbers']} |特別號:{draw['special_number']}| 開獎日期：{draw['draw_date']}")
            print()  # 空行分隔月份資料
    except Exception as e:
        print("發生錯誤：", e)
