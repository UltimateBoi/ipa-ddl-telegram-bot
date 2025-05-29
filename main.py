import os
import re
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Extracts App ID and builds the direct IPA download link
def generate_download_link(app_store_url: str) -> str:
    match = re.search(r'id(\d+)', app_store_url)
    if not match:
        return "❌ Invalid App Store link. Please make sure it includes an App ID."
    app_id = match.group(1)
    folder_prefix = app_id[0]
    return f"http://c491z582.pushrcdn.com/strg/{folder_prefix}/{app_id}.ipa"

# Handles regular messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text.strip()
    link = generate_download_link(user_input)
    await update.message.reply_text(link)

# Handles /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📲 Send an App Store link, and I’ll give you the direct download link!")

if __name__ == "__main__":
    telegram_app = ApplicationBuilder().token(os.environ['BOT_TOKEN']).build()

    telegram_app.add_handler(CommandHandler("start", start))
    telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot is running...")
    telegram_app.run_polling(drop_pending_updates=True, close_loop=False)

# To keep bot up 24/7
from flask import Flask as _Flask
import threading

flask_app = _Flask(__name__)

@flask_app.route('/')
def home():
    return "Bot is alive"

def run_flask():
    flask_app.run(host="0.0.0.0", port=10000)

# start Flask in its own daemon thread
threading.Thread(target=run_flask, daemon=True).start()