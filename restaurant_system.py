import datetime
from typing import Dict, List, Optional

class MenuItem:
    """Kelas untuk item menu"""
    def __init__(self, id: int, nama: str, harga: float, kategori: str, stok: int = 100):
        self.id = id
        self.nama = nama
        self.harga = harga
        self.kategori = kategori
        self.stok = stok
    
    def __str__(self):
        return f"{self.nama} - Rp{self.harga:,.0f} ({self.kategori}) - Stok: {self.stok}"

class Order:
    """Kelas untuk pesanan"""
    def __init__(self, order_id: int, nomor_meja: int):
        self.order_id = order_id
        self.nomor_meja = nomor_meja
        self.items: List[Dict] = []
        self.total = 0.0
        self.status = "pending"
        self.waktu_order = datetime.datetime.now()
    
    def tambah_item(self, menu_item: MenuItem, quantity: int):
        """Menambah item ke pesanan"""
        if menu_item.stok >= quantity:
            item_total = menu_item.harga * quantity
            self.items.append({
                'menu_item': menu_item,
                'quantity': quantity,
                'subtotal': item_total
            })
            self.total += item_total
            menu_item.stok -= quantity
            return True
        else:
            print(f"Stok tidak cukup! Stok tersedia: {menu_item.stok}")
            return False
    
    def hapus_item(self, menu_item_id: int):
        """Menghapus item dari pesanan"""
        for i, item in enumerate(self.items):
            if item['menu_item'].id == menu_item_id:
                # Kembalikan stok
                item['menu_item'].stok += item['quantity']
                self.total -= item['subtotal']
                del self.items[i]
                return True
        return False
    
    def cetak_struk(self):
        """Mencetak struk pesanan"""
        print(f"\n{'='*50}")
        print(f"{'RESTORAN PYTHON':^50}")
        print(f"{'='*50}")
        print(f"Order ID: {self.order_id}")
        print(f"Nomor Meja: {self.nomor_meja}")
        print(f"Waktu: {self.waktu_order.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'-'*50}")
        
        for item in self.items:
            menu_item = item['menu_item']
            quantity = item['quantity']
            subtotal = item['subtotal']
            print(f"{menu_item.nama:<25} {quantity}x Rp{menu_item.harga:>8,.0f} = Rp{subtotal:>10,.0f}")
        
        print(f"{'-'*50}")
        print(f"{'TOTAL':<40} Rp{self.total:>10,.0f}")
        print(f"{'='*50}\n")

class RestaurantSystem:
    """Sistem utama restoran"""
    def __init__(self):
        self.menu: Dict[int, MenuItem] = {}
        self.orders: Dict[int, Order] = {}
        self.order_counter = 1
        self.load_default_menu()
    
    def load_default_menu(self):
        """Memuat menu default"""
        default_items = [
            (1, "Nasi Goreng", 25000, "Makanan Utama"),
            (2, "Mie Ayam", 20000, "Makanan Utama"),
            (3, "Soto Ayam", 18000, "Makanan Utama"),
            (4, "Gado-Gado", 15000, "Makanan Utama"),
            (5, "Es Teh", 5000, "Minuman"),
            (6, "Es Jeruk", 7000, "Minuman"),
            (7, "Kopi", 8000, "Minuman"),
            (8, "Jus Alpukat", 12000, "Minuman"),
            (9, "Pisang Goreng", 10000, "Snack"),
            (10, "Tahu Isi", 8000, "Snack")
        ]
        
        for item_data in default_items:
            item = MenuItem(*item_data)
            self.menu[item.id] = item
    
    def tampilkan_menu(self, kategori: Optional[str] = None):
        """Menampilkan menu"""
        print(f"\n{'='*60}")
        print(f"{'MENU RESTORAN':^60}")
        print(f"{'='*60}")
        
        if kategori:
            items = [item for item in self.menu.values() if item.kategori == kategori]
            print(f"Kategori: {kategori}")
        else:
            items = list(self.menu.values())
        
        # Grup berdasarkan kategori
        categories = {}
        for item in items:
            if item.kategori not in categories:
                categories[item.kategori] = []
            categories[item.kategori].append(item)
        
        for cat, cat_items in categories.items():
            print(f"\n{cat}:")
            print("-" * 60)
            for item in cat_items:
                print(f"{item.id:2d}. {item}")
        print("=" * 60)
    
    def tambah_menu(self, nama: str, harga: float, kategori: str, stok: int = 100):
        """Menambah item menu baru"""
        new_id = max(self.menu.keys()) + 1 if self.menu else 1
        new_item = MenuItem(new_id, nama, harga, kategori, stok)
        self.menu[new_id] = new_item
        print(f"Menu '{nama}' berhasil ditambahkan dengan ID {new_id}")
    
    def hapus_menu(self, item_id: int):
        """Menghapus item menu"""
        if item_id in self.menu:
            deleted_item = self.menu.pop(item_id)
            print(f"Menu '{deleted_item.nama}' berhasil dihapus")
            return True
        else:
            print("Item menu tidak ditemukan")
            return False
    
    def buat_pesanan(self, nomor_meja: int):
        """Membuat pesanan baru"""
        order = Order(self.order_counter, nomor_meja)
        self.orders[self.order_counter] = order
        self.order_counter += 1
        print(f"Pesanan baru dibuat untuk meja {nomor_meja} dengan ID {order.order_id}")
        return order
    
    def tampilkan_pesanan(self, order_id: int):
        """Menampilkan detail pesanan"""
        if order_id in self.orders:
            order = self.orders[order_id]
            print(f"\nPesanan ID: {order_id}")
            print(f"Meja: {order.nomor_meja}")
            print(f"Status: {order.status}")
            print(f"Waktu: {order.waktu_order.strftime('%Y-%m-%d %H:%M:%S')}")
            print("-" * 40)
            
            if order.items:
                for item in order.items:
                    menu_item = item['menu_item']
                    print(f"{menu_item.nama} x{item['quantity']} = Rp{item['subtotal']:,.0f}")
                print("-" * 40)
                print(f"Total: Rp{order.total:,.0f}")
            else:
                print("Belum ada item dalam pesanan")
        else:
            print("Pesanan tidak ditemukan")
    
    def ubah_status_pesanan(self, order_id: int, status: str):
        """Mengubah status pesanan"""
        if order_id in self.orders:
            self.orders[order_id].status = status
            print(f"Status pesanan {order_id} diubah menjadi '{status}'")
        else:
            print("Pesanan tidak ditemukan")
    
    def laporan_penjualan(self):
        """Menampilkan laporan penjualan"""
        print(f"\n{'='*60}")
        print(f"{'LAPORAN PENJUALAN':^60}")
        print(f"{'='*60}")
        
        total_pendapatan = 0
        total_pesanan = len(self.orders)
        
        if self.orders:
            print(f"Total Pesanan: {total_pesanan}")
            print("-" * 60)
            
            for order_id, order in self.orders.items():
                print(f"Order #{order_id} - Meja {order.nomor_meja} - Rp{order.total:,.0f} - {order.status}")
                total_pendapatan += order.total
            
            print("-" * 60)
            print(f"Total Pendapatan: Rp{total_pendapatan:,.0f}")
            print(f"Rata-rata per Pesanan: Rp{total_pendapatan/total_pesanan:,.0f}")
        else:
            print("Belum ada pesanan")
        print("=" * 60)

def main():
    """Fungsi utama untuk menjalankan sistem"""
    restaurant = RestaurantSystem()
    
    while True:
        print(f"\n{'='*60}")
        print(f"{'SISTEM MANAJEMEN RESTORAN':^60}")
        print(f"{'='*60}")
        print("1. Tampilkan Menu")
        print("2. Tambah Menu")
        print("3. Hapus Menu")
        print("4. Buat Pesanan Baru")
        print("5. Tampilkan Pesanan")
        print("6. Ubah Status Pesanan")
        print("7. Laporan Penjualan")
        print("8. Keluar")
        print("=" * 60)
        
        try:
            pilihan = input("Pilih menu (1-8): ").strip()
            
            if pilihan == "1":
                restaurant.tampilkan_menu()
                
            elif pilihan == "2":
                nama = input("Nama menu: ")
                harga = float(input("Harga: "))
                kategori = input("Kategori: ")
                stok = int(input("Stok (default 100): ") or "100")
                restaurant.tambah_menu(nama, harga, kategori, stok)
                
            elif pilihan == "3":
                restaurant.tampilkan_menu()
                item_id = int(input("ID menu yang akan dihapus: "))
                restaurant.hapus_menu(item_id)
                
            elif pilihan == "4":
                nomor_meja = int(input("Nomor meja: "))
                order = restaurant.buat_pesanan(nomor_meja)
                
                # Proses menambah item ke pesanan
                while True:
                    restaurant.tampilkan_menu()
                    print(f"\nPesanan untuk meja {nomor_meja} (Order ID: {order.order_id})")
                    print("Ketik 'selesai' untuk mengakhiri pesanan")
                    print("Ketik 'hapus' untuk menghapus item")
                    print("Ketik 'struk' untuk mencetak struk")
                    
                    action = input("Masukkan ID menu atau perintah: ").strip().lower()
                    
                    if action == "selesai":
                        if order.items:
                            order.cetak_struk()
                            restaurant.ubah_status_pesanan(order.order_id, "completed")
                        break
                    elif action == "struk":
                        order.cetak_struk()
                    elif action == "hapus":
                        if order.items:
                            print("Item dalam pesanan:")
                            for i, item in enumerate(order.items):
                                print(f"{item['menu_item'].id}. {item['menu_item'].nama}")
                            item_id = int(input("ID item yang akan dihapus: "))
                            order.hapus_item(item_id)
                        else:
                            print("Tidak ada item dalam pesanan")
                    else:
                        try:
                            menu_id = int(action)
                            if menu_id in restaurant.menu:
                                quantity = int(input("Jumlah: "))
                                if order.tambah_item(restaurant.menu[menu_id], quantity):
                                    print(f"Item berhasil ditambahkan ke pesanan")
                                    print(f"Total sementara: Rp{order.total:,.0f}")
                            else:
                                print("ID menu tidak valid")
                        except ValueError:
                            print("Input tidak valid")
                
            elif pilihan == "5":
                if restaurant.orders:
                    print("Daftar Pesanan:")
                    for order_id in restaurant.orders:
                        print(f"Order ID: {order_id}")
                    order_id = int(input("Masukkan Order ID: "))
                    restaurant.tampilkan_pesanan(order_id)
                else:
                    print("Belum ada pesanan")
                
            elif pilihan == "6":
                if restaurant.orders:
                    print("Daftar Pesanan:")
                    for order_id, order in restaurant.orders.items():
                        print(f"Order ID: {order_id} - Status: {order.status}")
                    order_id = int(input("Order ID: "))
                    status = input("Status baru (pending/preparing/ready/completed): ")
                    restaurant.ubah_status_pesanan(order_id, status)
                else:
                    print("Belum ada pesanan")
                
            elif pilihan == "7":
                restaurant.laporan_penjualan()
                
            elif pilihan == "8":
                print("Terima kasih telah menggunakan sistem restoran!")
                break
                
            else:
                print("Pilihan tidak valid!")
                
        except ValueError:
            print("Input tidak valid! Silakan masukkan angka.")
        except KeyboardInterrupt:
            print("\nProgram dihentikan oleh user.")
            break
        except Exception as e:
            print(f"Terjadi error: {e}")

if __name__ == "__main__":
    main()