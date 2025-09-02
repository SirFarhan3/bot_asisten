from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler, CommandHandler, MessageHandler, filters
from datetime import datetime
from global_action.cancel import get_cancel_handler
from middleware.format_rupiah import format_rupiah

PEMASUKAN = 0

def init_pemasukan(sheet):
    async def pemasukan(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            "Masukkan pemasukan hari ini (Format: Nominal Aktivitas)\n"
            "Contoh: 50000 Penjualan buku\n\n"
            "Untuk membatalkan /cancel"
        )
        return PEMASUKAN

    async def simpan_pemasukan(update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            text = update.message.text.strip()
            parts = text.split(" ", 1)
            if len(parts) < 2:
                await update.message.reply_text(
                    "Format salah! Gunakan format: Nominal Aktivitas\nContoh: 50000 Penjualan buku"
                )
                return PEMASUKAN

            jumlah_str, aktivitas = parts
            jumlah = int(jumlah_str)
            tanggal = datetime.now().strftime("%d-%m-%Y")
            sheet.append_row([tanggal, jumlah, "Pemasukan", aktivitas.capitalize()])
            await update.message.reply_text(
                f"✅ Pemasukan berhasil dicatat!\n\n"
                f"📅Tanggal: {tanggal}\n💰"
                f"Nominal: {format_rupiah(jumlah)}\n📝"
                f"Aktivitas: {aktivitas.capitalize()}"
            )
            return ConversationHandler.END
        except ValueError:
            await update.message.reply_text("Nominal harus berupa angka. Silakan coba lagi.")
            return PEMASUKAN

    return ConversationHandler(
        entry_points=[
            CommandHandler("pemasukan", pemasukan),
            MessageHandler(filters.TEXT & ~filters.COMMAND & filters.Regex(r"(?i)pemasukan"), pemasukan)
        ],
        states={PEMASUKAN: [MessageHandler(filters.TEXT & ~filters.COMMAND, simpan_pemasukan)]},
        fallbacks=[get_cancel_handler()]
    )
