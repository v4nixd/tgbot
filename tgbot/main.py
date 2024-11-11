import logging
import asyncio
import os

from qrgen import qrgenerator

from dotenv import load_dotenv, dotenv_values

from telegram import Update, ForceReply
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler

config = dotenv_values(".env")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

async def start(update: Update, _: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True)
    )

async def qrcode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = " ".join(update.message.text.split(" ")[1:])
    qr = qrgenerator.generate(msg)
    await update.message.reply_photo(
        photo=qr,
        caption=f"Вот ваш куаркод с следующим содержанием: {msg}"
    )

def main():
    application = Application.builder().token(config["API_TOKEN"]).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("qrcode", qrcode))

    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__=="__main__":
    main()