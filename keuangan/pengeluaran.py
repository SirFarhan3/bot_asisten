from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler, CommandHandler, MessageHandler, filters
from datetime import datetime
from global_action.cancel import get_cancel_handler
from keuangan.data_pengeluaran import get_total_pengeluaran
from middleware.format_rupiah import format_rupiah

PENGELUARAN = 0

def init_pengeluaran(sheet):
    async def pengeluaran(update, context):
        await update.message.reply_text(
            "Masukkan pengeluaran hari ini (Format: Nominal Aktivitas)\n"
            "Contoh: 50000 Pembelian buku\n\n"
            "Untuk membatalkan /cancel"
        )
        return PENGELUARAN

    async def simpan_pengeluaran(update, context):
        try:
            text = update.message.text.strip()
            parts = text.split(" ", 1)
            if len(parts) < 2:
                await update.message.reply_text(
                    "Format salah! Gunakan format: Nominal Aktivitas\nContoh: 50000 Pembelian buku"
                )
                return PENGELUARAN
            message = ""
            jumlah_str, aktivitas = parts
            jumlah = int(jumlah_str)
            tanggal = datetime.now().strftime("%d-%m-%Y")
            sheet.append_row([tanggal, jumlah, "Pengeluaran", aktivitas.capitalize()])
            
            # --- START: Kode untuk mengambil dan menjumlahkan data ---
            total_sum = 0
            total_sum = get_total_pengeluaran(sheet, "today")

            if total_sum >= 50000:
                message = "🟥🟥🟥"
            elif total_sum >= 40000:
                message = "🟨🟨🟨"
            else:
                message = "🟩🟩🟩"

            await update.message.reply_text(
                f"✅ Pengeluaran berhasil dicatat!\n\n"
                f"📅 Tanggal: {tanggal}\n"
                f"💰 Nominal: {format_rupiah(jumlah)}\n"
                f"📝 Aktivitas: {aktivitas.capitalize()}\n\n"
                f"Total pengeluaran saat ini: {format_rupiah(total_sum)}\n\n"
                f"{message}"
            )
            return ConversationHandler.END
        except ValueError:
            await update.message.reply_text("Nominal harus berupa angka. Silakan coba lagi.")
            return PENGELUARAN

    return ConversationHandler(
        entry_points=[
            CommandHandler("pengeluaran", pengeluaran),
            MessageHandler(filters.TEXT & ~filters.COMMAND & filters.Regex(r"(?i)pengeluaran"), pengeluaran)
        ],
        states={PENGELUARAN: [MessageHandler(filters.TEXT & ~filters.COMMAND, simpan_pengeluaran)]},
        fallbacks=[get_cancel_handler()]
    )
