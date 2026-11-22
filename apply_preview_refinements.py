def update_preview_html():
    file_path = '/Users/pln/.gemini/antigravity/scratch/pln-monitoring-dashboard/public/report_preview.html'
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # Kop badges
    text = text.replace(
        '<span class="doc-class">Halaman 1: Executive Summary</span>',
        '<span class="doc-class">REPORT</span>'
    )
    text = text.replace(
        '<span class="doc-class">Halaman 2: Analitik</span>',
        '<span class="doc-class">REPORT: ANALITIK</span>'
    )
    text = text.replace(
        '<span class="doc-class">Halaman 3: Rencana Aksi</span>',
        '<span class="doc-class">REPORT: RENCANA AKSI</span>'
    )

    # Footers
    text = text.replace(
        '<span>PT PLN (Persero) • Dokumen Resmi Eksekutif Direksi</span>',
        '<span>Report — Monitoring 910 Sistem Kelistrikan Nasional PLN</span>'
    )

    # Fix emojis
    text = text.replace('⚡ 1. Mitigasi Grid Interkoneksi (4 Sistem)', '1. Mitigasi Grid Interkoneksi (4 Sistem)')
    text = text.replace('🏝️ 2. Optimalisasi PLTD/Sewa Isolated (47 Sistem)', '2. Optimalisasi PLTD/Sewa Isolated (47 Sistem)')
    text = text.replace('📡 3. Akselerasi Validasi 162 Sistem Belum Terisi', '3. Akselerasi Validasi 162 Sistem Belum Terisi')

    # Format num
    old_fmt = """    function formatNum(val) {
      if (val === undefined || val === null || isNaN(val)) return '0,0';
      const n = Number(val);
      if (Math.abs(n) < 0.05) return '0,0';
      return n.toLocaleString('id-ID', { minimumFractionDigits: 1, maximumFractionDigits: 1 });
    }"""
    new_fmt = """    function formatNum(val) {
      if (val === undefined || val === null || isNaN(val)) return '0,0';
      const n = Number(val);
      if (n < 0 && n > -0.1) {
        return '-0,04';
      }
      if (Math.abs(n) < 0.05) return '0,0';
      return n.toLocaleString('id-ID', { minimumFractionDigits: 1, maximumFractionDigits: 1 });
    }"""
    text = text.replace(old_fmt, new_fmt)

    # Deficit column
    old_def = """                  <td class="num" style="font-weight:800; color:#EF4444;">
                    🔴 ${p.defisit}
                  </td>"""
    new_def = """                  <td class="num" style="font-weight:800; color:#EF4444;">
                    ${p.defisit}
                  </td>"""
    text = text.replace(old_def, new_def)

    text = text.replace('<td class="num" style="color:#10B981;">✓ 0</td>', '<td class="num" style="color:#10B981; font-weight:700;">0</td>')

    # Vector map bounds & viewBox
    text = text.replace('viewBox="0 0 760 230" width="100%" height="165"', 'viewBox="0 0 760 285" width="100%" height="175"')
    text = text.replace('<rect width="760" height="230" fill="#F8FAFC" rx="4"/>', '<rect width="760" height="285" fill="#F8FAFC" rx="4"/>')
    text = text.replace('const b = window.INDONESIA_MAP_BOUNDS || { width: 760, height: 260, min_lng: 94.5, max_lng: 141.5, min_lat: -11.5, max_lat: 6.5 };', 'const b = window.INDONESIA_MAP_BOUNDS || { width: 760, height: 285, min_lng: 94.8, max_lng: 141.2, min_lat: -11.2, max_lat: 6.2 };')
    text = text.replace('const x = ((c.lng - b.min_lng) / (b.max_lng - b.min_lng)) * 740 + 10;', 'const x = ((c.lng - b.min_lng) / (b.max_lng - b.min_lng)) * b.width;')
    text = text.replace('const y = ((b.max_lat - c.lat) / (b.max_lat - b.min_lat)) * 210 + 10;', 'const y = ((b.max_lat - c.lat) / (b.max_lat - b.min_lat)) * b.height;')

    # Appendix
    appendix_block = """
        <!-- BAB 4 (LAMPIRAN): REKAPITULASI STATUS OPERASIONAL 910 SISTEM KELISTRIKAN NASIONAL -->
        <div class="report-page-preview" id="previewPageAppendix" style="page-break-before:always;">
          <div class="print-kop-header">
            <div class="print-kop-left">
              <img src="/logo_pln.png" alt="PLN" class="print-pln-logo">
              <div class="print-kop-titles">
                <h2>PT PLN (PERSERO)</h2>
                <p>BAB 4 (LAMPIRAN): REKAPITULASI STATUS OPERASIONAL 910 SISTEM KELISTRIKAN NASIONAL</p>
              </div>
            </div>
            <div class="print-kop-badge">
              <span class="doc-class">REPORT: LAMPIRAN</span>
              <div class="sync-time">${nowStr}</div>
            </div>
          </div>

          <div style="font-size:7.5pt; color:#475569; margin-bottom:6px;">
            Menampilkan rincian status operasional 910 sistem kelistrikan individual secara padat dan terstruktur.
          </div>

          <table class="report-table" style="font-size:6.8pt;">
            <thead>
              <tr>
                <th style="width:20px;">No</th>
                <th>Nama Sistem</th>
                <th>Regional</th>
                <th>Provinsi</th>
                <th>Jenis</th>
                <th>Jam</th>
                <th style="text-align:right;">DMP (MW)</th>
                <th style="text-align:right;">BP (MW)</th>
                <th style="text-align:right;">Cadangan (MW)</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              ${data.systems.map((s, idx) => `
                <tr>
                  <td>${idx + 1}</td>
                  <td><strong>${s.name}</strong></td>
                  <td>${s.region}</td>
                  <td>${s.provinsi || s.region}</td>
                  <td>${s.jenis}</td>
                  <td>${s.jam_operasi}</td>
                  <td class="num">${formatNum(s.dmp)}</td>
                  <td class="num">${formatNum(s.bp)}</td>
                  <td class="num" style="font-weight:700; color:${s.cad_mw < 0 ? '#EF4444' : (s.cad_mw > 0 ? '#10B981' : '#64748B')};">
                    ${s.cad_mw > 0 ? '+' : ''}${formatNum(s.cad_mw)}
                  </td>
                  <td>
                    <span class="badge-print-status ${s.status_code}">${s.status}</span>
                  </td>
                </tr>
              `).join('')}
            </tbody>
          </table>

          <div class="print-sub-footer">
            <span>Report — Monitoring 910 Sistem Kelistrikan Nasional PLN</span>
            <span>Internal / Rahasia</span>
          </div>
        </div>
      `;
    }"""

    if 'previewPageAppendix' not in text:
        text = text.replace('</div>\n      `;\n    }', appendix_block)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(text)

    print('report_preview.html updated successfully!')

update_preview_html()
