import datetime
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, MessageHandler, filters, ConversationHandler
from global_action.cancel import get_cancel_handler
from middleware.format_rupiah import format_rupiah

def init_transaksi_today(sheet, category="today"):

    async def transaksi_hari_ini(update: Update, context: ContextTypes.DEFAULT_TYPE):
        all_data = sheet.get_all_records()
        if not all_data:
            await update.message.reply_text("Belum ada catatan.")
            return ConversationHandler.END
        
        today = datetime.datetime.now()

        data_transaksi = []
        for row in all_data:
            try:
                # parse tanggal dari sheet (misal format "dd-mm-YYYY")
                tgl = datetime.datetime.strptime(row["Tanggal"], "%d-%m-%Y")
            except Exception:
                continue  # skip kalau format salah

            if category == "year" and tgl.year == today.year:
                data_transaksi.append(row)
            elif category == "month" and (tgl.year == today.year and tgl.month == today.month):
                data_transaksi.append(row)
            elif category == "today" and tgl.date() == today.date():
                data_transaksi.append(row)

        if not data_transaksi:
            await update.message.reply_text("Belum ada catatan transaksi.")
            return ConversationHandler.END

        pesan = f"📊 Catatan Keuangan ({category}):\n"
        for row in data_transaksi:
            pesan += f"{row['Tanggal']} | {format_rupiah(row['Jumlah'])} | {row['Tipe']} | {row['Aktivitas']}\n"

        await update.message.reply_text(pesan)
        return ConversationHandler.END

    return ConversationHandler(
        entry_points=[
            CommandHandler("transaksi_hari_ini", transaksi_hari_ini),
            MessageHandler(filters.Regex(r"(?i)transaksi hari ini"), transaksi_hari_ini)
        ],
        states={},
        fallbacks=[get_cancel_handler()]
    )
