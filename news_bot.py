import feedparser
import requests
import os
from datetime import datetime
from openai import OpenAI

# =========================
# CONFIG
# =========================
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK")

client = OpenAI(api_key=OPENAI_API_KEY)

# =========================
# 1. ดึงข่าว
# =========================
def get_news():
    url = "https://news.google.com/rss/search?q=AI"
    feed = feedparser.parse(url)
    return feed.entries[:5]

# =========================
# 2. สรุปข่าวด้วย AI
# =========================
def summarize(text):
    try:
        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": f"สรุปข่าวนี้เป็นภาษาไทย 2-3 บรรทัด:\n{text}"}
            ]
        )
        return res.choices[0].message.content.strip()
    except Exception as e:
        return f"(สรุปไม่ได้: {e})"

# =========================
# 3. สร้างข้อความ
# =========================
def build_message(articles):
    today = datetime.now().strftime("%d/%m/%Y")
    msg = f"🧠 **AI News ({today})**\n\n"

    for i, a in enumerate(articles, 1):
        summary = summarize(a.title)
        msg += f"**{i}. {a.title}**\n"
        msg += f"{summary}\n"
        msg += f"{a.link}\n\n"

    return msg

# =========================
# 4. ส่งเข้า Discord
# =========================
def send_discord(message):
    data = {
        "content": message
    }
    res = requests.post(DISCORD_WEBHOOK, json=data)
    print("Discord status:", res.status_code)

# =========================
# 5. บันทึกไฟล์
# =========================
def save_file(content):
    with open("news.txt", "w", encoding="utf-8") as f:
        f.write(content)

# =========================
# MAIN
# =========================
def main():
    articles = get_news()
    message = build_message(articles)

    save_file(message)
    send_discord(message)

if __name__ == "__main__":
    main()



def send_discord(message):
    print("Sending to Discord...")
    print("Webhook:", DISCORD_WEBHOOK)

    data = {"content": message}

    res = requests.post(DISCORD_WEBHOOK, json=data)

    print("Status:", res.status_code)
    print("Response:", res.text)
