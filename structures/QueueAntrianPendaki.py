import json
import os

class Queue:
    def __init__(self):
        self.queue = []
        
    def save_to_json(self, filename):
        with open(filename, 'w') as f:
            json.dump(self.queue, f)

    def load_from_json(self, filename):
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                self.queue = json.load(f)

    def penambahan_pendaki(self, idTicket):
        self.queue.append(idTicket)
        
    def pengurangan_pendaki(self):
        # pastikan antrian tidak kosong sebelum mengurangi pendaki
        if not self.is_empty():
            pendaki_keluar = self.queue.pop(0) # ambil pendaki paling depan dari antrian
            return pendaki_keluar # kembalikan ID pendaki yang keluar
        return None
    
    def is_empty(self):
        return len(self.queue) == 0 # cek apakah antrian kosong
    
    def waktu_tunggu(self):
        return len(self.queue) # hitung jumlah pendaki dalam antrian untuk estimasi waktu tunggu