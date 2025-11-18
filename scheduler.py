import os
import json
import random
import requests
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI
from pymongo import MongoClient
import certifi
import random


# Load ENV
load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
MONGO_URI = os.getenv("MONGODB_URI")

# Kết nối MongoDB
client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
db = client["lifeup-legend"]
tasks = db["tasks"]

openai_client = OpenAI(api_key=OPENAI_KEY)

TG_SEND_MESSAGE = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

# Random ra một nhiệm vụ để làm

choice = random.choice(["lập trình", "tiếng anh", "tiếng trung"])



# ---------------------------
# 1. Tạo nhiệm vụ bằng GPT
# ---------------------------
def generate_daily_task():
    prompt = f"""
    Hãy tạo nhiệm vụ học "{choice}" hôm nay.
    Trả về dạng JSON:
    {{
        "name": "",
        "short_desc": "",
        "full_desc": "",
        "requirement": "",
        "reward": "",
        "penalty": "",
        "deadline": ""
    }}
    """
    res = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ],
        response_format={"type": "json_object"}
    )
    return res.choices[0].message.content


# ---------------------------
# 2. Lưu vào database
# ---------------------------
def save_task(task):
    task_data = json.loads(task)

    item = {
        "name": task_data["name"],
        "type": "Hàng ngày",
        "short_desc": task_data["short_desc"],
        "full_desc": task_data["full_desc"],
        "requirement": task_data["requirement"],
        "reward": task_data["reward"],
        "penalty": task_data["penalty"],
        "deadline": task_data["deadline"],
        "date": datetime.now().strftime("%Y-%m-%d"),
        "status": "chưa hoàn thành",
        "difficulty": random.choice(["Dễ", "Trung bình", "Khó"])
    }

    tasks.insert_one(item)
    return item


# ---------------------------
# 3. Gửi Telegram
# ---------------------------
def send_to_telegram(task):
    msg = (
        f"🧭 <b>Tên nhiệm vụ:</b> {task['name']}\n"
        f"📘 <b>Xếp loại:</b> Hàng ngày\n"
        f"📝 <b>Mô tả:</b> {task['short_desc']}\n"
        f"⏰ <b>Hạn:</b> {task['deadline']}\n"
        f"🔗 <b>Xem chi tiết:</b> https://www.lifeuplegend.com/tasks"
    )

    requests.post(TG_SEND_MESSAGE, json={
        "chat_id": CHAT_ID,
        "text": msg,
        "parse_mode": "HTML"
    })


# ---------------------------
# 4. Chạy toàn bộ workflow
# ---------------------------
def main():
    print("🚀 Đang tạo nhiệm vụ hằng ngày...")

    raw = generate_daily_task()
    task = save_task(raw)
    send_to_telegram(task)

    print("✅ Đã gửi nhiệm vụ xong!")


if __name__ == "__main__":
    main()
