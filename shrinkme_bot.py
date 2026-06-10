import telebot
import requests
import re
import json
import os

BOT_TOKEN = "8230266389:AAGFZpNvHoQwurRoMU3BbH3CXV1hIUv2cwo"

bot = telebot.TeleBot(BOT_TOKEN)

URL_PATTERN = r"(https?://[^\s]+)"

DB_FILE = "users.json"


# Load users
def load_users():

    if not os.path.exists(DB_FILE):
        return {}

    with open(DB_FILE, "r") as f:
        return json.load(f)


# Save users
def save_users(data):

    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)


# Shorten URL
def shorten_url(api_token, url):

    api_url = "https://shrinkme.io/api"

    params = {
        "api": api_token,
        "url": url
    }

    try:

        response = requests.get(
            api_url,
            params=params,
            timeout=20
        )

        data = response.json()

        if data.get("status") == "success":
            return data.get("shortenedUrl")

        return None

    except Exception as e:

        print(f"[ERROR] {e}")

        return None


# Start command
@bot.message_handler(commands=['start'])
def start(message):

    welcome_text = (
        "🤖 Professional Multi User Shortener Bot\n\n"
        "📌 First setup your API token.\n\n"
        "Use command:\n"
        "/setapi"
    )

    bot.reply_to(message, welcome_text)


# Set API Command
@bot.message_handler(commands=['setapi'])
def set_api(message):

    msg = bot.reply_to(
        message,
        "🔑 Send your ShrinkMe API Token"
    )

    bot.register_next_step_handler(
        msg,
        save_api_token
    )


# Save API Token
def save_api_token(message):

    user_id = str(message.from_user.id)

    api_token = message.text.strip()

    users = load_users()

    users[user_id] = {
        "api_token": api_token
    }

    save_users(users)

    bot.reply_to(
        message,
        "✅ API Token Saved Successfully!\n\nNow send any links."
    )


# Handle Messages
@bot.message_handler(func=lambda message: True)
def handle_message(message):

    user_id = str(message.from_user.id)

    users = load_users()

    if user_id not in users:

        bot.reply_to(
            message,
            "❌ First set your API token.\nUse /setapi"
        )

        return

    api_token = users[user_id]["api_token"]

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

        short_url = shorten_url(api_token, url)

        if short_url:

            success_count += 1

            updated_text = updated_text.replace(
                url,
                short_url
            )

    print(
        f"[USER] {message.from_user.first_name} shortened {success_count} links"
    )

    bot.reply_to(
        message,
        updated_text
    )


print("🤖 Professional Multi User Bot Running...")

bot.infinity_polling()
