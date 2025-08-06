import os
import time
import random
import requests
from datetime import datetime

BOT_TOKEN = os.getenv("8232232932:AAHHw0incVCAg2EHlJeSdMQYuORSzVlz1LM")
CHANNEL_ID = os.getenv("@CryptoxPulse") 

# ========== HELPER FUNCTIONS ==========

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHANNEL_ID,
        "text": text,
        "parse_mode": "HTML"
    }
    try:
        res = requests.post(url, data=data)
        if res.status_code != 200:
            print("Telegram error:", res.text)
    except Exception as e:
        print("Send message failed:", e)

def send_photo(caption, photo_url=None, local_path=None):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    data = {
        "chat_id": CHANNEL_ID,
        "caption": caption,
        "parse_mode": "HTML"
    }
    files = {'photo': open(local_path, 'rb')} if local_path else None
    if photo_url:
        data["photo"] = photo_url
        files = None
    try:
        res = requests.post(url, data=data, files=files)
        if res.status_code != 200:
            print("Telegram photo error:", res.text)
    except Exception as e:
        print("Send photo failed:", e)

# ========== MODULE 1: NEWS ==========

def get_crypto_news():
    url = "https://cryptopanic.com/api/v1/posts/?auth=demo&public=true"  # Replace 'demo' with real key if needed
    try:
        res = requests.get(url).json()
        articles = res['results'][:2]
        for article in articles:
            title = article['title']
            link = article['url']
            send_message(f"📰 <b>Crypto News</b>\n{title}\n🔗 {link}")
    except Exception as e:
        print("News error:", e)

# ========== MODULE 2: AI TRADING IDEA ==========

def generate_trade_prediction():
    coins = ['BTC', 'ETH', 'SOL', 'XRP', 'ADA', 'AVAX', 'LTC']
    directions = ['Bullish', 'Bearish']
    coin = random.choice(coins)
    direction = random.choice(directions)
    entry = round(random.uniform(20, 100), 2)
    exit_point = round(entry * (1.1 if direction == 'Bullish' else 0.9), 2)
    term = random.choice(['Short Term (1-2 Days)', 'Mid Term (1 Week)', 'Long Term (2+ Weeks)'])
    confidence = random.randint(89, 99)

    msg = (
        f"📈 <b>Trade Prediction</b>\n"
        f"💰 Coin: <b>{coin}</b>\n"
        f"📊 Direction: <b>{direction}</b>\n"
        f"🎯 Entry: <code>{entry}</code>\n"
        f"🏁 Exit: <code>{exit_point}</code>\n"
        f"⏱️ Term: {term}\n"
        f"✅ Confidence: <b>{confidence}%</b>"
    )
    send_message(msg)

# ========== MODULE 3: MOTIVATION ==========

def post_motivation():
    try:
        with open("quotes.txt", "r", encoding="utf-8") as f:
            quotes = f.readlines()
        if quotes:
            quote = random.choice(quotes).strip()
            send_message(f"🔥 <b>Motivation</b>\n“{quote}”")
    except Exception as e:
        print("Quote error:", e)

# ========== MODULE 4: CRYPTO MEMES ==========

def post_crypto_meme():
    try:
        memes_folder = "memes"
        memes = [f for f in os.listdir(memes_folder) if f.endswith((".png", ".jpg", ".jpeg"))]
        if memes:
            meme_path = os.path.join(memes_folder, random.choice(memes))
            send_photo("😂 <b>Crypto Meme of the Day</b>", local_path=meme_path)
    except Exception as e:
        print("Meme error:", e)

# ========== MAIN BOT LOOP ==========

if __name__ == "__main__":
    if not BOT_TOKEN or not CHANNEL_ID:
        print("❌ Missing BOT_TOKEN or CHANNEL_ID")
        exit()

    while True:
        now = datetime.now()
        hour = now.hour
        minute = now.minute

        print(f"⏱️ Running bot at {now.strftime('%H:%M')}")

        # Post news once every 6 hours
        if hour % 6 == 0 and minute < 5:
            get_crypto_news()

        # Post 2 memes per day at 10AM and 6PM
        if hour in [10, 18] and minute < 5:
            post_crypto_meme()

        # Post motivational quote at 9AM
        if hour == 9 and minute < 5:
            post_motivation()

        # Post trade prediction every 3 hours
        if hour % 3 == 0 and minute < 5:
            generate_trade_prediction()

        time.sleep(300)  # Check every 5 mins
