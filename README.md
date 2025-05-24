
[![Built with](https://img.shields.io/badge/Built%20with-Stima%20API-blueviolet?logo=robot)](https://api.stima.tech)
# 彩券預測 LINE Bot

這是一個透過LINE平台提供彩券預測服務的聊天機器人，使用AI模型分析歷史開獎資料，為用戶提供可能的中獎號碼預測。

## 功能特色

- 支援大樂透和威力彩兩種彩券類型預測
- 可選擇半年、一年或二年的歷史資料進行分析
- 使用Groq API進行AI模型預測
- 提供預測號碼、特別號及中獎機率分析
- 透過LINE平台方便使用者隨時查詢

## 技術架構

- **後端框架**：Flask 2.3.2
- **LINE Bot SDK**：line-bot-sdk 3.14.2
- **AI模型整合**：Groq API (透過OpenAI兼容接口)
- **資料處理**：Python-dateutil, Requests
- **部署平台**：Vercel


## 使用方式

1. 在LINE上加入此機器人為好友
2. 傳送「預測樂透」開始預測流程
3. 選擇想要預測的彩券類型（大樂透或威力彩）
4. 選擇要分析的歷史資料範圍（半年、一年或二年）
5. 等待系統分析並回傳預測結果

## 開發設定

### 環境變數

需要設定以下環境變數：
- `LINE_CHANNEL_ACCESS_TOKEN`：LINE Bot的存取令牌
- `LINE_CHANNEL_SECRET`：LINE Bot的頻道密鑰
- `GROQ_API_KEY`：Groq API金鑰
- `GROQ_API_BASE_URL`：Groq API基礎URL
- `GROQ_BASE_URL`：Groq API完整URL

### 本地開發

1. 克隆此專案
2. 安裝相依套件：
3. 設定環境變數
4. 使用ngrok等工具提供外部URL以接收LINE的Webhook

### 部署到Vercel

1. Fork此專案
2. 在Vercel上設定環境變數
3. 部署專案
4. 將LINE Bot的Webhook URL設定為`https://您的域名/callback`

## 授權資訊

本專案採用MIT授權條款。

## 聯絡方式

如有任何問題或建議，請透過GitHub Issues聯絡我們。
