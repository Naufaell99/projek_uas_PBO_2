from services.marketplace import Marketplace
from utils.data_manager import simpan_semua, muat_semua
from services.auth_service import AuthService
from services.order_service import OrderService
from models.admin import Admin
from models.customer import Customer
from models.order import OrderStatus
from utils.helpers import cetak_header, cetak_garis, generate_id


# ── Inisialisasi ─────────────────────────────────────────────────────────────

marketplace = Marketplace("Marketplace PBO - Hendra")
muat_semua(marketplace)          
marketplace.seed_jika_kosong()   
auth        = AuthService(marketplace)
order_svc   = OrderService(marketplace)


# ── Menu Admin ───────────────────────────────────────────────────────────────

def menu_admin(admin):
    while True:
        cetak_header(f"MENU ADMIN  [{admin.username}]")
        print("  1. Lihat Semua Produk")
        print("  2. Tambah Produk")
        print("  3. Hapus Produk")
        print("  4. Lihat Semua Order")
        print("  5. Update Status Order")
        print("  6. Detail Order")
        print("  7. Lihat Ulasan Produk")
        print("  8. Info Akun")
        print("  0. Logout")
        cetak_garis()
        pilihan = input("  Pilih menu : ").strip()

        if pilihan == "1":
            admin.lihat_semua_produk(marketplace)

        elif pilihan == "2":
            cetak_header("TAMBAH PRODUK")
            nama = input("  Nama Produk  : ").strip()
            # FIX BUG 3: validasi nama dulu sebelum lanjut input lainnya
            if not nama:
                print("[Input] Nama produk tidak boleh kosong.\n")
                continue
            try:
                harga = float(input("  Harga (Rp)   : ").strip())
                stok  = int(input("  Stok         : ").strip())
            except ValueError:
                print("[Input] Harga dan stok harus angka.\n")
                continue
            if harga <= 0:
                print("[Input] Harga harus lebih dari 0.\n")
                continue
            if stok < 0:
                print("[Input] Stok tidak boleh minus.\n")
                continue
            deskripsi = input("  Deskripsi    : ").strip()
            admin.tambah_produk(marketplace, nama, harga, stok, deskripsi)
            simpan_semua(marketplace)

        elif pilihan == "3":
            admin.lihat_semua_produk(marketplace)
            product_id = input("\n  Masukkan ID produk yang dihapus : ").strip()
            admin.hapus_produk(marketplace, product_id)
            simpan_semua(marketplace)

        elif pilihan == "4":
            order_svc.tampilkan_semua_order()

        elif pilihan == "5":
            order_svc.update_status_order()
            simpan_semua(marketplace)

        elif pilihan == "6":
            order_svc.tampilkan_detail_order()

        elif pilihan == "7":
            menu_lihat_ulasan_produk()

        elif pilihan == "8":
            print("\n" + admin.get_info() + "\n")

        elif pilihan == "0":
            auth.logout()
            print()
            break

        else:
            print("[Menu] Pilihan tidak valid.\n")


# ── Menu Customer ────────────────────────────────────────────────────────────

def menu_customer(customer):
    while True:
        cetak_header(f"MENU CUSTOMER  [{customer.nama_lengkap}]")
        print("  1. Lihat Semua Produk")
        print("  2. Cari Produk")
        print("  3. Tambah ke Cart")
        print("  4. Lihat Cart")
        print("  5. Hapus Item dari Cart")
        print("  6. Checkout")
        print("  7. Riwayat Transaksi")
        print("  8. Beri Ulasan Produk")
        print("  9. Lihat Ulasan Produk")
        print("  10. Info Akun")
        print("  0. Logout")
        cetak_garis()
        pilihan = input("  Pilih menu : ").strip()

        if pilihan == "1":
            tampilkan_produk_list()

        elif pilihan == "2":
            keyword = input("  Kata kunci cari produk : ").strip()
            hasil   = marketplace.cari_produk_by_nama(keyword)
            if not hasil:
                print(f"[Produk] Tidak ada produk dengan kata kunci '{keyword}'.\n")
            else:
                print(f"\n  Ditemukan {len(hasil)} produk:\n")
                for p in hasil:
                    print(p)
                    cetak_garis("-")
                print()

        elif pilihan == "3":
            tampilkan_produk_list()
            product_id = input("\n  Masukkan ID produk : ").strip()
            produk     = marketplace.cari_produk(product_id)
            if produk is None:
                print("[Produk] ID tidak ditemukan.\n")
                continue
            try:
                qty = int(input(f"  Jumlah (stok tersedia: {produk.stok}) : ").strip())
            except ValueError:
                print("[Input] Jumlah harus angka.\n")
                continue
            # FIX: qty tidak boleh minus atau nol
            if qty <= 0:
                print("[Input] Jumlah harus lebih dari 0.\n")
                continue
            customer.tambah_ke_cart(produk, qty)

        elif pilihan == "4":
            customer.lihat_cart()

        elif pilihan == "5":
            customer.lihat_cart()
            product_id = input("  Masukkan ID produk yang dihapus dari cart : ").strip()
            produk     = marketplace.cari_produk(product_id)
            if produk is None:
                print("[Produk] ID tidak ditemukan.\n")
                continue
            customer.hapus_dari_cart(produk)

        elif pilihan == "6":
            customer.lihat_cart()
            konfirmasi = input("  Yakin ingin checkout? (y/n) : ").strip().lower()
            if konfirmasi == "y":
                hasil = customer.checkout(marketplace)
                if hasil:
                    simpan_semua(marketplace)
            else:
                print("[Checkout] Dibatalkan.\n")

        elif pilihan == "7":
            customer.lihat_riwayat()

        elif pilihan == "8":
            menu_beri_ulasan(customer)

        elif pilihan == "9":
            menu_lihat_ulasan_produk()

        elif pilihan == "10":
            print("\n" + customer.get_info() + "\n")

        elif pilihan == "0":
            auth.logout()
            print()
            break

        else:
            print("[Menu] Pilihan tidak valid.\n")


def menu_beri_ulasan(customer):
    """Sub-menu untuk beri ulasan produk yang pernah dibeli."""
    cetak_header("BERI ULASAN PRODUK")

    # Hanya tampilkan produk dari order yang sudah Selesai
    riwayat     = customer.history.get_by_status(OrderStatus.COMPLETED)
    produk_beli = []

    for order in riwayat:
        for produk in order.items.keys():
            if produk not in produk_beli:
                produk_beli.append(produk)

    if not produk_beli:
        print("  Kamu belum punya pembelian yang selesai untuk diulas.\n")
        return

    print("  Produk yang bisa kamu ulas:\n")
    for i, p in enumerate(produk_beli, start=1):
        print(f"  {i}. [{p.product_id}] {p.nama}")

    product_id = input("\n  Masukkan ID produk : ").strip()
    produk     = marketplace.cari_produk(product_id)

    if produk is None:
        print("[Ulasan] Produk tidak ditemukan.\n")
        return

    try:
        rating = int(input("  Rating (1-5)    : ").strip())
    except ValueError:
        print("[Input] Rating harus angka.\n")
        return

    komentar = input("  Komentar        : ").strip()
    # FIX BUG 5: komentar tidak boleh kosong
    if not komentar:
        print("[Ulasan] Komentar tidak boleh kosong.\n")
        return
    hasil_ulasan = customer.beri_ulasan(produk, rating, komentar)
    if hasil_ulasan:
        simpan_semua(marketplace)


def menu_lihat_ulasan_produk():
    """Lihat semua ulasan dari suatu produk — bisa diakses admin maupun customer."""
    cetak_header("LIHAT ULASAN PRODUK")
    tampilkan_produk_list()

    product_id = input("  Masukkan ID produk : ").strip()
    produk     = marketplace.cari_produk(product_id)

    if produk is None:
        print("[Ulasan] Produk tidak ditemukan.\n")
        return

    reviews = produk.reviews  # property, return copy list
    print(f"\n  Produk  : {produk.nama}")
    print(f"  Rating  : {produk.get_avg_rating()}/5.0  "
          f"({len(reviews)} ulasan)")
    cetak_garis()

    if not reviews:
        print("  Belum ada ulasan untuk produk ini.\n")
        return

    for i, r in enumerate(reviews, start=1):
        print(f"\n  Ulasan #{i}")
        print(r)

    print()


# ── Helper tampilkan produk ───────────────────────────────────────────────────

def tampilkan_produk_list():
    produk_list = marketplace.get_produk()
    if not produk_list:
        print("\n  Belum ada produk tersedia.\n")
        return
    print(f"\n=== DAFTAR PRODUK ({len(produk_list)} produk) ===\n")
    for p in produk_list:
        print(p)
        cetak_garis("-")
    print()


# ── Menu Utama ────────────────────────────────────────────────────────────────

def menu_utama():
    while True:
        cetak_header(marketplace.nama_toko)
        print("  1. Login")
        print("  2. Daftar Akun Baru")
        print("  3. Lihat Produk (tanpa login)")
        print("  0. Keluar")
        cetak_garis()
        pilihan = input("  Pilih menu : ").strip()

        if pilihan == "1":
            berhasil = auth.login()
            if berhasil:
                user = auth.user_aktif
                if isinstance(user, Admin):
                    menu_admin(user)
                elif isinstance(user, Customer):
                    menu_customer(user)

        elif pilihan == "2":
            berhasil_daftar = auth.register_customer()
            if berhasil_daftar:
                simpan_semua(marketplace)

        elif pilihan == "3":
            tampilkan_produk_list()

        elif pilihan == "0":
            print("\n  Terima kasih sudah menggunakan Marketplace PBO!")
            print("  Sampai jumpa!\n")
            break

        else:
            print("[Menu] Pilihan tidak valid.\n")


# ── Jalankan Aplikasi ────────────────────────────────────────────────────────

if __name__ == "__main__":
    print()
    print("  ╔══════════════════════════════════╗")
    print("  ║    MARKETPLACE APP — PBO 2025    ║")
    print("  ╚══════════════════════════════════╝")
    print()
    menu_utama()