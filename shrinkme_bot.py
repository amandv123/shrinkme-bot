import telebot
import requests
import re
import time

# =========================
# TOKENS
# =========================

BOT_TOKEN = "8230266389:AAGXiAaVakXuiPqrAuN1oCinFYYqaN92KPk"
SHRINKME_TOKEN = "9391bc42128173732b1f34a6e69615d5425e2507"

# =========================
# BOT SETUP
# =========================

bot = telebot.TeleBot(BOT_TOKEN)

URL_PATTERN = r"(https?://[^\s]+)"

# =========================
# SHORTENER FUNCTION
# =========================

def shorten_url(url):

    try:

        api_url = (
            f"https://shrinkme.io/api"
            f"?api={SHRINKME_TOKEN}"
            f"&url={url}"
            f"&format=text"
        )

        response = requests.get(
            api_url,
            timeout=20
        )

        short_url = response.text.strip()

        if short_url.startswith("http"):
            return short_url

        return url

    except Exception as e:

        print(f"[ERROR] {e}")

        return url

# =========================
# START COMMAND
# =========================

@bot.message_handler(commands=['start'])
def start_message(message):

    welcome_text = (
        "🤖 Professional Smart Shortener Bot\n\n"
        "✅ Multiple links supported\n"
        "✅ Original formatting preserved\n"
        "✅ Smart URL replacement\n\n"
        "🚀 Powered by ShrinkMe"
    )

    bot.reply_to(message, welcome_text)

# =========================
# MAIN MESSAGE HANDLER
# =========================

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

# =========================
# START BOT
# =========================

print("🤖 Professional Smart Bot Running...")

while True:

    try:

        bot.infinity_polling(
            timeout=30,
            long_polling_timeout=30
        )

    except Exception as e:

        print(f"[ERROR] {e}")

        time.sleep(5)
