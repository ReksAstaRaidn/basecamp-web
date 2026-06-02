const API = "http://localhost:8000"

async function daftarPendaki() {
    const idTicket = document.getElementById("idTicket").value.trim()
    const nama = document.getElementById("nama").value.trim()
    const kontak = document.getElementById("kontak").value.trim()
    const tanggal = document.getElementById("tanggal").value
    const estimasi_jam = parseInt(document.getElementById("estimasi").value)
    const pesan = document.getElementById("pesan-daftar")

    if (!idTicket || !nama || !estimasi_jam) {
        pesan.textContent = "Data tidak lengkap!"
        pesan.className = "pesan gagal"
        return
    }

    const response = await fetch(`${API}/daftar-pendaki`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ idTicket, nama, kontak, tanggal, estimasi_jam })
    })

    const data = await response.json()
    pesan.textContent = data.pesan
    pesan.className = `pesan ${data.status === "sukses" ? "sukses" : "gagal"}`
    if (data.status === "sukses") {
        lihatAntrian()
    }
}

async function lihatAntrian() {
    const response = await fetch(`${API}/antrian`)
    const data = await response.json()

    const list = document.getElementById("list-antrian")
    list.innerHTML = ""
    data.pendaki.forEach(p => {
        const tr = document.createElement("tr")
        tr.innerHTML = `<td>${p.id}</td><td>${p.nama}</td>`
        list.appendChild(tr)
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
    
    if (data.status === "sukses") {
        lihatAntrian()
        lihatMendaki()
    }
}

async function lihatMendaki() {
    const response = await fetch(`${API}/mendaki`)
    const data = await response.json()

    const list = document.getElementById("list-mendaki")
    list.innerHTML = ""
    data.pendaki.forEach(p => {
        const tr = document.createElement("tr")
        if (p.is_sos) tr.className = "sos-alert"
        tr.innerHTML = `
            <td>${p.id}</td>
            <td>${p.nama}</td>
            <td>${p.waktu_berangkat}</td>
            <td>${p.estimasi_kembali}</td>
            <td>${p.is_sos ? "<strong>OVERDUE (SOS)</strong>" : "Normal"}</td>
        `
        list.appendChild(tr)
    })
}

async function checkoutPendaki() {
    const idTicket = document.getElementById("checkout-id").value.trim()
    const pesan = document.getElementById("pesan-checkout")

    const response = await fetch(`${API}/checkout-pendaki/${idTicket}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" }
    })

    const data = await response.json()
    pesan.textContent = data.pesan
    pesan.className = `pesan ${data.status === "sukses" ? "sukses" : "gagal"}`
    
    if (data.status === "sukses") {
        lihatMendaki()
        lihatRiwayat()
    }
}

async function lihatRiwayat() {
    const tgl = document.getElementById("filter-tanggal").value
    const url = tgl ? `${API}/riwayat?tanggal=${tgl}` : `${API}/riwayat`
    
    const response = await fetch(url)
    const data = await response.json()

    const list = document.getElementById("list-riwayat")
    list.innerHTML = ""
    data.riwayat.forEach(p => {
        const tr = document.createElement("tr")
        tr.innerHTML = `
            <td>${p.id}</td>
            <td>${p.nama}</td>
            <td>${p.waktu_berangkat}</td>
            <td>${p.waktu_kembali}</td>
        `
        list.appendChild(tr)
    })
}

async function cariPendaki() {
    const id = document.getElementById("cari-id").value.trim()
    const hasil = document.getElementById("hasil-cari")

    const response = await fetch(`${API}/cari-pendaki/${id}`)
    const data = await response.json()

    if (data.status === "sukses") {
        hasil.textContent = `[${data.lokasi}] ${data.data.nama} (ID: ${data.data.id})`
        hasil.className = "pesan sukses"
    } else {
        hasil.textContent = data.pesan
        hasil.className = "pesan gagal"
    }
}

// Initial loads
window.onload = () => {
    lihatAntrian()
    lihatMendaki()
    lihatRiwayat()
}