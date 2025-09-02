import gspread
import re
from datetime import datetime

def get_total_pengeluaran(sheet: gspread.worksheet.Worksheet, mode="today"):
    """
    mode: "day", "month", atau "year"
    """
    try:
        data = sheet.get_all_values()
        total_pengeluaran_sum = 0

        # tanggal sekarang
        today = datetime.now()

        for row in data[1:]:  # skip header
            if len(row) > 2 and row[0].strip() and row[1].strip() and row[2].strip():
                try:
                    tanggal = datetime.strptime(row[0].strip(), "%d-%m-%Y")
                except ValueError:
                    continue  # kalau format salah, skip

                tipe = row[2].strip().lower()

                # cek sesuai mode
                if tipe == "pengeluaran":
                    match = False
                    if mode == "today":
                        match = tanggal.date() == today.date()
                    elif mode == "month":
                        match = (tanggal.month == today.month and tanggal.year == today.year)
                    elif mode == "year":
                        match = tanggal.year == today.year

                    if match:
                        try:
                            # hapus karakter non angka
                            amount_str_cleaned = re.sub(r'[^\d]', '', row[1].strip())
                            amount = float(amount_str_cleaned)
                            total_pengeluaran_sum += amount
                        except ValueError:
                            continue

        return int(total_pengeluaran_sum)

    except Exception as e:
        print(f"Error saat mengambil data dari sheet: {e}")
        return 0
