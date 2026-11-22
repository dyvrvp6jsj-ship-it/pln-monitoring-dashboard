# Dashboard Realtime Monitoring 910 Sistem Kelistrikan Nasional PLN

Dashboard monitoring eksekutif berbasis web untuk memantau neraca daya dan keandalan operasional **910 Sistem Kelistrikan Nasional PT PLN (Persero)** di seluruh Indonesia secara realtime.

## ⚡ Fitur Utama
1. **Executive Command Center (Japanese Clean Style):**
   - Tampilan bersih, kontras tinggi, bebas visual noise, dan tipografi angka tabular presisi (`tabular-nums`).
   - 4 KPI Utama Nasional: Total 910 Sistem, DMP (MW), Beban Puncak (MW), dan Cadangan Daya (MW) beserta Reserve Margin (%).
2. **Peta Geografis GIS & Anti-Tumpang Tindih:**
   - 62 titik koordinat unik nasional dengan agregasi bubble multi-sistem (radius proporsional akar kuadrat).
   - Indikator prioritas status kelistrikan: Defisit (Merah), Siaga (Kuning), Normal (Hijau), dan Belum Terisi (Abu-abu).
   - Drawer interaktif multi-sistem saat titik bubble diklik.
3. **100% Mobile Responsive (< 768px):**
   - Header ringkas 52px dengan tombol Hamburger Menu.
   - Bilah navigasi bawah (*Bottom Navigation Bar*) untuk akses cepat: KPI, Peta, Defisit, Wilayah, dan AI PLN.
   - Drawer multi-sistem otomatis berubah menjadi *Bottom Sheet* setinggi 72vh.
4. **Fitur "Download Report" (Laporan Eksekutif Direksi):**
   - Format standar A4 Portrait resmi bergaya McKinsey/BCG, tepat 3 halaman padat tanpa halaman kosong meluber:
     - **Halaman 1:** Executive Summary, 4 KPI, Peta Vektor Presisi Kepulauan Indonesia, dan Callout 7 Wilayah.
     - **Halaman 2:** Analitik Komparasi Regional DMP vs BP, Stacked Bar Jam Nyala (24j/12j/6j), Status Kelistrikan, dan Catatan Strategis.
     - **Halaman 3:** Matriks Konsolidasi Neraca Daya 35 Provinsi dan 3 Kategori Aksi Korporat.
   - Opsi lampiran matriks 910 sistem yang dapat diaktifkan kapan saja melalui checkbox `[ ] +Lampiran 910 Sistem (Opsional)`.
5. **Asisten AI PLN:**
   - Chatbot konsultasi cerdas terintegrasi untuk analisis neraca daya dan kondisi kelistrikan regional.

---

## 🚀 Cara Menjalankan

### Persyaratan:
- Python 3.8 atau yang lebih baru.
- Tanpa dependensi eksternal berat (menggunakan pustaka bawaan Python: `http.server`, `socketserver`, `zipfile`, `xml.etree`).

### Menjalankan Server:
```bash
python3 server.py
```
atau di macOS cukup klik dua kali file:
```bash
1_JALANKAN_DASHBOARD.command
```

### Akses Aplikasi:
- **Komputer Lokal:** Buka browser di [http://localhost:8080](http://localhost:8080)
- **Akses Jaringan Lokal (HP / Laptop Lain):** Buka `http://<IP-LAN>:8080` (misal: `http://192.168.0.118:8080`)

---

## 📁 Struktur Direktori
```text
├── server.py                   # HTTP & WebSocket Backend Server (Port 8080)
├── parser.py                   # Data extraction, normalization, & geocoding 910 sistem
├── chatbot.py                  # Mesin konsultasi AI PLN
├── data/
│   └── sumber_data_pln.xlsx    # Database sumber monitoring 910 sistem PLN
├── public/
│   ├── index.html              # Frontend dashboard & responsive command center
│   ├── report_preview.html     # Pratinjau dokumen cetak eksekutif A4 Portrait
│   ├── indonesia_map_paths.js  # Peta vektor SVG kepulauan Indonesia presisi
│   ├── logo_pln.png            # Aset resmi logo PLN
│   └── leaflet/                # Modul Leaflet GIS offline
└── 1_JALANKAN_DASHBOARD.command # Shortcut peluncuran satu-klik di macOS
```
