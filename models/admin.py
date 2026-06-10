from models.user import User


class Admin(User):
    def __init__(self, username, password):
        super().__init__(username, password)
    
        self.__managed_products = []
        self.__managed_orders = []

    def login(self, password):
        if self.check_password(password):
            self._is_logged_in = True
            print(f"[Admin] Selamat datang, {self._username}!")
            return True
        print("[Admin] Password salah.")
        return False

    def logout(self):
        self._is_logged_in = False
        print(f"[Admin] {self._username} telah logout.")

    def get_info(self):
        status = "Login" if self._is_logged_in else "Logout"
        return (
            f"=== Info Admin ===\n"
            f"Username : {self._username}\n"
            f"Role     : Administrator\n"
            f"Status   : {status}"
        )

    def tambah_produk(self, marketplace, nama, harga, stok, deskripsi=""):
        from models.product import Product
        from utils.helpers import generate_id

        produk_baru = Product(generate_id("PRD"), nama, harga, stok, deskripsi)
        marketplace.tambah_produk(produk_baru)
        self.__managed_products.append(produk_baru)
        print(f"[Admin] Produk '{nama}' berhasil ditambahkan.")
        return produk_baru

    def hapus_produk(self, marketplace, product_id):
        hasil = marketplace.hapus_produk(product_id)
        if hasil:
            print(f"[Admin] Produk ID {product_id} berhasil dihapus.")
        else:
            print(f"[Admin] Produk ID {product_id} tidak ditemukan.")
        return hasil

    def update_status_order(self, marketplace, order_id, status_baru):
        order = marketplace.cari_order(order_id)
        if order is None:
            print(f"[Admin] Order ID {order_id} tidak ditemukan.")
            return False
        order.update_status(status_baru)
        print(f"[Admin] Status order {order_id} diubah ke '{status_baru.value}'.")
        return True

    def lihat_semua_order(self, marketplace):
        semua_order = marketplace.get_semua_order()
        if not semua_order:
            print("[Admin] Belum ada order masuk.")
            return
        print("\n=== Daftar Semua Order ===")
        for order in semua_order:
            print(order)

    def lihat_semua_produk(self, marketplace):
        produk_list = marketplace.get_produk()
        if not produk_list:
            print("[Admin] Belum ada produk.")
            return
        print("\n=== Daftar Produk ===")
        for p in produk_list:
            print(p)

    def __str__(self):
        return f"Admin({self._username})"