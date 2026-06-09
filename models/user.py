from abc import ABC, abstractmethod


class User(ABC):
    def __init__(self, username, password):
        self._username = username
        self.__password = password
        self._is_logged_in = False

    # getter buat username, password disimpan private jadi gak bisa diakses langsung
    @property
    def username(self):
        return self._username

    @property
    def is_logged_in(self):
        return self._is_logged_in

    def check_password(self, password):
        return self.__password == password

    # method abstrak — wajib di-override di subclass
    @abstractmethod
    def login(self, password):
        pass

    @abstractmethod
    def logout(self):
        pass

    @abstractmethod
    def get_info(self):
        pass

    def __str__(self):
        return f"User({self._username})"