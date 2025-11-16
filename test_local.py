import os
from dotenv import load_dotenv
import requests
from pymongo import MongoClient
import certifi
from openai import OpenAI

# Load ENV
load_dotenv()

# ===== ENV =====
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
MONGO_URI = os.getenv("MONGODB_URI")

# ===== 1. TEST ENV =====
print("===== KIỂM TRA ENV =====")
print("BOT_TOKEN:", "OK" if BOT_TOKEN else "❌ MISSING")
print("CHAT_ID:", "OK" if CHAT_ID else "❌ MISSING")
print("OPENAI_KEY:", "OK" if OPENAI_KEY else "❌ MISSING")
print("MONGO_URI:", "OK" if MONGO_URI else "❌ MISSING")
print()


# ===== 2. TEST TELEGRAM =====
def test_telegram():
    print("===== TEST TELEGRAM =====")
    
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": "✅ *Test thành công!* Bot đang online.",
        "parse_mode": "Markdown"
    }

    res = requests.post(url, json=data)

    if res.status_code == 200:
        print("📩 Gửi Telegram: OK")
    else:
        print("❌ Gửi Telegram lỗi:", res.text)


# ===== 3. TEST MONGODB =====
def test_mongo():
    print("\n===== TEST MONGODB =====")
    try:
        client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
        db = client["lifeup-legend"]
        print("🗄️ MongoDB version:", client.server_info()["version"])
        print("📁 Database:", db.name)

        # test đọc collection
        names = db.list_collection_names()
        print("📚 Collections:", names)

        print("🔗 MongoDB: OK")
    except Exception as e:
        print("❌ MongoDB lỗi:", e)


# ===== 4. TEST OPENAI GPT =====
def test_openai():
    print("\n===== TEST OPENAI =====")
    try:
        client = OpenAI(api_key=OPENAI_KEY)

        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "Say hello!"}]
        )

        print("🤖 GPT trả lời:", res.choices[0].message.content)
        print("🔗 OpenAI: OK")

    except Exception as e:
        print("❌ OpenAI lỗi:", e)


# ===== RUN ALL TEST =====
if __name__ == "__main__":
    print("🚀 Đang chạy test_local.py...\n")
    
    test_telegram()
    test_mongo()
    test_openai()

    print("\n🎉 Hoàn tất! Nếu cả 3 đều OK → bot sẵn sàng deploy.")
