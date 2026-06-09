import datetime


class Review:
    def __init__(self, customer, rating, komentar):
        # validasi rating 1-5
        if not (1 <= rating <= 5):
            raise ValueError("Rating harus antara 1 sampai 5.")

        self.__customer = customer
        self.__rating = rating
        self.__komentar = komentar
        self.__tanggal = datetime.datetime.now()

    @property
    def customer(self):
        return self.__customer

    @property
    def rating(self):
        return self.__rating

    @property
    def komentar(self):
        return self.__komentar

    @property
    def tanggal(self):
        return self.__tanggal

    def get_rating(self):
        return self.__rating

    def __str__(self):
        bintang = "★" * self.__rating + "☆" * (5 - self.__rating)
        tgl = self.__tanggal.strftime("%d-%m-%Y")
        return (f"  {bintang} ({self.__rating}/5)\n"
                f"  Oleh    : {self.__customer.username}\n"
                f"  Tanggal : {tgl}\n"
                f"  Komentar: {self.__komentar}")