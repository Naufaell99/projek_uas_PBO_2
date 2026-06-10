from models.order import OrderStatus


class TransactionHistory:
    def __init__(self):
        self.__orders = []

    def tambah_order(self, order):
        self.__orders.append(order)

    def get_semua(self):
        return list(self.__orders)

    def get_by_status(self, status):
        return [o for o in self.__orders if o.status == status]

    def sudah_beli(self, produk):
        for order in self.__orders:
            if order.status == OrderStatus.COMPLETED and order.berisi_produk(produk):
                return True
        return False

    def tampilkan(self):
        if not self.__orders:
            print("[Riwayat] Belum ada transaksi.")
            return

        print("\n===== Riwayat Transaksi =====")
        for i, order in enumerate(self.__orders, start=1):
            print(f"  {i}. {order}")
        print("==============================\n")

    def tampilkan_detail(self, order_id):
        for order in self.__orders:
            if order.order_id == order_id:
                print(order.get_detail())
                return
        print(f"[Riwayat] Order ID '{order_id}' tidak ditemukan.")