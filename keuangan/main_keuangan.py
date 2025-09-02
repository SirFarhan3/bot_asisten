from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler, CommandHandler
from global_action.cancel import get_cancel_handler

from keuangan.pemasukan import init_pemasukan
from keuangan.pengeluaran import init_pengeluaran
from keuangan.summary import init_transaksi_today

# State untuk ConversationHandler
MAIN_MENU, PEMASUKAN, PENGELUARAN = range(3)

def init_keuangan(sheet):
    # Entry point ConversationHandler
    async def main_keuangan(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            "Halo Tn.Farhan! Apa yang bisa dibantu?\n"
            "Gunakan /pemasukan untuk mencatat pemasukan.\n"
            "Gunakan /pengeluaran untuk mencatat pengeluaran.\n"
            "Gunakan /transaksi_hari_ini untuk melihat transaksi hari ini.\n"
            "Gunakan /cancel untuk membatalkan."
        )
        return MAIN_MENU

    # ConversationHandler utama
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("keuangan", main_keuangan)],
        states={
            MAIN_MENU: [
                init_pemasukan(sheet),
                init_pengeluaran(sheet),
                init_transaksi_today(sheet, "today"),
            ]
        },
        fallbacks=[get_cancel_handler()]
    )

    return conv_handler
