import json
import os
import datetime

# path folder data relatif dari root project
DATA_DIR    = os.path.join(os.path.dirname(__file__), "..", "data")
FILE_USERS    = os.path.join(DATA_DIR, "users.json")
FILE_PRODUCTS = os.path.join(DATA_DIR, "products.json")
FILE_ORDERS   = os.path.join(DATA_DIR, "orders.json")


def _pastikan_folder():
    """Buat folder data kalau belum ada."""
    os.makedirs(DATA_DIR, exist_ok=True)


# ── SIMPAN DATA ──────────────────────────────────────────────────────────────

def simpan_semua(marketplace):
    """
    Simpan seluruh state marketplace ke file JSON.
    Dipanggil setiap kali ada perubahan data penting.
    """
    _pastikan_folder()
    _simpan_users(marketplace.get_semua_user())
    _simpan_products(marketplace.get_produk())
    _simpan_orders(marketplace.get_semua_order())


def _simpan_users(users):
    from models.admin import Admin
    from models.customer import Customer

    data = []
    for u in users:
        if isinstance(u, Admin):
            data.append({
                "role"     : "admin",
                "username" : u.username,
                "password" : u._User__password  
            })
        elif isinstance(u, Customer):
            data.append({
                "role"        : "customer",
                "username"    : u.username,
                "password"    : u._User__password,
                "nama_lengkap": u.nama_lengkap,
                "alamat"      : u.alamat,
                "no_telepon"  : u.no_telepon
            })

    with open(FILE_USERS, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def _simpan_products(products):
    data = []
    for p in products:
        reviews_data = []
        for r in p.reviews:
            reviews_data.append({
                "customer_username": r.customer.username,
                "rating"           : r.rating,
                "komentar"         : r.komentar,
                "tanggal"          : r.tanggal.strftime("%Y-%m-%d %H:%M:%S")
            })
        data.append({
            "product_id": p.product_id,
            "nama"      : p.nama,
            "harga"     : p.harga,
            "stok"      : p.stok,
            "deskripsi" : p.deskripsi,
            "reviews"   : reviews_data
        })

    with open(FILE_PRODUCTS, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def _simpan_orders(orders):
    from models.order import OrderStatus

    data = []
    for o in orders:
        items_data = {}
        for produk, qty in o.items.items():
            items_data[produk.product_id] = qty  

        data.append({
            "order_id"          : o.order_id,
            "customer_username" : o.customer.username,
            "items"             : items_data,
            "total"             : o.total,
            "status"            : o.status.value,
            "tanggal"           : o.tanggal.strftime("%Y-%m-%d %H:%M:%S")
        })

    with open(FILE_ORDERS, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# ── MUAT DATA ────────────────────────────────────────────────────────────────

def muat_semua(marketplace):
    """
    Muat data dari JSON ke marketplace saat program pertama jalan.
    Kalau file belum ada, lewati saja (program jalan normal dengan seed).
    """
    _pastikan_folder()

    
    produk_map  = _muat_products(marketplace)
    user_map    = _muat_users(marketplace)
    _muat_orders(marketplace, user_map, produk_map)


def _muat_users(marketplace):
    """Return dict {username: user_object} untuk dipakai muat_orders."""
    from models.admin import Admin
    from models.customer import Customer

    if not os.path.exists(FILE_USERS):
        return {}

    with open(FILE_USERS, "r", encoding="utf-8") as f:
        data = json.load(f)

    user_map = {}
    for item in data:
        if item["role"] == "admin":
            u = Admin(item["username"], item["password"])
            marketplace.daftarkan_user(u)
            user_map[u.username] = u

        elif item["role"] == "customer":
            u = Customer(
                item["username"], item["password"],
                item["nama_lengkap"], item["alamat"], item["no_telepon"]
            )
            marketplace.daftarkan_user(u)
            user_map[u.username] = u

    return user_map


def _muat_products(marketplace):
    """Return dict {product_id: product_object} untuk dipakai muat_orders."""
    from models.product import Product
    from models.review import Review

    if not os.path.exists(FILE_PRODUCTS):
        return {}

    with open(FILE_PRODUCTS, "r", encoding="utf-8") as f:
        data = json.load(f)

    produk_map = {}
    for item in data:
        p = Product(
            item["product_id"], item["nama"],
            item["harga"], item["stok"], item["deskripsi"]
        )
        
        p._pending_reviews = item.get("reviews", [])
        marketplace.tambah_produk(p)
        produk_map[p.product_id] = p

    return produk_map


def _muat_orders(marketplace, user_map, produk_map):
    """Muat orders dan sambungkan review ke produk."""
    from models.order import Order, OrderStatus
    from models.review import Review

    for produk in produk_map.values():
        for rv in getattr(produk, "_pending_reviews", []):
            customer = user_map.get(rv["customer_username"])
            if customer:
                r = Review.__new__(Review)
                r._Review__customer = customer
                r._Review__rating   = rv["rating"]
                r._Review__komentar = rv["komentar"]
                r._Review__tanggal  = datetime.datetime.strptime(
                    rv["tanggal"], "%Y-%m-%d %H:%M:%S"
                )
                produk.tambah_review(r)
    
        if hasattr(produk, "_pending_reviews"):
            del produk._pending_reviews

    if not os.path.exists(FILE_ORDERS):
        return

    with open(FILE_ORDERS, "r", encoding="utf-8") as f:
        data = json.load(f)

    status_map = {s.value: s for s in OrderStatus}

    for item in data:
        customer = user_map.get(item["customer_username"])
        if customer is None:
            continue

        items = {}
        for pid, qty in item["items"].items():
            p = produk_map.get(pid)
            if p:
                items[p] = qty

      
        o = Order.__new__(Order)
        o._Order__order_id = item["order_id"]
        o._Order__customer = customer
        o._Order__items    = items
        o._Order__total    = item["total"]
        o._Order__status   = status_map.get(item["status"], OrderStatus.PENDING)
        o._Order__tanggal  = datetime.datetime.strptime(
            item["tanggal"], "%Y-%m-%d %H:%M:%S"
        )

        marketplace.tambah_order(o)

        # masukkan juga ke history customer
        customer.history.tambah_order(o)