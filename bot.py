import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import requests

# 🔑 Replace this with your Bot Token
BOT_TOKEN = '7820388928:AAEEX2B-yvzIGuRx4uC4ud0Oljl_r8YfD6w'

# Flask backend URL
BASE_URL = 'http://127.0.0.1:5000/shorten'

logging.basicConfig(level=logging.INFO)

def start(update, context):
    update.message.reply_text("Send me any link and I'll shorten it for you 🔗")

def shorten_link(update, context):
    user_input = update.message.text
    if not user_input.startswith("http"):
        update.message.reply_text("❌ Please send a valid URL starting with http or https")
        return
    
    try:
        # Send POST to Flask backend
        response = requests.post(BASE_URL, data={'url': user_input})
        short_link = response.text
        update.message.reply_text(f"✅ Shortened Link:\n{short_link}")
    except Exception as e:
        update.message.reply_text("❌ Error shortening link")
        print("Error:", e)

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, shorten_link))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
