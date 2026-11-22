import re

def update_index_html():
    file_path = '/Users/pln/.gemini/antigravity/scratch/pln-monitoring-dashboard/public/index.html'
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # 1. Update button text and checkbox in desktop header
    text = text.replace(
        '<span>+Lampiran 910 Sis</span>',
        '<span>Sertakan Lampiran 910 Sistem</span>'
    )
    text = text.replace(
        '<input type="checkbox" id="chkIncludeAppendix" onchange="window.includeAppendixInPrint = this.checked">',
        '<input type="checkbox" id="chkIncludeAppendix" checked onchange="window.includeAppendixInPrint = this.checked">'
    )
    text = text.replace(
        '<span>📄 Cetak Laporan Direksi</span>',
        '<span>📥 Download Report</span>'
    )
    text = text.replace(
        'title="Cetak Laporan Direksi Resmi (McKinsey Style A4 Portrait)"',
        'title="Download Laporan Resmi PLN (PDF / Cetak)"'
    )

    # 2. Update mobile menu drawer
    text = text.replace(
        '📄 Cetak Laporan Direksi',
        '📥 Download Report (PDF)'
    )
    text = text.replace(
        '<input type="checkbox" id="chkIncludeAppendixMob" onchange="document.getElementById(\'chkIncludeAppendix\').checked = this.checked; window.includeAppendixInPrint = this.checked;">',
        '<input type="checkbox" id="chkIncludeAppendixMob" checked onchange="document.getElementById(\'chkIncludeAppendix\').checked = this.checked; window.includeAppendixInPrint = this.checked;">'
    )
    text = text.replace(
        '<span style="font-size:11.5px; font-weight:600; color:#0F2942;">+Lampiran 910 Sistem</span>',
        '<span style="font-size:11.5px; font-weight:600; color:#0F2942;">Sertakan Lampiran 910 Sistem</span>'
    )

    # 3. Default variable
    text = text.replace('window.includeAppendixInPrint = false;', 'window.includeAppendixInPrint = true;')

    # 4. formatNum near-zero fix
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

    # 5. Kop badges and titles
    old_badge_page1 = """            <div class="print-kop-badge">
              <span class="doc-class">Dokumen Eksekutif Direksi</span>
              <div class="sync-time">Sinkronisasi: ${nowStr}</div>
              <div style="font-size:6.8pt; color:#0284C7; font-weight:700; margin-top:2px;">910 SISTEM TERVERIFIKASI</div>
            </div>"""

    new_badge_page1 = """            <div class="print-kop-badge">
              <span class="doc-class">REPORT</span>
              <div class="sync-time">Sinkronisasi: ${nowStr}</div>
              <div style="font-size:6.8pt; color:#0284C7; font-weight:700; margin-top:2px;">DOWNLOAD REPORT • 910 SISTEM</div>
            </div>"""

    text = text.replace(old_badge_page1, new_badge_page1)
    text = text.replace('<span class="doc-class">Halaman 2: Analitik</span>', '<span class="doc-class">REPORT: ANALITIK</span>')
    text = text.replace('<span class="doc-class">Halaman 3: Rencana Aksi</span>', '<span class="doc-class">REPORT: RENCANA AKSI</span>')
    text = text.replace('<span class="doc-class">Lampiran Detail</span>', '<span class="doc-class">REPORT: LAMPIRAN</span>')

    # 6. Footers
    text = text.replace(
        '<span>PT PLN (Persero) • Dokumen Resmi Eksekutif Direksi</span>',
        '<span>Report — Monitoring 910 Sistem Kelistrikan Nasional PLN</span>'
    )

    # 7. Page 3 headings: Remove emojis that turn to 41. and 12.
    text = text.replace('⚡ 1. Mitigasi Grid Interkoneksi (4 Sistem)', '1. Mitigasi Grid Interkoneksi (4 Sistem)')
    text = text.replace('🏝️ 2. Optimalisasi PLTD/Sewa Isolated (47 Sistem)', '2. Optimalisasi PLTD/Sewa Isolated (47 Sistem)')
    text = text.replace('📡 3. Akselerasi Validasi 162 Sistem Belum Terisi', '3. Akselerasi Validasi 162 Sistem Belum Terisi')

    # 8. buildPrintProvinceMatrixTable deficit badge & surplus 0
    old_def_cell = """                  <td class="num" style="font-weight:800; color:#EF4444;">
                    🔴 ${p.defisit}
                  </td>"""
    new_def_cell = """                  <td class="num" style="font-weight:800; color:#EF4444;">
                    ${p.defisit}
                  </td>"""
    text = text.replace(old_def_cell, new_def_cell)

    text = text.replace(
        '<td class="num" style="color:#10B981;">✓ 0</td>',
        '<td class="num" style="color:#10B981; font-weight:700;">0</td>'
    )

    # 9. buildPrintAppendixTable heading
    text = text.replace(
        '<p>LAMPIRAN MATRIKS STATUS 910 SISTEM KELISTRIKAN NASIONAL (COMPACT)</p>',
        '<p>BAB 4 (LAMPIRAN): REKAPITULASI STATUS OPERASIONAL 910 SISTEM KELISTRIKAN NASIONAL</p>'
    )

    # 10. Vector map builder SVG dimensions and projection
    old_vmap = """    function buildPrintVectorMapSvg(systems) {
      const b = window.INDONESIA_MAP_BOUNDS || { width: 760, height: 260, min_lng: 94.5, max_lng: 141.5, min_lat: -11.5, max_lat: 6.5 };
      const mapPath = window.INDONESIA_SVG_MAP_PATH || '';

      const clusterMap = {};
      systems.forEach(s => {
        if (!s.geo || !s.geo.lat || !s.geo.lng) return;
        const key = `${s.geo.lat.toFixed(4)},${s.geo.lng.toFixed(4)}`;
        if (!clusterMap[key]) {
          clusterMap[key] = {
            lat: s.geo.lat, lng: s.geo.lng, is_shared: s.geo.is_shared,
            systems: [], defCount: 0, siagaCount: 0, normalCount: 0, unfilledCount: 0
          };
        }
        const c = clusterMap[key];
        c.systems.push(s);
        if (s.cad_mw < 0) c.defCount++;
        else if (s.status_code === 'siaga') c.siagaCount++;
        else if (s.status_code === 'normal') c.normalCount++;
        else c.unfilledCount++;
      });

      const bubblesSvg = Object.values(clusterMap).map(c => {
        const x = ((c.lng - b.min_lng) / (b.max_lng - b.min_lng)) * 740 + 10;
        const y = ((b.max_lat - c.lat) / (b.max_lat - b.min_lat)) * 210 + 10;
        const count = c.systems.length;
        
        let fill = '#10B981';
        if (c.defCount > 0) fill = '#EF4444';
        else if (c.siagaCount > 0) fill = '#F59E0B';
        else if (c.normalCount > 0) fill = '#10B981';
        else fill = '#94A3B8';

        const r = Math.max(3, Math.min(10, Math.round(Math.sqrt(count) * 2.0)));
        let textSvg = count > 1 ? `<text x="${x.toFixed(1)}" y="${(y + 2.5).toFixed(1)}" text-anchor="middle" font-size="${count > 99 ? '5.5' : '6.5'}px" font-weight="700" fill="#FFFFFF">${count}</text>` : '';
        let badgeSvg = (c.defCount > 0 && count > 1) ? `<circle cx="${(x + r - 1).toFixed(1)}" cy="${(y - r + 1).toFixed(1)}" r="2.8" fill="#DC2626" stroke="#FFFFFF" stroke-width="0.7"/>` : '';

        return `
          <g>
            <circle cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="${r}" fill="${fill}" stroke="#FFFFFF" stroke-width="1" opacity="0.9"/>
            ${textSvg}
            ${badgeSvg}
          </g>
        `;
      }).join('');

      return `
        <svg viewBox="0 0 760 230" width="100%" height="165" style="background:#F8FAFC; border-radius:4px;" xmlns="http://www.w3.org/2000/svg">
          <rect width="760" height="230" fill="#F8FAFC" rx="4"/>
          <path d="${mapPath}" fill="#E2E8F0" stroke="#94A3B8" stroke-width="0.7" />
          ${bubblesSvg}
        </svg>
      `;
    }"""

    new_vmap = """    function buildPrintVectorMapSvg(systems) {
      const b = window.INDONESIA_MAP_BOUNDS || { width: 760, height: 285, min_lng: 94.8, max_lng: 141.2, min_lat: -11.2, max_lat: 6.2 };
      const mapPath = window.INDONESIA_SVG_MAP_PATH || '';

      const clusterMap = {};
      systems.forEach(s => {
        if (!s.geo || !s.geo.lat || !s.geo.lng) return;
        const key = `${s.geo.lat.toFixed(4)},${s.geo.lng.toFixed(4)}`;
        if (!clusterMap[key]) {
          clusterMap[key] = {
            lat: s.geo.lat, lng: s.geo.lng, is_shared: s.geo.is_shared,
            systems: [], defCount: 0, siagaCount: 0, normalCount: 0, unfilledCount: 0
          };
        }
        const c = clusterMap[key];
        c.systems.push(s);
        if (s.cad_mw < 0) c.defCount++;
        else if (s.status_code === 'siaga') c.siagaCount++;
        else if (s.status_code === 'normal') c.normalCount++;
        else c.unfilledCount++;
      });

      const bubblesSvg = Object.values(clusterMap).map(c => {
        const x = ((c.lng - b.min_lng) / (b.max_lng - b.min_lng)) * b.width;
        const y = ((b.max_lat - c.lat) / (b.max_lat - b.min_lat)) * b.height;
        const count = c.systems.length;
        
        let fill = '#10B981';
        if (c.defCount > 0) fill = '#EF4444';
        else if (c.siagaCount > 0) fill = '#F59E0B';
        else if (c.normalCount > 0) fill = '#10B981';
        else fill = '#94A3B8';

        const r = Math.max(3.5, Math.min(11, Math.round(Math.sqrt(count) * 2.1)));
        let textSvg = count > 1 ? `<text x="${x.toFixed(1)}" y="${(y + 2.5).toFixed(1)}" text-anchor="middle" font-size="${count > 99 ? '5.5' : '6.5'}px" font-weight="700" fill="#FFFFFF">${count}</text>` : '';
        let badgeSvg = (c.defCount > 0 && count > 1) ? `<circle cx="${(x + r - 1).toFixed(1)}" cy="${(y - r + 1).toFixed(1)}" r="3.0" fill="#DC2626" stroke="#FFFFFF" stroke-width="0.8"/>` : '';

        return `
          <g>
            <circle cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="${r}" fill="${fill}" stroke="#FFFFFF" stroke-width="1" opacity="0.9"/>
            ${textSvg}
            ${badgeSvg}
          </g>
        `;
      }).join('');

      return `
        <svg viewBox="0 0 760 285" width="100%" height="175" style="background:#F8FAFC; border-radius:4px;" xmlns="http://www.w3.org/2000/svg">
          <rect width="760" height="285" fill="#F8FAFC" rx="4"/>
          <path d="${mapPath}" fill="#E2E8F0" stroke="#94A3B8" stroke-width="0.75" />
          ${bubblesSvg}
        </svg>
      `;
    }"""

    text = text.replace(old_vmap, new_vmap)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(text)

    print('index.html updated successfully!')

update_index_html()
