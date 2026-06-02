import json
import os

class Hash:
    def __init__(self, size=1000):
        self.size = size
        self.table = [[] for _ in range(size)]
    
    def save_to_json(self, filename):
        with open(filename, 'w') as f:
            json.dump(self.table, f)

    def load_from_json(self, filename):
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                self.table = json.load(f)
                self.size = len(self.table)
    
    # fungsi hash sederhana yang mengambil bagian numerik dari idTicket dan menggunakan modulus untuk menentukan index
    def _hash(self, idTicket):
        numeric_part = int (''.join(filter(str.isdigit, idTicket))) 
        return numeric_part % self.size
    
    #cek apakah idTicket sudah terdaftar untuk mencegah duplikasi
    def cek_duplikat_id(self, idTicket):
        index = self._hash(idTicket)
        for data in self.table[index]:
            if data["id"] == idTicket:
                return True
        return False

    #daftarkan pendaki dengan idTicket, nama, dan kontak jika ID belum ada
    def daftar_pendaki(self, idTicket, nama, kontak, tanggal):
        index = self._hash(idTicket)
        if self.cek_duplikat_id(idTicket):
            return False
        dataPendaki = {"id": idTicket, "nama": nama, "kontak": kontak, "tanggal": tanggal}
        self.table[index].append(dataPendaki)
        return True
    
    #verifikasi pendaki berdasarkan idTicket untuk memastikan data yang benar saat antri
    def verifikasi_pendaki(self, idTicket):
        index = self._hash(idTicket)
        #cari data dengan idTicket yang sesuai
        for data in self.table[index]:
            if data["id"] == idTicket:
                return data
        return None
    
    def cek_seluruh_id(self):
        #ambil semua idTicket yang terdaftar
        id_list = []
        for bucket in self.table:
            for data in bucket:
                id_list.append(data["id"])
        return id_list