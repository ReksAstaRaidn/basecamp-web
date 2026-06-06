import os
import json
import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from structures.HashDataPendaki import Hash
from structures.QueueAntrianPendaki import Queue
from structures.StackRiwayat import Stack

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
DATA_DIR = "data"
HISTORY_DIR = os.path.join(DATA_DIR, "history")
ACTIVE_SESSION_FILE = os.path.join(DATA_DIR, "active_session.json")

# Ensure directories exist
os.makedirs(HISTORY_DIR, exist_ok=True)


data_pendaki_master = Hash(size=1000) 
antrian_pendaki = Queue()
pendaki_di_jalur = [] 

def save_active_session():
    state = {
        "queue": antrian_pendaki.queue,
        "on_trail": pendaki_di_jalur
    }
    with open(ACTIVE_SESSION_FILE, "w") as f:
        json.dump(state, f)
    data_pendaki_master.save_to_json(os.path.join(DATA_DIR, "master_hash.json"))

def load_active_session():
    global pendaki_di_jalur
    if os.path.exists(ACTIVE_SESSION_FILE):
        with open(ACTIVE_SESSION_FILE, "r") as f:
            state = json.load(f)
            antrian_pendaki.queue = state.get("queue", [])
            pendaki_di_jalur = state.get("on_trail", [])
    
    master_hash_path = os.path.join(DATA_DIR, "master_hash.json")
    if os.path.exists(master_hash_path):
        data_pendaki_master.load_from_json(master_hash_path)

load_active_session()

class DataPendakian(BaseModel):
    idTicket: str
    nama: str
    kontak: str
    tanggal: str
    estimasi_jam: int # Durasi pendakian dalam jam

class KuotaPendaki(BaseModel):
    kuota: int

@app.get("/")
def root():
    return {"message": "Welcome to Basecamp API"}

@app.post("/daftar-pendaki")
def daftar_pendakian(data: DataPendakian):
    # Cek duplikat di master hash
    if data_pendaki_master.cek_duplikat_id(data.idTicket):
        return {"status": "gagal", "pesan": f"ID Ticket {data.idTicket} sudah terdaftar"}

    # Tambahkan durasi estimasi ke data
    payload = {
        "id": data.idTicket,
        "nama": data.nama,
        "kontak": data.kontak,
        "tanggal_daftar": data.tanggal,
        "estimasi_jam": data.estimasi_jam,
        "status": "Antrian"
    }
    
    data_pendaki_master.daftar_pendaki(data.idTicket, data.nama, data.kontak, data.tanggal)
    # Update data in hash with extra fields
    index = data_pendaki_master._hash(data.idTicket)
    for d in data_pendaki_master.table[index]:
        if d["id"] == data.idTicket:
            d.update(payload)

    antrian_pendaki.penambahan_pendaki(payload)
    save_active_session()
    
    return {"status": "sukses", "pesan": f"Pendaki {data.nama} berhasil didaftarkan"}

@app.get("/antrian")
def lihat_antrian():
    return {"jumlah": antrian_pendaki.waktu_tunggu(), "pendaki": antrian_pendaki.queue}

@app.post("/kirim-pendaki")
def kirim_pendaki(data: KuotaPendaki):
    now = datetime.datetime.now()
    dikirim = []
    
    for _ in range(data.kuota):
        if antrian_pendaki.is_empty():
            break
        
        pendaki = antrian_pendaki.pengurangan_pendaki()
        pendaki["status"] = "Mendaki"
        pendaki["waktu_berangkat"] = now.strftime("%Y-%m-%d %H:%M")
        
        # Hitung estimasi kembali
        estimasi_kembali = now + datetime.timedelta(hours=pendaki["estimasi_jam"])
        pendaki["estimasi_kembali"] = estimasi_kembali.strftime("%Y-%m-%d %H:%M")
        
        pendaki_di_jalur.append(pendaki)
        dikirim.append(pendaki["nama"])
    
    if not dikirim:
        return {"status": "gagal", "pesan": "Antrian kosong"}
    
    save_active_session()
    return {"status": "sukses", "dikirim": dikirim, "jumlah": len(dikirim)}

@app.get("/mendaki")
def lihat_pendaki_mendaki():
    now = datetime.datetime.now()
    results = []
    for p in pendaki_di_jalur:
        # Check for SOS
        estimasi = datetime.datetime.strptime(p["estimasi_kembali"], "%Y-%m-%d %H:%M")
        p["is_sos"] = now > estimasi
        results.append(p)
    return {"jumlah": len(results), "pendaki": results}

@app.post("/checkout-pendaki/{idTicket}")
def checkout_pendaki(idTicket: str):
    # 1. Cari di jalur (Mendaki)
    found_in_trail_idx = -1
    for i, p in enumerate(pendaki_di_jalur):
        if p["id"] == idTicket:
            found_in_trail_idx = i
            break
            
    if found_in_trail_idx != -1:
        pendaki = pendaki_di_jalur.pop(found_in_trail_idx)
        pendaki["status"] = "Selesai"
        pendaki["waktu_kembali"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    else:
        # 2. Cari di antrian (Batal)
        found_in_queue_idx = -1
        for i, p in enumerate(antrian_pendaki.queue):
            if p["id"] == idTicket:
                found_in_queue_idx = i
                break
        
        if found_in_queue_idx == -1:
            return {"status": "gagal", "pesan": f"Pendaki {idTicket} tidak ditemukan di jalur maupun antrian"}
            
        pendaki = antrian_pendaki.queue.pop(found_in_queue_idx)
        pendaki["status"] = "Dibatalkan"
        pendaki["waktu_berangkat"] = "-" # Tidak pernah berangkat
        pendaki["waktu_kembali"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    # Save to daily history
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    history_file = os.path.join(HISTORY_DIR, f"{today}.json")
    
    history_data = []
    if os.path.exists(history_file):
        with open(history_file, "r") as f:
            history_data = json.load(f)
            
    history_data.append(pendaki)
    with open(history_file, "w") as f:
        json.dump(history_data, f)
        
    save_active_session()
    status_msg = "berhasil checkout" if pendaki["status"] == "Selesai" else "berhasil dibatalkan"
    return {"status": "sukses", "pesan": f"Pendaki {pendaki['nama']} {status_msg}"}

@app.get("/riwayat")
def lihat_riwayat(tanggal: Optional[str] = None):
    if not tanggal:
        tanggal = datetime.datetime.now().strftime("%Y-%m-%d")
    
    history_file = os.path.join(HISTORY_DIR, f"{tanggal}.json")
    if not os.path.exists(history_file):
        return {"jumlah": 0, "riwayat": [], "tanggal": tanggal}
        
    with open(history_file, "r") as f:
        data = json.load(f)
        return {"jumlah": len(data), "riwayat": data, "tanggal": tanggal}

@app.get("/cari-pendaki/{idTicket}")
def cari_pendaki(idTicket: str):
    # Check Active Session first
    for p in antrian_pendaki.queue:
        if p["id"] == idTicket:
            return {"status": "sukses", "data": p, "lokasi": "Antrian"}
    
    for p in pendaki_di_jalur:
        if p["id"] == idTicket:
            return {"status": "sukses", "data": p, "lokasi": "Di Jalur"}
            
    # Check Master Hash (might be in old history)
    hasil = data_pendaki_master.verifikasi_pendaki(idTicket)
    if hasil:
        return {"status": "sukses", "data": hasil, "lokasi": "Arsip/Riwayat"}
        
    return {"status": "gagal", "pesan": "Pendaki tidak ditemukan"}
