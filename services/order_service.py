from models.order import OrderStatus
from utils.helpers import cetak_header


class OrderService:
    """
    Menangani operasi order: lihat detail, update status.
    Dipakai terutama oleh admin.
    """

    def __init__(self, marketplace):
        self.__marketplace = marketplace

    def tampilkan_semua_order(self):
        """Tampilkan semua order yang masuk ke marketplace."""
        cetak_header("SEMUA ORDER MASUK")
        semua_order = self.__marketplace.get_semua_order()

        if not semua_order:
            print("  Belum ada order masuk.\n")
            return

        for i, order in enumerate(semua_order, start=1):
            print(f"  {i}. {order}")
        print()

    def tampilkan_detail_order(self):
        """Admin bisa lihat detail spesifik satu order."""
        order_id = input("  Masukkan Order ID : ").strip()
        order = self.__marketplace.cari_order(order_id)

        if order is None:
            print(f"[Order] Order ID '{order_id}' tidak ditemukan.\n")
            return

        print(order.get_detail())

    def update_status_order(self):
        """
        Admin pilih order, lalu pilih status baru.
        Status hanya bisa maju (Pending -> Diproses -> Selesai).
        """
        cetak_header("UPDATE STATUS ORDER")
        self.tampilkan_semua_order()

        order_id = input("  Masukkan Order ID yang ingin diupdate : ").strip()
        order = self.__marketplace.cari_order(order_id)

        if order is None:
            print(f"[Order] Order ID '{order_id}' tidak ditemukan.\n")
            return

        print(f"\n  Status sekarang : {order.status.value}")
        print("  Pilih status baru:")
        print("  1. Diproses")
        print("  2. Selesai")
        pilihan = input("  Pilihan : ").strip()

        if pilihan == "1":
            status_baru = OrderStatus.PROCESSING
        elif pilihan == "2":
            status_baru = OrderStatus.COMPLETED
        else:
            print("[Order] Pilihan tidak valid.\n")
            return

        berhasil = order.update_status(status_baru)
        if berhasil:
            print(f"[Order] Status order {order_id} berhasil diubah ke '{status_baru.value}'.\n")