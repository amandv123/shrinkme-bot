import telebot
import requests
import re
import time
import os

# =========================

# TOKENS

# =========================

BOT_TOKEN = os.getenv("BOT_TOKEN")
SHRINKME_TOKEN = os.getenv("SHRINKME_TOKEN")

# =========================

# BOT SETUP

# =========================

bot = telebot.TeleBot(BOT_TOKEN)

# URL REGEX

URL_PATTERN = r"(https?://[^\s]+)"

# =========================

# SHORTEN FUNCTION

# =========================

def shorten_url(url):

```
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
```

# =========================

# START COMMAND

# =========================

@bot.message_handler(commands=['start'])
def start_message(message):

```
welcome_text = (
    "🤖 Professional Smart Shortener Bot\n\n"
    "✅ Multiple links supported\n"
    "✅ Original formatting preserved\n"
    "✅ Smart URL replacement\n\n"
    "🚀 Powered by ShrinkMe"
)

bot.reply_to(message, welcome_text)
```

# =========================

# MAIN MESSAGE HANDLER

# =========================

@bot.message_handler(func=lambda message: True)
def handle_message(message):

```
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

    updated_text = updated_text.replace(
        url,
        short_url
    )

user_name = message.from_user.first_name

print(
    f"[USER] {user_name} shortened {success_count} links"
)

bot.reply_to(
    message,
    updated_text
)
```

# =========================

# START BOT

# =========================

print("🤖 Professional Smart Bot Running On Render...")

while True:

```
try:

    bot.infinity_polling(
        timeout=30,
        long_polling_timeout=30
    )

except Exception as e:

    print("Restarting polling...", e)

    time.sleep(5)
```
