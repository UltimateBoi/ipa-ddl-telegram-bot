import os
import re
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import threading
from flask import Flask as _Flask


# Extracts App ID and builds the direct IPA download link
def generate_download_link(app_store_url: str) -> str:
    match = re.search(r'id(\d+)', app_store_url)
    if not match:
        return "❌ Invalid App Store link. Please make sure it includes an App ID."
    app_id = match.group(1)
    return f"http://c491z582.pushrcdn.com/strg/{app_id[0]}/{app_id}.ipa"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    link = generate_download_link(update.message.text.strip())
    await update.message.reply_text(link)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📲 Send an App Store link…")

flask_app = _Flask(__name__)
@flask_app.route('/')
def home():
    return "Bot is alive"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    flask_app.run(host="0.0.0.0", port=port)

# start Flask in background so it binds the Render port immediately
threading.Thread(target=run_flask, daemon=True).start()

if __name__ == "__main__":
    telegram_app = ApplicationBuilder().token(os.environ['BOT_TOKEN']).build()
    telegram_app.add_handler(CommandHandler("start", start))
    telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot is running…")
    telegram_app.run_polling(drop_pending_updates=True, close_loop=False)