from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
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

dataPendaki = Hash(size=1000)
antrianPendaki = Queue()
riwayatPendaki = Stack()

class DataPendakian(BaseModel):
    idTicket: str
    nama: str
    kontak: str
    tanggal: str
    
class KuotaPendaki(BaseModel):
    kuota: int

@app.get("/")
def root():
    return {"message": "Welcome to Basecamp API"}

@app.post("/daftar-pendaki")
def daftar_pendakian(data: DataPendakian):
    berhasil = dataPendaki.daftar_pendaki(data.idTicket, data.nama, data.kontak, data.tanggal)
    if not berhasil:
        return {"status": "gagal", "message": f"ID Ticket {data.idTicket} sudah terdaftar"}    

    pendaki = dataPendaki.verifikasi_pendaki(data.idTicket)
    antrianPendaki.penambahan_pendaki(pendaki)
    return {"status": "sukses", "message": f"Pendaki {data.nama} berhasil didaftarkan dengan ID Ticket {data.idTicket}"}
    
@app.get("/antrian")
def lihat_antrian():
    return {"jumlah": antrianPendaki.waktu_tunggu(), "pendaki": antrianPendaki.queue, }

@app.post("/kirim-pendaki")
def kirim_pendaki(data: KuotaPendaki):
    dikirim = []
    for _ in range(data.kuota):
        if antrianPendaki.is_empty():
            break
        pendaki = antrianPendaki.pengurangan_pendaki()
        riwayatPendaki.push(pendaki)
        dikirim.append(pendaki["nama"])
    
    if not dikirim:
        return {"status": "gagal", "pesan": "Antrian kosong"}
    
    return {"status": "sukses", "dikirim": dikirim, "jumlah": len(dikirim)}

@app.post("/checkout-pendaki/{idTicket}")
def checkout_pendaki(idTicket: str):
    pendaki = riwayatPendaki.checkout_pendaki(idTicket)
    if not pendaki:
        return {"status": "gagal", "pesan": f"Pendaki dengan ID Ticket {idTicket} tidak ditemukan dalam riwayat"}
    
    return {"status": "sukses", "message": f"Pendaki {pendaki['nama']} dengan ID Ticket {idTicket} berhasil checkout"}

@app.get("/riwayat")
def lihat_riwayat():
    return {"jumlah": riwayatPendaki.size(), "riwayat": riwayatPendaki.stack}

@app.get("/cari-pendaki/{idTicket}")
def cari_pendaki(idTicket: str):
    hasil = dataPendaki.verifikasi_pendaki(idTicket)
    if not hasil:
        return {"status": "gagal", "pesan": "Pendaki tidak ditemukan"}
    return {"status": "sukses", "data": hasil}