
_id_counter = {}


def generate_id(prefix="ID"):
  
    if prefix not in _id_counter:
        _id_counter[prefix] = 1
    nomor = str(_id_counter[prefix]).zfill(3)
    _id_counter[prefix] += 1
    return f"{prefix}-{nomor}"


def format_rupiah(angka):
    """
    Format angka jadi string rupiah.
    Contoh: 75000 -> 'Rp 75.000'
    """
    return f"Rp {angka:,.0f}".replace(",", ".")


def cetak_garis(karakter="=", panjang=45):
    """Cetak garis pemisah di CLI."""
    print(karakter * panjang)


def cetak_header(judul):
    """Cetak header dengan garis atas dan bawah."""
    cetak_garis()
    print(f"  {judul.upper()}")
    cetak_garis()