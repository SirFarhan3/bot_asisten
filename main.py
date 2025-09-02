import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
from dotenv import load_dotenv
import gspread
from google.oauth2.service_account import Credentials

from keuangan.pemasukan import init_pemasukan
from keuangan.pengeluaran import init_pengeluaran
from keuangan.main_keuangan import init_keuangan
from keuangan.summary import init_transaksi_today
from global_action.cancel import get_cancel_handler

load_dotenv()

# ----- Google Sheets Setup -----
SHEET_FILE = "credentials.json"
SHEET_ID = os.getenv("SHEET_ID")

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive",
]
creds = Credentials.from_service_account_file(SHEET_FILE, scopes=scope)
client = gspread.authorize(creds)
sheet = client.open_by_key(SHEET_ID).sheet1

# ----- Telegram Bot Token -----
TOKEN = os.getenv("TELEGRAM_TOKEN")

# ----- Keywords -----
with open("keywords.txt", "r") as f:
    kata_targets = [line.strip().lower() for line in f if line.strip()]


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # Command /start
    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            "Halo! Selamat datang Tn.Farhan, ada yang bisa saya bantu?\n"
            "Gunakan /keuangan untuk masuk dalam menu keuangan.\n"
            "Gunakan /cancel untuk membatalkan operasi."
        )

    app.add_handler(CommandHandler("start", start))

    # Handler lain
    app.add_handler(init_pengeluaran(sheet))
    app.add_handler(init_pemasukan(sheet))
    app.add_handler(init_keuangan(sheet))
    app.add_handler(init_transaksi_today(sheet))
    app.add_handler(get_cancel_handler())

    async def handle_keyword(update: Update, context: ContextTypes.DEFAULT_TYPE):
        text = update.message.text.lower()
        kata_ditemukan = [kata for kata in kata_targets if kata in text]

        if not kata_ditemukan:
            print("Tidak ada kata target di kalimat")
            return

        kata_kunci = kata_ditemukan[0]
        print("Kata Kunci:", kata_kunci)

        if kata_kunci == "pengeluaran":
            await init_pengeluaran(sheet).entry_points[0].callback(update, context)
        elif kata_kunci == "pemasukan":
            await init_pemasukan(sheet).entry_points[0].callback(update, context)
        elif kata_kunci == "catatan hari ini":
            await init_transaksi_today(sheet, "today").entry_points[0].callback(update, context)
        elif kata_kunci == "catatan bulan ini":
            await init_transaksi_today(sheet, "month").entry_points[0].callback(update, context)
        elif kata_kunci == "catatan tahun ini":
            await init_transaksi_today(sheet, "year").entry_points[0].callback(update, context)
        else:
            print("Command tidak dikenal")

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_keyword))

    print("Bot berjalan...")
    app.run_polling()   # <- langsung sync, tanpa asyncio.run()


if __name__ == "__main__":
    main()
