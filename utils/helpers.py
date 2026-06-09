import uuid


def generate_id(prefix="ID"):
    """
    Buat ID unik dengan format PREFIX-XXXXXXXX
    Contoh: PRD-A1B2C3D4, ORD-9F3E1A2B
    """
    kode_unik = uuid.uuid4().hex[:8].upper()
    return f"{prefix}-{kode_unik}"


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