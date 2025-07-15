
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import asyncio
import re
import threading

BOT_TOKEN = "7777252416:AAGG07twWDJjfFvldXqxaxrJmAFXa0yQAbA"  # Replace with your bot token
LOG_CHANNEL_ID = -1002391366258     # Replace with your channel ID

response_dict = {}

app_flask = Flask(__name__)

@app_flask.route('/')
def home():
    return "Raj One Bot is running!"

async def fetch_channel_data(app):
    global response_dict
    response_dict.clear()
    messages = await app.bot.get_chat_history(chat_id=LOG_CHANNEL_ID, limit=100)
    for msg in messages:
        if msg.text and "=" in msg.text:
            parts = msg.text.split("=", 1)
            trigger = parts[0].strip().lower()
            reply = parts[1].strip()
            response_dict[trigger] = reply

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower().strip()
    for trigger, reply in response_dict.items():
        if re.fullmatch(trigger, text):
            await update.message.reply_text(reply)
            return

tg_app = ApplicationBuilder().token(BOT_TOKEN).build()
tg_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

async def startup(app):
    await fetch_channel_data(app)
    print("✅ Raj One Bot data loaded from log channel!")

tg_app.post_init = startup

def run_telegram():
    tg_app.run_polling()

def run_flask():
    app_flask.run(host="0.0.0.0", port=8080)

# Run both Flask and Telegram bot in parallel threads
if __name__ == "__main__":
    threading.Thread(target=lambda: asyncio.run(run_telegram())).start()
    run_flask()
