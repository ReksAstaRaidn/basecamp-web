# Sistem Manajemen Basecamp Pendakian

Aplikasi web untuk membantu petugas basecamp dalam mengelola pendaftaran pendaki, mengatur antrian keberangkatan, dan melihat riwayat pendaki.

---

## Teknologi yang Digunakan

- **Backend**: Python, FastAPI, Uvicorn
- **Frontend**: HTML, CSS, JavaScript (Vanilla)
- **Struktur Data**: Hash Table, Queue, Stack

---

## Prasyarat

Pastikan perangkat kamu sudah terinstall:

- Python 3.8 atau lebih baru → [Download Python](https://www.python.org/downloads/)
- Git → [Download Git](https://git-scm.com/downloads)

Cek versi Python di terminal:
```bash
python --version
```

---

## Cara Instalasi & Menjalankan Program

### 1. Clone Repositori

```bash
git clone https://github.com/username/nama-repo.git
cd nama-repo
```

### 2. Buat Virtual Environment

```bash
python -m venv venv
```

### 3. Aktifkan Virtual Environment

**Windows (Command Prompt):**
```bash
venv\Scripts\activate
```

**Windows (PowerShell):**
```powershell
venv\Scripts\Activate.ps1
```

> Jika muncul error "running scripts is disabled" di PowerShell, jalankan perintah ini sekali lalu coba lagi:
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```

**Mac/Linux:**
```bash
source venv/bin/activate
```

Jika berhasil, terminal akan menampilkan prefix `(venv)` di awal baris.

### 4. Install Dependencies

```bash
pip install fastapi uvicorn
```

### 5. Jalankan Backend

```bash
uvicorn main:app --reload
```

Jika berhasil, terminal akan menampilkan:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

> Jangan tutup terminal ini selama menggunakan aplikasi.

### 6. Buka Frontend

Masuk ke folder `frontend`, lalu buka file `index.html` langsung di browser dengan cara double-click.

---

## Fitur Aplikasi

| Fitur | Keterangan |
|---|---|
| Daftarkan Pendaki | Registrasi pendaki baru dengan ID Ticket, Nama, dan Kontak Darurat |
| Lihat Antrian | Melihat daftar pendaki yang sedang mengantri |
| Kirim Pendaki | Memberangkatkan pendaki ke jalur sesuai kuota |
| Riwayat Pendaki | Melihat daftar pendaki yang sudah dikirim ke jalur |
| Cari Pendaki | Mencari data pendaki berdasarkan ID Ticket |

---

## Dokumentasi API

Setelah backend berjalan, dokumentasi API interaktif tersedia di:

```
http://localhost:8000/docs
```

---

## Struktur Folder

```
├── main.py                          ← Entry point backend (FastAPI)
├── structures/
│   ├── __init__.py
│   ├── HashDataPendaki.py           ← Hash Table untuk data pendaki
│   ├── QueueAntrianPendaki.py       ← Queue untuk antrian pendaki
│   ├── StackRiwayat.py              ← Stack untuk riwayat pendaki
│   └── GraphJalur.py                ← Graph untuk jalur pendakian
└── frontend/
    ├── index.html
    ├── style.css
    └── app.js
```
