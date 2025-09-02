from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler, CommandHandler

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Baik! Sampai jumpa lagi Tn.Farhan")
    return ConversationHandler.END

def get_cancel_handler():
    return CommandHandler("cancel", cancel)
