import re
from models.customer import Customer
from utils.helpers import cetak_header


class AuthService:
    """
    Menangani proses login dan registrasi user.
    Menyimpan referensi siapa yang sedang login (sesi aktif).
    """

    def __init__(self, marketplace):
        self.__marketplace = marketplace
        self.__user_aktif = None

    @property
    def user_aktif(self):
        return self.__user_aktif

    def sudah_login(self):
        return self.__user_aktif is not None and self.__user_aktif.is_logged_in

    def login(self):
        cetak_header("LOGIN")
        username = input("  Username : ").strip()
        password = input("  Password : ").strip()

        # FIX BUG 4: password tidak boleh kosong
        if not username or not password:
            print("\n[Auth] Username dan password tidak boleh kosong.\n")
            return False

        user = self.__marketplace.cari_user(username)

        if user is None:
            print("\n[Auth] Username tidak ditemukan.\n")
            return False

        berhasil = user.login(password)
        if berhasil:
            self.__user_aktif = user
            print()
            return True
        else:
            print()
            return False

    def logout(self):
        if self.__user_aktif:
            self.__user_aktif.logout()
            self.__user_aktif = None

    def register_customer(self):
        """
        Registrasi akun customer baru.
        Hanya customer yang bisa mendaftar sendiri,
        admin dibuat manual/di-seed.
        """
        cetak_header("DAFTAR AKUN BARU")
        print("  Isi data kamu di bawah ini:\n")

        username = input("  Username      : ").strip()
        if not username:
            print("[Register] Username tidak boleh kosong.\n")
            return False

        if not self.__marketplace.username_tersedia(username):
            print("[Register] Username sudah dipakai, coba yang lain.\n")
            return False

        password = input("  Password      : ").strip()
        if len(password) < 4:
            print("[Register] Password minimal 4 karakter.\n")
            return False

        nama_lengkap = input("  Nama Lengkap  : ").strip()
        if not nama_lengkap:
            print("[Register] Nama lengkap tidak boleh kosong.\n")
            return False

        alamat = input("  Alamat        : ").strip()
        if not alamat:
            print("[Register] Alamat tidak boleh kosong.\n")
            return False

        no_telepon = input("  No. Telepon   : ").strip()
        if not no_telepon:
            print("[Register] No. Telepon tidak boleh kosong.\n")
            return False

        no_bersih = re.sub(r"[\s\-]", "", no_telepon)
        if not no_bersih.isdigit():
            print("[Register] No. Telepon hanya boleh berisi angka.\n")
            return False
        if not (9 <= len(no_bersih) <= 13):
            print("[Register] No. Telepon harus 9-13 digit "
                  "(contoh: 081234567890).\n")
            return False

        customer_baru = Customer(username, password, nama_lengkap, alamat, no_telepon)
        self.__marketplace.daftarkan_user(customer_baru)

        print(f"\n[Register] Akun '{username}' berhasil dibuat! Silakan login.\n")
        return True