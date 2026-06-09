import telebot
import requests
import re
import time
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
SHRINKME_TOKEN = os.getenv("SHRINKME_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

URL regex

URL_PATTERN = r"(https?://[^\s]+)"

def shorten_url(url):
api_url = "https://shrinkme.io/api"

params = {
    "api": SHRINKME_TOKEN,
    "url": url
}

headers = {
    "User-Agent": "Mozilla/5.0"
}

try:
    response = requests.get(
        api_url,
        params=params,
        headers=headers,
        timeout=20
    )

    data = response.json()

    if data.get("status") == "success":
        return data.get("shortenedUrl")

    return url

except Exception as e:
    print(f"[ERROR] {e}")
    return url

@bot.message_handler(func=lambda message: True)
def handle_message(message):
text = message.text

urls = re.findall(URL_PATTERN, text)

if not urls:
    bot.reply_to(
        message,
        "❌ No valid links found."
    )
    return

updated_text = text

success_count = 0

for url in urls:
    short_url = shorten_url(url)

    if short_url != url:
        success_count += 1

    updated_text = updated_text.replace(url, short_url)

print(f"[USER] shortened {success_count} links")

bot.reply_to(message, updated_text)

print("🤖 Professional Smart Bot Running...")

while True:
try:
bot.infinity_polling(
timeout=30,
long_polling_timeout=30
)

except Exception as e:
    print("Restarting polling...", e)
    time.sleep(5)
