import locale

def format_rupiah(angka, with_prefix=True, desimal=0):
    # locale.setlocale(locale.LC_NUMERIC, 'id_ID.UTF-8')
    # rupiah = locale.format_string("%.*f", (desimal, angka), True)
    # if with_prefix:
    #     return "Rp.{}".format(rupiah)
    # return rupiah
    return f"Rp.{angka:,}".replace(",", ".")
