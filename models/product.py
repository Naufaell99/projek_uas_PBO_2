class Product:
    def __init__(self, product_id, nama, harga, stok, deskripsi=""):
        self.__product_id = product_id
        self.__nama = nama
        self.__harga = harga
        self.__stok = stok
        self.__deskripsi = deskripsi
        self.__reviews = []

    # getter — semua atribut private, akses lewat property
    @property
    def product_id(self):
        return self.__product_id

    @property
    def nama(self):
        return self.__nama

    @property
    def harga(self):
        return self.__harga

    @property
    def stok(self):
        return self.__stok

    @property
    def deskripsi(self):
        return self.__deskripsi

    @property
    def reviews(self):
        return list(self.__reviews)  # return copy, biar list asli gak bisa diutak-atik

    def kurangi_stok(self, qty):
        if qty > self.__stok:
            raise ValueError(f"Stok tidak cukup. Stok tersedia: {self.__stok}")
        self.__stok -= qty

    def tambah_stok(self, qty):
        self.__stok += qty

    def tambah_review(self, review):
        self.__reviews.append(review)

    def sudah_direview_oleh(self, customer):
        for r in self.__reviews:
            if r.customer.username == customer.username:
                return True
        return False

    def get_avg_rating(self):
        if not self.__reviews:
            return 0.0
        total = sum(r.rating for r in self.__reviews)
        return round(total / len(self.__reviews), 1)

    def __str__(self):
        rating = self.get_avg_rating()
        bintang = f"{rating}/5.0" if rating > 0 else "Belum ada rating"
        return (
            f"[{self.__product_id}] {self.__nama}\n"
            f"  Harga      : Rp {self.__harga:,.0f}\n"
            f"  Stok       : {self.__stok} pcs\n"
            f"  Rating     : {bintang}\n"
            f"  Deskripsi  : {self.__deskripsi or '-'}"
        )