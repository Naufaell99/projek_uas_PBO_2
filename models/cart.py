class Cart:
    def __init__(self):
        # key = objek Product, value = qty
        self.__items = {}

    def tambah_item(self, produk, qty=1):
        if qty <= 0:
            print("[Cart] Jumlah harus lebih dari 0.")
            return

        if produk.stok < qty:
            print(f"[Cart] Stok '{produk.nama}' tidak cukup. "
                  f"Tersedia: {produk.stok}.")
            return

        if produk in self.__items:
            self.__items[produk] += qty
        else:
            self.__items[produk] = qty

        print(f"[Cart] '{produk.nama}' x{qty} ditambahkan ke cart.")

    def hapus_item(self, produk):
        if produk not in self.__items:
            print(f"[Cart] '{produk.nama}' tidak ada di cart.")
            return
        del self.__items[produk]
        print(f"[Cart] '{produk.nama}' dihapus dari cart.")

    def get_total(self):
        total = 0
        for produk, qty in self.__items.items():
            total += produk.harga * qty
        return total

    def get_items(self):
        return self.__items

    def kosong(self):
        return len(self.__items) == 0

    def kosongkan(self):
        self.__items.clear()

    def tampilkan(self):
        if self.kosong():
            print("[Cart] Cart kamu masih kosong.")
            return

        print("\n===== Isi Cart =====")
        for i, (produk, qty) in enumerate(self.__items.items(), start=1):
            subtotal = produk.harga * qty
            print(f"  {i}. {produk.nama:<25} x{qty}  "
                  f"@ Rp {produk.harga:>10,.0f}  "
                  f"= Rp {subtotal:>12,.0f}")
        print(f"{'':->48}")
        print(f"  Total : Rp {self.get_total():>12,.0f}")
        print("====================\n")