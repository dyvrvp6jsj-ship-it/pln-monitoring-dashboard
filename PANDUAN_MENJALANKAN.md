# ⚡ Panduan Menjalankan Dashboard Realtime Monitoring 910 Sistem Kelistrikan PLN

Aplikasi ini bersifat **portabel, mandiri (zero external dependencies), dan offline-ready**. Seluruh data konsolidasi resmi **910 Sistem Kelistrikan Nasional** (49 Interkoneksi, 645 Isolated dengan pola 24j/12j/6j, dan 216 ULD) dari SharePoint PT PLN 365 tersimpan lengkap di dalam folder ini.

---

## 🚀 Cara 1: Double-Click Langsung di Finder macOS (Paling Mudah)

1. Buka folder ini di **Finder**:
   ```bash
   open /Users/pln/.gemini/antigravity/scratch/pln-monitoring-dashboard
   ```
2. Klik 2x (*double-click*) pada file:
   👉 **`jalankan.command`**
3. Terminal akan terbuka otomatis, server langsung aktif, dan browser (Chrome/Safari) akan otomatis membuka:
   * **http://localhost:8080**

---

## 💻 Cara 2: Menjalankan via Terminal

1. Buka aplikasi **Terminal** di Mac Anda.
2. Jalankan perintah berikut:
   ```bash
   cd /Users/pln/.gemini/antigravity/scratch/pln-monitoring-dashboard
   python3 server.py
   ```
3. Buka browser dan akses **`http://localhost:8080`**.

---

## 🌐 Cara Akses dari Laptop / HP Rekan Kerja di Jaringan Kantor (Wi-Fi / LAN)

Server ini otomatis mendeteksi alamat IP jaringan Anda saat terhubung ke Wi-Fi atau kabel LAN kantor:

1. Saat server berjalan, perhatikan teks yang muncul di Terminal, contoh:
   ```
   PLN REALTIME MONITORING DASHBOARD IS READY & OPEN FOR ACCESS:
     • Localhost: http://localhost:8080
     • Open Network (LAN/Wi-Fi): http://192.168.0.116:8080 (atau http://10.xxx.xxx.xxx:8080)
   ```
2. Anda juga dapat melihat dan menyalin IP LAN langsung dari tombol **🌐 Akses LAN** di header dashboard.
3. Rekan kerja atau pimpinan di ruangan yang sama dapat langsung mengakses dashboard tanpa instalasi apa pun.

---

## 🏝️ Fitur Sistem Isolated & Jam Nyala Operasi

Dashboard kini dilengkapi filter dan tab khusus untuk menavigasi 910 sistem kelistrikan:
- **Filter Jenis Sistem:**
  - ⚡ **Interkoneksi (Grid):** 49 sistem beroperasi 24 jam penuh.
  - 🏝️ **Isolated (Mandiri):** 645 sistem kepulauan dan wilayah 3T.
  - 🏘️ **ULD (Listrik Desa):** 216 sistem elektrifikasi pedesaan.
- **Filter Jam Operasi (Jam Nyala):**
  - ⏱️ **24 Jam:** 537 sistem nasional.
  - 🌙 **12 Jam:** 305 sistem (nyala malam pk 18:00 – 06:00).
  - ⚡ **6 Jam:** 68 sistem (nyala beban puncak pk 18:00 – 24:00).
- **Tab Khusus "Sistem Isolated":**
  - Rincian komprehensif 645 sistem isolated beserta sebaran regional dan pola nyala.
- **Sorotan 57 Sistem Defisit:**
  - Pemantauan real-time sistem-sistem yang mengalami cadangan negatif dengan marker radar berdenyut di peta GIS.
- **Chatbot AI 910 Sistem:**
  - Mampu menjawab pertanyaan teknis & non-teknis tentang sistem apa pun di Indonesia.

---

## 📁 Cara Backup Folder ke Dokumen Anda

Jika ingin menyimpan salinan folder ini di folder **Documents**:
```bash
cp -R /Users/pln/.gemini/antigravity/scratch/pln-monitoring-dashboard ~/Documents/
```

---

## 🔄 Pembaruan Data Excel Besok di Kantor

Jika ada file Excel pembaruan dari SharePoint (Mohammad Anang Fachrudin):
1. Buka dashboard di browser.
2. Klik tombol **"📁 Sumber Data"** di pojok kanan atas.
3. Pada bagian *Unggah File Excel Pembaruan (.xlsx)*, pilih file `.xlsx` terbaru Anda.
4. Dashboard seketika tersinkronisasi dengan 910 sistem terbaru secara presisi!
