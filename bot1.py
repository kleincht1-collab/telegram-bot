import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters, CallbackQueryHandler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = f"Hola {user.first_name or 'amigo'}! Soy tu bot."
    keyboard = [
        [InlineKeyboardButton("Saludar", callback_data="hi")],
        [InlineKeyboardButton("Info", callback_data="info")]
    ]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("/start - inicia\n/help - ayuda\n/echo texto")

async def echo_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        await update.message.reply_text(" ".join(context.args))
    else:
        await update.message.reply_text("Usa: /echo texto")

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("No entiendo ese comando.")

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    if q.data == "hi":
        await q.edit_message_text("¡Hola! 👋")
    elif q.data == "info":
        await q.edit_message_text("Bot corriendo en Railway.")

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("echo", echo_cmd))
    app.add_handler(CallbackQueryHandler(buttons))
    app.add_handler(MessageHandler(filters.COMMAND, unknown))
    logger.info("Bot ejecutándose…")
    app.run_polling()

if __name__ == "__main__":
    main()
