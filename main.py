import os
import time
import requests

BOT_TOKEN = os.getenv("8232232932:AAHHw0incVCAg2EHlJeSdMQYuORSzVlz1LM")
CHANNEL_ID = os.getenv("@CryptoxPulse")  

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHANNEL_ID,
        "text": text,
        "parse_mode": "HTML"
    }
    try:
        res = requests.post(url, data=payload)
        if res.status_code != 200:
            print("❌ Telegram error:", res.text)
    except Exception as e:
        print("⚠️ Send message failed:", e)

if not BOT_TOKEN or not CHANNEL_ID:
    print("⚠️ BOT_TOKEN or CHANNEL_ID is missing!")
    exit()

# 🕒 Send message every hour
while True:
    send_message("🚀 Bot is now LIVE and posting from Render every hour!")
    time.sleep(3600)  # 3600 seconds = 1 hour
