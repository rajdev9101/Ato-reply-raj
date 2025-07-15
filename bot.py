from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
import asyncio
import threading
import re

BOT_TOKEN = "7777252416:AAGG07twWDJjfFvldXqxaxrJmAFXa0yQAbA"
LOG_CHANNEL_ID = -1002391366258

flask_app = Flask(__name__)
response_dict = {}

@flask_app.route('/')
def home():
    return "✅ Raj One Bot is Live!"

async def fetch_channel_data(application):
    global response_dict
    response_dict.clear()
    async for msg in application.bot.get_chat_history(LOG_CHANNEL_ID, limit=100):
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

async def run_bot():
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    await fetch_channel_data(application)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🤖 Raj One Bot is Running...")
    await application.run_polling()

def run_flask():
    flask_app.run(host="0.0.0.0", port=8080)

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    asyncio.run(run_bot())
