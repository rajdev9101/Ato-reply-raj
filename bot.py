# Auto-Reply Telegram Bot (50k+ Replies)
# Author: Rajdev (Professor)
# Bot Owner: @raj_dev_01
# Basic version using Pyrogram with FORCE SUBSCRIBE feature

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import random
import json

# Load 50k+ replies from a JSON file
with open("replies.json", "r", encoding="utf-8") as f:
    REPLY_DB = json.load(f)

API_ID = 27084955  # Replace with your API_ID
API_HASH = "91c88b554ab2a34f8b0c72228f06fc0b"
BOT_TOKEN = "your_bot_token_here"
FORCE_SUB_CHANNEL = "1005804953849"  # Replace with your channel username

bot = Client("professor_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Force Subscribe Checker
async def is_subscribed(user_id):
    try:
        member = await bot.get_chat_member(FORCE_SUB_CHANNEL, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

@bot.on_message(filters.private | filters.group)
async def auto_reply(client, message):
    user_id = message.from_user.id
    if not await is_subscribed(user_id):
        btn = InlineKeyboardMarkup([
            [InlineKeyboardButton("📢 Join Channel", url=f"https://t.me/{FORCE_SUB_CHANNEL.replace('@', '')}")]
        ])
        await message.reply_text("🚫 Please join our channel to use this bot!", reply_markup=btn)
        return

    text = message.text.lower()
    reply_found = False

    for keyword, replies in REPLY_DB.items():
        if keyword in text:
            await message.reply_text(random.choice(replies))
            reply_found = True
            break

    if not reply_found:
        default_replies = REPLY_DB.get("default", [
            "Hmm... 🤔", "Aur batao?", "Yeh toh interesting hai!", "Kya kehna chahte ho?"
        ])
        await message.reply_text(random.choice(default_replies))

bot.run()
