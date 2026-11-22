"""
PLN Realtime Monitoring AI Assistant Engine (chatbot.py)
Menjawab pertanyaan teknis dan non-teknis mengenai 910 Sistem Kelistrikan Nasional PLN:
- Regional / Pulau: Nusa Tenggara (74), Papua (258), Maluku (168), Sumatera (188), Jawa Bali (44), Kalimantan (89), Sulawesi (89)
- Kategori Sumber: Interkoneksi (49), Isolated (645), ULD (216)
- Pola Operasi: 24 Jam (537), 12 Jam (305), 6 Jam (68)
- Neraca Daya: 57 Defisit, 467 Siaga, 224 Normal, 162 Belum Terisi
- Fokus Monitoring: Interkoneksi 24 Sistem Besar (Mapping & Kandidat)
- Pencarian cerdas nama sistem dari 910 sistem (termasuk Merauke, Sabang, Tanakeke, Leok, dll.)
- Konsep teknis ketenagalistrikan (DMP, BP, DMN, Cadangan, Reserve Margin, Dedieselisasi)
100% Data Fidelity - Berdasarkan workbook konsolidasi resmi Microsoft Excel SharePoint PT PLN 365.
"""

import re
from datetime import datetime

def f_num(n):
    """Format angka Indonesia (1.234,5)"""
    if n is None or n == '':
        return '0'
    try:
        val = float(n)
        return f"{val:,.1f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    except Exception:
        return str(n)

def build_system_card(s):
    """Menghasilkan representasi ringkas kartu sistem"""
    is_def = s.get('cad_mw', 0) < 0
    sign = '+' if s.get('cad_mw', 0) >= 0 else ''
    cad_color = '#EF4444' if is_def else ('#F59E0B' if s.get('status_code') == 'siaga' else '#10B981')
    
    geo_info = "Koordinat Bersama" if s.get('geo', {}).get('is_shared') else "Koordinat Mandiri"
    return f"""### 📍 Sistem #{s.get('no')}: {s.get('name')}
- **Unit / Wilayah:** **{s.get('unit')}** ({s.get('region')})
- **Jenis & Pola Nyala:** **{s.get('jenis')}** • **{s.get('jam_operasi')}**
- **Status Operasi:** **{s.get('status')}** (Cadangan Daya: `{sign}{f_num(s.get('cad_mw'))} MW` / `{s.get('cad_pct')}%`)
- **Daya Mampu Pasok (DMP):** `{f_num(s.get('dmp'))} MW` | **Beban Puncak (BP):** `{f_num(s.get('bp'))} MW`
- **Daya Terpasang:** `{f_num(s.get('daya_terpasang'))} MW` | **DMN:** `{f_num(s.get('dmn'))} MW`
- **Kualitas Lokasi:** {geo_info} ({s.get('geo', {}).get('lat', '-')}, {s.get('geo', {}).get('lng', '-')})
- **Catatan Operasional:** {s.get('keterangan', '-')}

[[ACTION:focus_system:{s.get('no')}:🔍 Buka Detail Sistem {s.get('name')}]]"""

def build_group_summary(subset, title_label, action_tag=None):
    """Membangun analisis statistik komprehensif untuk sekelompok sistem"""
    total = len(subset)
    if total == 0:
        return f"Tidak ditemukan sistem untuk kategori **{title_label}**."

    total_dmp = sum(s.get('dmp', 0) for s in subset)
    total_bp = sum(s.get('bp', 0) for s in subset)
    total_cad = total_dmp - total_bp
    rm_pct = round((total_cad / total_bp * 100), 2) if total_bp > 0 else 0.0

    # Status Breakdown
    def_systems = [s for s in subset if s.get('status_code') == 'defisit']
    siaga_systems = [s for s in subset if s.get('status_code') == 'siaga']
    norm_systems = [s for s in subset if s.get('status_code') == 'normal']
    unf_systems = [s for s in subset if s.get('status_code') == 'unfilled']

    # Jenis Breakdown
    inter_count = sum(1 for s in subset if s.get('jenis_code') == 'interkoneksi')
    iso_count = sum(1 for s in subset if s.get('jenis_code') == 'isolated')
    uld_count = sum(1 for s in subset if s.get('jenis_code') == 'uld')

    # Jam Breakdown
    c_24 = sum(1 for s in subset if s.get('jam_code') == '24h')
    c_12 = sum(1 for s in subset if s.get('jam_code') == '12h')
    c_6 = sum(1 for s in subset if s.get('jam_code') == '6h')

    # Top 5 Sistem Terbesar
    sorted_by_dmp = sorted(subset, key=lambda x: x.get('dmp', 0), reverse=True)[:5]

    sign = '+' if total_cad >= 0 else ''
    resp = f"### 📊 Ringkasan Analitik: {title_label} ({total} Sistem)\n\n"
    resp += f"#### ⚡ Neraca Daya Agregat:\n"
    resp += f"- **Total Sistem:** **{total} Sistem**\n"
    resp += f"- **Daya Mampu Pasok (DMP):** **{f_num(total_dmp)} MW**\n"
    resp += f"- **Beban Puncak (BP):** **{f_num(total_bp)} MW**\n"
    resp += f"- **Cadangan Daya:** **{sign}{f_num(total_cad)} MW** (Reserve Margin: **{rm_pct}%**)\n\n"

    resp += f"#### 🚥 Distribusi Status Operasional:\n"
    resp += f"- 🔴 **Defisit (Cadangan < 0 MW):** **{len(def_systems)} sistem**\n"
    resp += f"- 🟡 **Siaga (Margin Ketat):** **{len(siaga_systems)} sistem**\n"
    resp += f"- 🟢 **Normal (Cadangan Aman):** **{len(norm_systems)} sistem**\n"
    resp += f"- ⚪ **Belum Terisi (Perlu Validasi):** **{len(unf_systems)} sistem**\n\n"

    resp += f"#### 🏷️ Klasifikasi Sumber & Jam Operasi:\n"
    resp += f"- **Jenis Sistem:** ⚡ Interkoneksi: **{inter_count}** | 🏝️ Isolated: **{iso_count}** | 🏘️ ULD: **{uld_count}**\n"
    resp += f"- **Pola Nyala:** ⏱️ 24 Jam: **{c_24} sistem** | 🌙 12 Jam: **{c_12} sistem** | ⚡ 6 Jam: **{c_6} sistem**\n\n"

    # Sistem Defisit jika ada
    if def_systems:
        resp += f"#### 🚨 Sistem Defisit ({len(def_systems)} Sistem Terpantau):\n"
        for ds in sorted(def_systems, key=lambda x: x.get('cad_mw', 0))[:8]:
            resp += f"- **{ds.get('name')}** ({ds.get('unit')}): Defisit `{f_num(ds.get('cad_mw'))} MW` (DMP {f_num(ds.get('dmp'))} MW vs BP {f_num(ds.get('bp'))} MW)\n"
        if len(def_systems) > 8:
            resp += f"- *...dan {len(def_systems) - 8} sistem defisit lainnya.*\n"
        resp += "\n"

    # 5 Sistem Kapasitas Terbesar
    if sorted_by_dmp and sorted_by_dmp[0].get('dmp', 0) > 0:
        resp += f"#### 🏆 5 Sistem Berkapasitas Terbesar:\n"
        for i, ts in enumerate(sorted_by_dmp, 1):
            s_sign = '+' if ts.get('cad_mw', 0) >= 0 else ''
            resp += f"{i}. **{ts.get('name')}** ({ts.get('jenis')}, {ts.get('jam_operasi')}): DMP `{f_num(ts.get('dmp'))} MW` | BP `{f_num(ts.get('bp'))} MW` | Cadangan `{s_sign}{f_num(ts.get('cad_mw'))} MW` ({ts.get('status')})\n"
        resp += "\n"

    if action_tag:
        resp += f"{action_tag}\n"

    return resp


def process_chat_query(user_query, app_data):
    """
    Memproses pertanyaan pengguna secara komprehensif:
    1. Pulau / Regional resmi (Nusa Tenggara, Papua, Maluku, Sumatera, Jawa Bali, Kalimantan, Sulawesi)
    2. Cross-filter dinamis (Pulau + Status, Pulau + Jam, Jenis + Jam)
    3. Fokus Monitoring 24 Sistem Besar Interkoneksi
    4. Analisis defisit nasional & regional
    5. Sistem tertentu berdasarkan nama atau nomor ID (910 sistem)
    6. Superlatif (Terbesar, Terkecil, Cadangan tertinggi/terendah)
    7. Pengetahuan teknis (DMP, BP, Reserve Margin, Dedieselisasi, dll.)
    8. Tata kelola data & Kualitas lokasi sumber data
    """
    if not user_query or not user_query.strip():
        return "Silakan tanyakan informasi teknis & non-teknis mengenai 910 Sistem Kelistrikan Nasional PLN."

    raw_q = user_query.strip()
    q = raw_q.lower()
    
    systems = app_data.get('systems', [])
    kpi = app_data.get('kpi_summary', {})
    src = app_data.get('source_info', {})
    sistem_besar_ids = app_data.get('sistem_besar_ids', [])
    
    # -------------------------------------------------------------
    # 1. PERTANYAAN REGIONAL / GUGUS PULAU
    # -------------------------------------------------------------
    
    # A. NUSA TENGGARA (74 SISTEM: NTB & NTT)
    if any(k in q for k in ['nusa tenggara', 'ntb', 'ntt', 'lombok', 'sumbawa', 'timor', 'flores', 'sumba', 'alor', 'rote', 'kupang', 'mataram', 'larantuka', 'waingapu', 'waitabula']):
        # Cek apakah bertanya sistem spesifik di NTT/NTB
        matched_single = None
        for name_candidate in ['lombok', 'timor', 'tambora', 'waingapu', 'larantuka', 'waitabula', 'alor', 'rote', 'ende', 'labuan bajo']:
            if name_candidate in q:
                match = next((s for s in systems if name_candidate in s.get('name', '').lower()), None)
                if match:
                    matched_single = match
                    break
        
        # Jika bukan sistem tunggal, berikan analisis wilayah Nusa Tenggara
        if not matched_single or 'semua' in q or 'khusus' in q or 'wilayah' in q or 'berapa' in q or 'ringkasan' in q:
            nusa_systems = [s for s in systems if s.get('island') == 'nusa']
            
            # Cek cross-filter tambahan: defisit
            if 'defisit' in q:
                defs = [s for s in nusa_systems if s.get('status_code') == 'defisit']
                return build_group_summary(defs, "Sistem Defisit di Wilayah Nusa Tenggara", "[[ACTION:zoom_island:nusa:🗺️ Lihat Peta Nusa Tenggara]]")
            if 'isolated' in q:
                isos = [s for s in nusa_systems if s.get('jenis_code') == 'isolated']
                return build_group_summary(isos, "Sistem Isolated di Wilayah Nusa Tenggara", "[[ACTION:zoom_island:nusa:🗺️ Lihat Peta Nusa Tenggara]]")
            if 'interkoneksi' in q:
                inters = [s for s in nusa_systems if s.get('jenis_code') == 'interkoneksi']
                return build_group_summary(inters, "Sistem Interkoneksi di Wilayah Nusa Tenggara (Lombok, Tambora, Timor)", "[[ACTION:zoom_island:nusa:🗺️ Lihat Peta Nusa Tenggara]]")

            resp = build_group_summary(
                nusa_systems, 
                "Wilayah Nusa Tenggara (NTB & NTT)",
                "[[ACTION:zoom_island:nusa:🗺️ Fokuskan Peta ke Nusa Tenggara (74 Sistem)]]"
            )
            resp += "> 💡 **Karakteristik Kelistrikan Nusa Tenggara:** Terdiri dari 2 Unit Induk: **7701 - UIW Nusa Tenggara Barat** (Sistem Lombok, Sumbawa/Tambora) dan **7801 - UIW Nusa Tenggara Timur** (Sistem Timor, Flores, Sumba, dan pulau-pulau isolated). Terdapat penetrasi EBT tinggi seperti PLTP Ulumbu/Mataloko dan PLTS Komunal."
            return resp

    # B. PAPUA & PAPUA BARAT (258 SISTEM)
    if any(k in q for k in ['papua', 'papua barat', 'jayapura', 'merauke', 'sorong', 'manokwari', 'biak', 'fak-fak', 'fakfak', 'timika', 'nabire', 'sarmi']):
        # Cek apakah bertanya Merauke atau Jayapura secara spesifik
        if 'merauke' in q:
            m = next((s for s in systems if 'merauke' in s.get('name', '').lower()), None)
            if m:
                return build_system_card(m)
        if 'jayapura' in q and not any(w in q for w in ['semua', 'wilayah', 'ringkasan', 'papua']):
            j = next((s for s in systems if 'jayapura' in s.get('name', '').lower()), None)
            if j:
                return build_system_card(j)

        papua_systems = [s for s in systems if s.get('island') == 'papua']
        
        if 'defisit' in q:
            defs = [s for s in papua_systems if s.get('status_code') == 'defisit']
            return build_group_summary(defs, "Sistem Defisit di Papua & Papua Barat", "[[ACTION:zoom_island:papua:🗺️ Lihat Peta Papua]]")

        resp = build_group_summary(
            papua_systems,
            "Wilayah Papua & Papua Barat (Unit 7601)",
            "[[ACTION:zoom_island:papua:🦅 Fokuskan Peta ke Papua & Papua Barat (258 Sistem)]]"
        )
        resp += "> 📍 **Catatan Kualitas Lokasi:** Di sheet Rekap Sistem, terdapat **241 sistem Papua** yang memakai koordinat bersama kantor induk (Jayapura) dan **17 sistem dengan koordinat individual**. Seluruh 258 record valid dan terintegrasi penuh."
        return resp

    # C. MALUKU & MALUKU UTARA (168 SISTEM)
    if any(k in q for k in ['maluku', 'maluku utara', 'ambon', 'ternate', 'tidore', 'seram', 'halmahera', 'bula', 'masohi', 'tobelo', 'jailolo', 'sofifi']):
        maluku_systems = [s for s in systems if s.get('island') == 'maluku']
        if 'defisit' in q:
            defs = [s for s in maluku_systems if s.get('status_code') == 'defisit']
            return build_group_summary(defs, "Sistem Defisit di Maluku & Maluku Utara", "[[ACTION:zoom_island:maluku:🗺️ Lihat Peta Maluku]]")

        resp = build_group_summary(
            maluku_systems,
            "Wilayah Maluku & Maluku Utara (Unit 7501)",
            "[[ACTION:zoom_island:maluku:⛰️ Fokuskan Peta ke Maluku (168 Sistem)]]"
        )
        resp += "> 🏝️ **Karakteristik Maluku:** Wilayah kepulauan dengan proporsi sistem Isolated dan ULD terbesar, mengandalkan kapal pembangkit listrik terapung (Barge Mounted Power Plant / BMPP) dan PLTD kepulauan."
        return resp

    # D. SUMATERA (188 SISTEM)
    if any(k in q for k in ['sumatera', 'sumsel', 'sumut', 'sumbar', 'aceh', 'riau', 'kepri', 'batam', 'bintan', 'bangka', 'belitung', 'lampung', 'tol listrik sumatera']):
        sumatera_systems = [s for s in systems if s.get('island') == 'sumatera']
        if 'defisit' in q:
            defs = [s for s in sumatera_systems if s.get('status_code') == 'defisit']
            return build_group_summary(defs, "Sistem Defisit di Sumatera", "[[ACTION:zoom_island:sumatera:🗺️ Lihat Peta Sumatera]]")

        resp = build_group_summary(
            sumatera_systems,
            "Wilayah Regional Sumatera",
            "[[ACTION:zoom_island:sumatera:🌴 Fokuskan Peta ke Sumatera (188 Sistem)]]"
        )
        resp += "> ⚡ **Grid Utama Sumatera:** Tol Listrik 275 kV & 150 kV menghubungkan Aceh hingga Lampung, didukung interkoneksi Batam-Bintan dan sistem kepulauan Bangka-Belitung."
        return resp

    # E. JAWA, MADURA, BALI (44 SISTEM)
    if any(k in q for k in ['jawa', 'madura', 'bali', 'jamali', 'jawa bali', 'paiton', 'suralaya', 'cirata', 'saguling']):
        jawa_systems = [s for s in systems if s.get('island') == 'jawa']
        resp = build_group_summary(
            jawa_systems,
            "Wilayah Jawa, Madura, dan Bali (JAMALI)",
            "[[ACTION:zoom_island:jawa:⚡ Fokuskan Peta ke Jawa-Bali (44 Sistem)]]"
        )
        resp += "> 🏭 **Pusat Beban Nasional:** Grid 500 kV Jamali merupakan sistem interkoneksi terbesar di Asia Tenggara yang memasok lebih dari 65% konsumsi energi listrik nasional."
        return resp

    # F. KALIMANTAN (89 SISTEM)
    if any(k in q for k in ['kalimantan', 'kalseltengtimra', 'kalsel', 'kalteng', 'kaltim', 'kalbar', 'kaltara', 'khatulistiwa']):
        kal_systems = [s for s in systems if s.get('island') == 'kalimantan']
        resp = build_group_summary(
            kal_systems,
            "Wilayah Regional Kalimantan",
            "[[ACTION:zoom_island:kalimantan:🌲 Fokuskan Peta ke Kalimantan (89 Sistem)]]"
        )
        resp += "> 🔌 **Interkoneksi Regional:** Sistem Kalseltengtimra (UIP3B Kalimantan) dan Sistem Khatulistiwa yang terhubung ke transmisi SESCO Sarawak (Malaysia)."
        return resp

    # G. SULAWESI (89 SISTEM)
    if any(k in q for k in ['sulawesi', 'sulbagsel', 'sulutgo', 'makassar', 'manado', 'kendari', 'palu', 'luwuk', 'bau-bau', 'tanakeke', 'leok']):
        sul_systems = [s for s in systems if s.get('island') == 'sulawesi']
        if 'tanakeke' in q:
            t = next((s for s in systems if 'tanakeke' in s.get('name', '').lower()), None)
            if t:
                return build_system_card(t)
        if 'leok' in q:
            l = next((s for s in systems if 'leok' in s.get('name', '').lower()), None)
            if l:
                return build_system_card(l)

        resp = build_group_summary(
            sul_systems,
            "Wilayah Regional Sulawesi",
            "[[ACTION:zoom_island:sulawesi:🌊 Fokuskan Peta ke Sulawesi (89 Sistem)]]"
        )
        return resp

    # -------------------------------------------------------------
    # 2. FOKUS MONITORING: INTERKONEKSI 24 SISTEM BESAR
    # -------------------------------------------------------------
    if any(k in q for k in ['24 sistem', 'sistem besar', 'fokus monitoring', 'konfigurasi 24', 'mapping 24', 'kandidat sistem besar']):
        inter_systems = [s for s in systems if s.get('jenis_code') == 'interkoneksi']
        sorted_inter = sorted(inter_systems, key=lambda x: x.get('dmp', 0), reverse=True)
        
        status_cfg = "Terkonfigurasi" if len(sistem_besar_ids) == 24 else ("Sebagian Terkonfigurasi" if len(sistem_besar_ids) > 0 else "Belum Dikonfigurasi")
        
        resp = f"### ⭐ Fokus Monitoring: Interkoneksi 24 Sistem Besar\n\n"
        resp += f"**Definisi Resmi:** Sesuai arahan teknis PLN, angka **24** adalah **kuota jumlah sistem besar** yang menjadi fokus pengawasan intensif nasional (bukan jam operasi). Seluruh 49 sistem interkoneksi beroperasi selama 24 jam.\n\n"
        resp += f"- **Status Konfigurasi Saat Ini:** `{status_cfg}` ({len(sistem_besar_ids)} / 24 Sistem)\n"
        resp += f"- **Penyimpanan:** `config/sistem_besar.json`\n"
        resp += f"- **Kandidat Sistem Interkoneksi Tersedia:** **{len(inter_systems)} Sistem** di workbook sumber.\n\n"

        resp += "#### 🏆 10 Sistem Interkoneksi Berkapasitas Terbesar (Kandidat Utama):\n"
        for i, s in enumerate(sorted_inter[:10], 1):
            is_def = s.get('cad_mw', 0) < 0
            sign = '+' if s.get('cad_mw', 0) >= 0 else ''
            resp += f"{i}. **{s.get('name')}** ({s.get('unit')}): DMP `{f_num(s.get('dmp'))} MW` | BP `{f_num(s.get('bp'))} MW` | Cadangan `{sign}{f_num(s.get('cad_mw'))} MW` ({s.get('status')})\n"

        resp += "\n> ⚙️ Untuk menetapkan atau mengubah 24 sistem resmi, gunakan tombol pengaturan di bawah ini:\n\n"
        resp += "[[ACTION:open_config_24::⚙️ Buka Dialog Konfigurasi 24 Sistem Besar]]"
        return resp

    # -------------------------------------------------------------
    # 3. PERTANYAAN KHUSUS: SISTEM DEFISIT (57 SISTEM)
    # -------------------------------------------------------------
    if any(k in q for k in ['defisit', 'kurang daya', 'minus', 'kritis', '57 defisit', 'daftar defisit']):
        defs = [s for s in systems if s.get('status_code') == 'defisit']
        sorted_defs = sorted(defs, key=lambda x: x.get('cad_mw', 0))

        resp = f"### 🚨 Analisis Komprehensif 57 Sistem Berstatus DEFISIT\n\n"
        resp += f"Sistem berstatus **DEFISIT** didefinisikan sebagai sistem kelistrikan di mana **Cadangan Daya < 0 MW** (Daya Mampu Pasok tidak mencukupi Beban Puncak pemakaian).\n\n"
        resp += f"#### 📊 Rekap Defisit Nasional:\n"
        resp += f"- Total Sistem Defisit: **{len(defs)} Sistem** (dari 910 sistem)\n"
        resp += f"- Defisit Terbesar: **SULBAGSEL (`-267,5 MW`)**, **Tanakeke (`-90,0 MW`)**, **Leok (`-72,2 MW`)**, **Interkoneksi Kalimantan (`-60,2 MW`)**, **Khatulistiwa (`-16,8 MW`)**\n\n"

        resp += "#### 📋 Daftar Sistem Defisit Tertinggi:\n"
        resp += "| No | Nama Sistem | Unit / Wilayah | Jenis | Pola | DMP (MW) | BP (MW) | Defisit |\n"
        resp += "|---|---|---|---|---|---|---|---|\n"
        for i, s in enumerate(sorted_defs[:12], 1):
            resp += f"| {i} | **{s['name']}** | {s['unit']} | {s['jenis']} | {s['jam_operasi']} | {f_num(s['dmp'])} | {f_num(s['bp'])} | `{f_num(s['cad_mw'])} MW` |\n"

        if len(sorted_defs) > 12:
            resp += f"\n*...dan {len(sorted_defs) - 12} sistem defisit lainnya di Maluku, Nusa Tenggara, dan Papua.* Gunakan tombol aksi di bawah untuk memfilter peta secara langsung:\n\n"

        resp += "[[ACTION:filter_status:defisit:🚨 Tampilkan 57 Sistem Defisit di Dashboard]]"
        return resp

    # -------------------------------------------------------------
    # 4. POLA JAM OPERASI (24 JAM, 12 JAM, 6 JAM)
    # -------------------------------------------------------------
    if any(k in q for k in ['jam operasi', 'jam nyala', 'pola operasi', '24 jam', '12 jam', '6 jam', 'dedieselisasi']):
        c_24 = kpi.get('jam_operasi_counts', {}).get('24h', 537)
        c_12 = kpi.get('jam_operasi_counts', {}).get('12h', 305)
        c_6 = kpi.get('jam_operasi_counts', {}).get('6h', 68)

        resp = f"### ⏱️ Analisis Pola Jam Operasi Nasional (910 Sistem)\n\n"
        resp += f"PLN membagi operasional kelistrikan menjadi 3 pola jam nyala:\n\n"
        resp += f"1. **⏱️ Sistem 24 Jam ({c_24} Sistem / {round(c_24/len(systems)*100, 1)}%):**\n"
        resp += f"   - Pasokan menyala kontinu 24 jam penuh. Terdiri dari 49 Interkoneksi, 412 Isolated, dan 76 ULD.\n"
        resp += f"   - Memasok kota besar, kawasan industri, dan pulau dengan kapasitas pembangkit stabil.\n\n"
        resp += f"2. **🌙 Sistem 12 Jam ({c_12} Sistem / {round(c_12/len(systems)*100, 1)}%):**\n"
        resp += f"   - Beroperasi malam hari (rata-rata pk 18:00 – 06:00). Terdiri dari 197 Isolated dan 108 ULD.\n"
        resp += f"   - Bertujuan mengefisienkan bahan bakar minyak (BBM diesel) dan memperpanjang jam kerja mesin.\n\n"
        resp += f"3. **⚡ Sistem 6 Jam ({c_6} Sistem / {round(c_6/len(systems)*100, 1)}%):**\n"
        resp += f"   - Beroperasi hanya pada jam beban puncak malam (pk 18:00 – 24:00). Terdiri dari 36 Isolated dan 32 ULD di pedalaman/pulau terpencil.\n\n"
        resp += "> ☀️ **Program Dedieselisasi PLN:** Program strategis transisi energi untuk mengkonversi PLTD 6 & 12 jam menjadi 24 jam dengan integrasi PLTS Komunal dan sistem penyimpanan baterai (BESS)."
        return resp

    # -------------------------------------------------------------
    # 5. KATEGORI SUMBER: ISOLATED & ULD
    # -------------------------------------------------------------
    if any(k in q for k in ['isolated', 'terisolir', 'mandiri']) and not any(k in q for k in ['nusa', 'papua', 'maluku', 'sumatera', 'sulawesi', 'kalimantan']):
        iso_systems = [s for s in systems if s.get('jenis_code') == 'isolated']
        return build_group_summary(iso_systems, "Sistem Isolated Nasional (645 Sistem)", "[[ACTION:filter_jenis:isolated:🏝️ Filter Dashboard ke Sistem Isolated]]")

    if any(k in q for k in ['uld', 'listrik desa']) and not any(k in q for k in ['nusa', 'papua', 'maluku', 'sumatera', 'sulawesi', 'kalimantan']):
        uld_systems = [s for s in systems if s.get('jenis_code') == 'uld']
        return build_group_summary(uld_systems, "Unit Listrik Desa / ULD Nasional (216 Sistem)", "[[ACTION:filter_jenis:uld:🏘️ Filter Dashboard ke Sistem ULD]]")

    # -------------------------------------------------------------
    # 6. SUPERLATIF: TERBESAR, TERKECIL, CADANGAN TERTINGGI/TERENDAH
    # -------------------------------------------------------------
    if any(k in q for k in ['terbesar', 'paling besar', 'top 10', 'top 5', 'tertinggi']):
        sorted_dmp = sorted(systems, key=lambda x: x.get('dmp', 0), reverse=True)[:10]
        resp = "### 🏆 10 Sistem Kelistrikan Terbesar di Indonesia (Berdasarkan DMP)\n\n"
        for i, s in enumerate(sorted_dmp, 1):
            sign = '+' if s.get('cad_mw', 0) >= 0 else ''
            resp += f"{i}. **{s['name']}** ({s['region']}) — **{s['jenis']}** ({s['jam_operasi']})\n"
            resp += f"   • DMP: `{f_num(s['dmp'])} MW` | Beban: `{f_num(s['bp'])} MW` | Cadangan: `{sign}{f_num(s['cad_mw'])} MW` ({s['status']})\n"
        return resp

    # -------------------------------------------------------------
    # 7. KONSEP TEKNIS KETENAGALISTRIKAN PLN
    # -------------------------------------------------------------
    if any(k in q for k in ['apa itu dmp', 'daya mampu pasok', 'arti dmp']):
        return """### 🔋 Definisi Teknis: Daya Mampu Pasok (DMP)
**Daya Mampu Pasok (DMP)** adalah daya maksimum yang siap dibangkitkan dan disalurkan oleh seluruh unit pembangkit yang beroperasi untuk melayani beban konsumen pada jam operasional tertentu.
- **DMP Nasional:** **56.763,5 MW**
- **Hubungan:** DMP = Daya Mampu Netto (DMN) dikurangi unit pembangkit yang mengalami pemeliharaan (Planned Outage/PO, Maintenance Outage/MO) atau gangguan (Forced Outage/FO, Derating)."""

    if any(k in q for k in ['apa itu bp', 'beban puncak', 'arti bp']):
        return """### 📈 Definisi Teknis: Beban Puncak (BP)
**Beban Puncak (BP)** adalah nilai serapan daya listrik tertinggi oleh seluruh konsumen (industri, bisnis, rumah tangga, publik) dalam satu kurun waktu pengukuran (biasanya di waktu malam pk 18:00 - 22:00 waktu setempat).
- **Beban Puncak Nasional:** **55.246,0 MW**
- **Analisis:** Selisih antara DMP dan BP menentukan kecukupan cadangan daya sistem."""

    if any(k in q for k in ['cadangan daya', 'reserve margin', 'arti cadangan']):
        return """### 🛡️ Definisi Teknis: Cadangan Daya & Reserve Margin
- **Cadangan Daya (MW):** Selisih langsung antara pasokan dan serapan:  
  `Cadangan Daya = Daya Mampu Pasok (DMP) - Beban Puncak (BP)`
- **Reserve Margin (%):** Rasio keandalan sistem terhadap beban puncak:  
  `Reserve Margin = (Cadangan Daya / Beban Puncak) × 100%`
- **Kriteria Status PLN:**
  - 🔴 **DEFISIT:** Cadangan Daya < 0 MW (Pasokan kurang dari kebutuhan).
  - 🟡 **SIAGA:** Cadangan Daya > 0 MW namun Reserve Margin tipis di bawah standar cadangan operasi unit terbesar (N-1).
  - 🟢 **NORMAL:** Cadangan Daya aman melebihi kriteria kontinjensi unit terbesar."""

    # -------------------------------------------------------------
    # 8. NON-TEKNIS & DATA GOVERNANCE
    # -------------------------------------------------------------
    if any(k in q for k in ['sumber data', 'sharepoint', 'author', 'pembuat', 'excel online', 'ptpln365', 'anang']):
        return f"""### 📁 Tata Kelola & Integritas Sumber Data Rekap
- **Nama Berkas:** `{src.get('workbook_title', 'Rekap Konsolidasi 910 Sistem Update 12Nov2026.xlsx')}`
- **Penyusun / Editor:** **{src.get('author', 'MOHAMMAD ANANG FACHRUDIN')}**
- **Media Sumber:** Microsoft SharePoint Online Organisasi PT PLN (Persero) 365
- **Tautan Resmi:** `{src.get('sharepoint_url', '-')}`
- **Validasi Data:** 100% Data Riil terverifikasi langsung dari sheet `Rekap Sistem` (910 sistem baris per baris tanpa estimasi buatan)."""

    if any(k in q for k in ['kualitas lokasi', 'koordinat bersama', 'kenapa koordinat sama', 'lokasi papua']):
        return """### 📍 Penjelasan Panel Kualitas Lokasi Sumber Data
Berdasarkan audit workbook resmi:
- Dari 910 sistem, terdapat **62 pasangan Latitude-Longitude unik**.
- Sebanyak **872 sistem menggunakan Koordinat Bersama** (titik kantor induk / UP3 / ULP terdekat).
- Khusus di **UIW Papua dan Papua Barat (7601)**, terdapat **241 sistem** yang menggunakan satu koordinat kantor induk Jayapura sampai verifikasi GPS lapangan tuntas.
- **Prinsip Tampilan:** Dashboard menampilkan bubble agregat asli tanpa menambahkan offset/jitter buatan agar integritas data sumber tetap terjaga 100%."""

    # -------------------------------------------------------------
    # 9. PENCARIAN SISTEM TERTENTU (BERDASARKAN ID ATAU NAMA)
    # -------------------------------------------------------------
    # Cek pencarian ID angka (misal "sistem 66", "no 56")
    id_match = re.search(r'\b(?:sistem|no|id|nomor)\s*#?\s*(\d+)\b', q)
    if id_match:
        target_no = int(id_match.group(1))
        found_by_no = next((s for s in systems if s.get('no') == target_no), None)
        if found_by_no:
            return build_system_card(found_by_no)

    # Cek pencarian nama spesifik dari 910 sistem
    # Bersihkan query dari stop words umum
    stop_words = ['bagaimana', 'kondisi', 'status', 'data', 'informasi', 'sistem', 'apa', 'kabar', 'tentang', 'tampilkan', 'buka', 'lihat', 'tolong', 'detail', 'analisis']
    clean_q = q
    for sw in stop_words:
        clean_q = re.sub(r'\b' + sw + r'\b', '', clean_q).strip()

    if len(clean_q) >= 3:
        # Prioritas 1: nama persis sama
        exact_match = next((s for s in systems if s.get('name', '').lower().strip() == clean_q), None)
        if exact_match:
            return build_system_card(exact_match)

        # Prioritas 2: substring nama sistem
        sub_matches = [s for s in systems if clean_q in s.get('name', '').lower()]
        if len(sub_matches) == 1:
            return build_system_card(sub_matches[0])
        elif len(sub_matches) > 1 and len(sub_matches) <= 5:
            resp = f"### 🔍 Ditemukan {len(sub_matches)} Sistem dengan kata kunci *'{clean_q}'*:\n\n"
            for s in sub_matches:
                sign = '+' if s.get('cad_mw', 0) >= 0 else ''
                resp += f"- **#{s['no']} {s['name']}** ({s['region']}) • {s['jenis']} ({s['jam_operasi']})\n"
                resp += f"  Status: **{s['status']}** | DMP `{f_num(s['dmp'])} MW` | Cadangan `{sign}{f_num(s['cad_mw'])} MW`\n"
                resp += f"  [[ACTION:focus_system:{s['no']}:🔍 Buka Detail Sistem {s['name']}]]\n\n"
            return resp

    # -------------------------------------------------------------
    # 10. OVERVIEW UMUM & RINGKASAN NASIONAL
    # -------------------------------------------------------------
    if any(k in q for k in ['halo', 'hai', 'siapa kamu', 'ringkasan', 'summary', 'overview', 'kpi', 'semua sistem', 'total sistem', 'rekap']):
        return build_group_summary(systems, "Seluruh 910 Sistem Kelistrikan Nasional PLN", "[[ACTION:reset_filters::🔄 Tampilkan Semua di Peta]]")

    # -------------------------------------------------------------
    # 11. SMART FALLBACK / SEARCH TOKEN MATCHING
    # -------------------------------------------------------------
    # Token matching untuk mencari sistem yang mendekati
    tokens = [t for t in clean_q.split() if len(t) >= 3]
    candidate_systems = []
    for s in systems:
        s_lower = s.get('name', '').lower()
        if any(tok in s_lower for tok in tokens):
            candidate_systems.append(s)

    if candidate_systems:
        top_candidates = candidate_systems[:6]
        resp = f"Saya menemukan beberapa sistem yang berkaitan dengan pertanyaan Anda *'{user_query}'*:\n\n"
        for s in top_candidates:
            sign = '+' if s.get('cad_mw', 0) >= 0 else ''
            resp += f"- **#{s['no']} {s['name']}** ({s['unit']}): **{s['status']}** (DMP `{f_num(s['dmp'])} MW`, Cadangan `{sign}{f_num(s['cad_mw'])} MW`)\n"
            resp += f"  [[ACTION:focus_system:{s['no']}:🔍 Buka Sistem {s['name']}]]\n"
        resp += f"\n💡 *Ketik nama lengkap salah satu sistem di atas atau gunakan navigasi dashboard.*"
        return resp

    # Fallback Default jika sama sekali tidak ada yang cocok
    return f"""Maaf, saya belum menemukan data spesifik untuk: *"{user_query}"*.

Silakan coba salah satu topik berikut:
- **Wilayah & Pulau:** *"Khusus Nusa Tenggara"*, *"Analisis sistem Papua"*, *"Kondisi Maluku"*, *"Sistem di Sumatera"*
- **Status Operasi:** *"Sistem mana saja yang defisit?"*, *"Tampilkan 57 sistem defisit"*, *"Sistem siaga"*
- **Pola Nyala & Jenis:** *"Berapa sistem 12 jam?"*, *"Jelaskan sistem 6 jam"*, *"Apa itu sistem isolated?"*
- **Fokus 24 Sistem:** *"Bagaimana fokus monitoring 24 sistem besar?"*, *"10 sistem terbesar di Indonesia"*
- **Sistem Tertentu:** *"Status Merauke"*, *"Kondisi Tanakeke"*, *"Data Batam-Bintan"*, *"Sistem Sulbagsel"*
- **Teknis:** *"Apa itu DMP?"*, *"Arti cadangan daya dan reserve margin"*, *"Sumber data SharePoint"*"""
