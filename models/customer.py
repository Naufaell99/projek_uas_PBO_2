from models.user import User
from models.cart import Cart
from models.transaction_history import TransactionHistory


class Customer(User):
    def __init__(self, username, password, nama_lengkap, alamat, no_telepon):
        super().__init__(username, password)
        self.__nama_lengkap = nama_lengkap
        self.__alamat = alamat
        self.__no_telepon = no_telepon

        self.__cart = Cart()
        self.__history = TransactionHistory()

    # getter
    @property
    def nama_lengkap(self):
        return self.__nama_lengkap

    @property
    def alamat(self):
        return self.__alamat

    @property
    def no_telepon(self):
        return self.__no_telepon

    @property
    def cart(self):
        return self.__cart

    @property
    def history(self):
        return self.__history

    # override login
    def login(self, password):
        if self.check_password(password):
            self._is_logged_in = True
            print(f"[Customer] Selamat datang, {self.__nama_lengkap}!")
            return True
        print("[Customer] Username atau password salah.")
        return False

    def logout(self):
        self._is_logged_in = False
        print(f"[Customer] {self.__nama_lengkap} telah logout.")

    # override get_info — lebih lengkap dari admin karena ada alamat dll
    def get_info(self):
        status = "Login" if self._is_logged_in else "Logout"
        return (
            f"=== Info Customer ===\n"
            f"Username     : {self._username}\n"
            f"Nama Lengkap : {self.__nama_lengkap}\n"
            f"Alamat       : {self.__alamat}\n"
            f"No. Telepon  : {self.__no_telepon}\n"
            f"Status       : {status}"
        )

    def tambah_ke_cart(self, produk, qty):
        self.__cart.tambah_item(produk, qty)

    def hapus_dari_cart(self, produk):
        self.__cart.hapus_item(produk)

    def lihat_cart(self):
        self.__cart.tampilkan()

    def checkout(self, marketplace):
        if self.__cart.kosong():
            print("[Customer] Cart masih kosong, tidak bisa checkout.")
            return None

        from models.order import Order
        from utils.helpers import generate_id
        import datetime

        order_id = generate_id("ORD")
        items_snapshot = dict(self.__cart.get_items())
        total = self.__cart.get_total()

        # cek stok semua item dulu sebelum proses
        for produk, qty in items_snapshot.items():
            if produk.stok < qty:
                print(f"[Customer] Stok '{produk.nama}' tidak cukup. "
                      f"Tersedia: {produk.stok}, diminta: {qty}.")
                return None

        # kurangi stok & buat order
        for produk, qty in items_snapshot.items():
            produk.kurangi_stok(qty)

        order_baru = Order(order_id, self, items_snapshot, total)
        self.__history.tambah_order(order_baru)
        marketplace.tambah_order(order_baru)

        self.__cart.kosongkan()
        print(f"[Customer] Checkout berhasil! Order ID: {order_id}")
        print(f"           Total bayar: Rp {total:,.0f}")
        return order_baru

    def beri_ulasan(self, produk, rating, komentar):
        from models.review import Review
        from utils.helpers import generate_id

        # pastikan customer sudah pernah beli produk ini
        if not self.__history.sudah_beli(produk):
            print("[Customer] Kamu belum pernah membeli produk ini.")
            return None

        # cek apakah sudah review sebelumnya
        if produk.sudah_direview_oleh(self):
            print("[Customer] Kamu sudah pernah memberi ulasan untuk produk ini.")
            return None

        review_baru = Review(self, rating, komentar)
        produk.tambah_review(review_baru)
        print(f"[Customer] Ulasan berhasil ditambahkan untuk '{produk.nama}'.")
        return review_baru

    def lihat_riwayat(self):
        self.__history.tampilkan()

    def __str__(self):
        return f"Customer({self._username} - {self.__nama_lengkap})"