from enum import Enum
import datetime


class OrderStatus(Enum):
    PENDING    = "Pending"
    PROCESSING = "Diproses"
    COMPLETED  = "Selesai"


class Order:
    def __init__(self, order_id, customer, items, total):
        self.__order_id = order_id
        self.__customer = customer
        self.__items = items       
        self.__total = total
        self.__status = OrderStatus.PENDING
        self.__tanggal = datetime.datetime.now()

    # getter
    @property
    def order_id(self):
        return self.__order_id

    @property
    def customer(self):
        return self.__customer

    @property
    def items(self):
        return self.__items

    @property
    def total(self):
        return self.__total

    @property
    def status(self):
        return self.__status

    @property
    def tanggal(self):
        return self.__tanggal

    def update_status(self, status_baru):
        if not isinstance(status_baru, OrderStatus):
            print("[Order] Status tidak valid.")
            return False

        urutan = [OrderStatus.PENDING, OrderStatus.PROCESSING, OrderStatus.COMPLETED]
        idx_sekarang = urutan.index(self.__status)
        idx_baru = urutan.index(status_baru)

        if idx_baru <= idx_sekarang:
            print(f"[Order] Tidak bisa mengubah status dari "
                  f"'{self.__status.value}' ke '{status_baru.value}'.")
            return False

        self.__status = status_baru
        return True

    def get_detail(self):
        tgl = self.__tanggal.strftime("%d-%m-%Y %H:%M")
        baris_item = ""
        for produk, qty in self.__items.items():
            subtotal = produk.harga * qty
            baris_item += (f"  - {produk.nama:<25} x{qty}  "
                           f"Rp {subtotal:>12,.0f}\n")
        return (
            f"\n===== Detail Order =====\n"
            f"Order ID  : {self.__order_id}\n"
            f"Tanggal   : {tgl}\n"
            f"Customer  : {self.__customer.nama_lengkap}\n"
            f"Status    : {self.__status.value}\n"
            f"Item      :\n{baris_item}"
            f"{'':->45}\n"
            f"Total     : Rp {self.__total:>12,.0f}\n"
            f"========================\n"
        )

    def berisi_produk(self, produk):
        return produk in self.__items

    def __str__(self):
        tgl = self.__tanggal.strftime("%d-%m-%Y %H:%M")
        return (f"Order [{self.__order_id}] | "
                f"{tgl} | "
                f"Rp {self.__total:,.0f} | "
                f"Status: {self.__status.value}")