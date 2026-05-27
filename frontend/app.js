const API = "http://localhost:8000"

async function daftarPendaki() {
    const idTicket = document.getElementById("idTicket").value.trim()
    const nama = document.getElementById("nama").value.trim()
    const kontak = document.getElementById("kontak").value.trim()
    const pesan = document.getElementById("pesan-daftar")

    const response = await fetch(`${API}/daftar-pendaki`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ idTicket, nama, kontak })
    })

    const data = await response.json()
    pesan.textContent = data.pesan
    pesan.className = `pesan ${data.status === "sukses" ? "sukses" : "gagal"}`
}

async function lihatAntrian() {
    const response = await fetch(`${API}/antrian`)
    const data = await response.json()

    document.getElementById("jumlah-antrian").textContent = `Total: ${data.jumlah} pendaki`

    const list = document.getElementById("list-antrian")
    list.innerHTML = ""
    data.pendaki.forEach(p => {
        const li = document.createElement("li")
        li.textContent = `${p.id} — ${p.nama} (${p.kontak})`
        list.appendChild(li)
    })
}

async function kirimPendaki() {
    const kuota = parseInt(document.getElementById("kuota").value)
    const pesan = document.getElementById("pesan-kirim")

    const response = await fetch(`${API}/kirim-pendaki`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ kuota })
    })

    const data = await response.json()
    pesan.textContent = data.status === "sukses"
        ? `Berhasil mengirim: ${data.dikirim.join(", ")}`
        : data.pesan
    pesan.className = `pesan ${data.status === "sukses" ? "sukses" : "gagal"}`
}

async function lihatRiwayat() {
    const response = await fetch(`${API}/riwayat`)
    const data = await response.json()

    const list = document.getElementById("list-riwayat")
    list.innerHTML = ""
    data.riwayat.forEach(p => {
        const li = document.createElement("li")
        li.textContent = `${p.id} — ${p.nama} (${p.kontak})`
        list.appendChild(li)
    })
}

async function cariPendaki() {
    const id = document.getElementById("cari-id").value.trim()
    const hasil = document.getElementById("hasil-cari")

    const response = await fetch(`${API}/cari-pendaki/${id}`)
    const data = await response.json()

    if (data.status === "sukses") {
        hasil.textContent = `Ditemukan: ${data.data.nama}, Kontak: ${data.data.kontak}`
        hasil.className = "pesan sukses"
    } else {
        hasil.textContent = data.pesan
        hasil.className = "pesan gagal"
    }
}