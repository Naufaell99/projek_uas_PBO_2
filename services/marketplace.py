from models.admin import Admin
from models.product import Product
from utils.helpers import generate_id


class Marketplace:
    """
    Pusat data aplikasi: nyimpan semua produk, order, dan user.
    Admin default dibuat otomatis hanya saat data kosong (file JSON belum ada).
    """

    def __init__(self, nama_toko="Toko Online PBO"):
        self.__nama_toko  = nama_toko
        self.__produk_list = []
        self.__order_list  = []
        self.__user_list   = []

    @property
    def nama_toko(self):
        return self.__nama_toko

    def seed_jika_kosong(self):
        """
        Dipanggil setelah muat_semua() — kalau data benar-benar kosong
        (pertama kali jalan), baru seed admin dan produk contoh.
        """
        if not self.__user_list:
            self._seed_admin()
        if not self.__produk_list:
            self._seed_produk_contoh()

    def _seed_admin(self):
        admin_default = Admin("pbo", "pbo26")
        self.__user_list.append(admin_default)

    def _seed_produk_contoh(self):
        contoh = [
            Product(generate_id("PRD"), "Laptop Asus VivoBook",    7_500_000, 10, "Intel i5, RAM 8GB, SSD 512GB"),
            Product(generate_id("PRD"), "Mouse Wireless Logitech",   150_000, 50, "DPI 1600, baterai tahan lama"),
            Product(generate_id("PRD"), "Keyboard Mechanical",       350_000, 25, "Switch Blue, RGB backlight"),
            Product(generate_id("PRD"), "Headset Gaming Rexus",      200_000, 30, "Surround 7.1, mic noise cancel"),
        ]
        self.__produk_list.extend(contoh)

    # ── Manajemen Produk ─────────────────────────────────────────

    def tambah_produk(self, produk):
        self.__produk_list.append(produk)

    def hapus_produk(self, product_id):
        for p in self.__produk_list:
            if p.product_id == product_id:
                if self._produk_ada_di_cart(p):
                    print(f"[Marketplace] Produk '{p.nama}' tidak bisa dihapus "
                          f"karena masih ada di cart customer.")
                    return False
                self.__produk_list.remove(p)
                return True
        return False

    def _produk_ada_di_cart(self, produk):
        from models.customer import Customer
        for user in self.__user_list:
            if isinstance(user, Customer):
                if produk in user.cart.get_items():
                    return True
        return False

    def cari_produk(self, product_id):
        for p in self.__produk_list:
            if p.product_id == product_id:
                return p
        return None

    def cari_produk_by_nama(self, keyword):
        keyword = keyword.lower()
        return [p for p in self.__produk_list if keyword in p.nama.lower()]

    def get_produk(self):
        return list(self.__produk_list)

    # ── Manajemen Order ──────────────────────────────────────────

    def tambah_order(self, order):
        self.__order_list.append(order)

    def cari_order(self, order_id):
        for o in self.__order_list:
            if o.order_id == order_id:
                return o
        return None

    def get_semua_order(self):
        return list(self.__order_list)

    # ── Manajemen User ───────────────────────────────────────────

    def daftarkan_user(self, user):
        self.__user_list.append(user)

    def cari_user(self, username):
        for u in self.__user_list:
            if u.username.lower() == username.lower():
                return u
        return None

    def username_tersedia(self, username):
        return self.cari_user(username.lower()) is None

    def get_semua_user(self):
        return list(self.__user_list)

    def __str__(self):
        return (
            f"=== {self.__nama_toko} ===\n"
            f"Total Produk : {len(self.__produk_list)}\n"
            f"Total Order  : {len(self.__order_list)}\n"
            f"Total User   : {len(self.__user_list)}"
        )