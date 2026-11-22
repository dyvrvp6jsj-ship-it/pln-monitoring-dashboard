with open('public/report_preview.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Replace report rendering inside report_preview.html
new_script = '''
  <script>
    function formatNum(val) {
      if (val === undefined || val === null || isNaN(val)) return '0,0';
      const n = Number(val);
      if (Math.abs(n) < 0.05) return '0,0';
      return n.toLocaleString('id-ID', { minimumFractionDigits: 1, maximumFractionDigits: 1 });
    }

    fetch('/api/data')
      .then(res => res.json())
      .then(data => {
        window.appData = data;
        renderReport();
      });

    function renderReport() {
      const data = window.appData;
      const kpi = data.kpi_summary;
      const regions = data.regions || [];
      const provinces = data.provinces || [];
      const deficits = [...data.systems].filter(s => s.cad_mw < 0).sort((a, b) => a.cad_mw - b.cad_mw);
      const nowStr = data.last_updated_wib || (new Date().toLocaleString('id-ID', { timeZone: 'Asia/Jakarta' }) + ' WIB');

      const nationalCad = kpi.total_cad_mw || 0;
      const rmPct = kpi.overall_reserve_margin_pct || 0;
      const defCount = deficits.length;
      const actionTitle = `NERACA DAYA NASIONAL ${nationalCad >= 0 ? 'SURPLUS +' : ''}${formatNum(nationalCad)} MW (CADANGAN MARGIN ${rmPct}%); PRIORITAS MANUVER PADA ${defCount} SISTEM DEFISIT REGIONAL`;

      const vectorMapSvg = buildPrintVectorMapSvg(data.systems);
      const chartsSvg = buildPrintChartsSvg(regions);
      const provinceMatrixHtml = buildPrintProvinceMatrixTable(provinces);

      document.getElementById('reportPagesWrapper').innerHTML = `
        <!-- HALAMAN 1 -->
        <div class="report-page-preview" id="previewPage1">
          <div class="print-kop-header">
            <div class="print-kop-left">
              <img src="/logo_pln.png" alt="PLN" class="print-pln-logo">
              <div class="print-kop-titles">
                <h2>PT PLN (PERSERO)</h2>
                <p>DIREKTORAT MANAJEMEN PEMBANGKITAN &amp; SISTEM KELISTRIKAN NASIONAL</p>
                <p style="font-size:7pt; color:#64748B; margin-top:1px;">Monitoring Neraca Daya 910 Sistem Kelistrikan • Interkoneksi (49), Isolated (645), ULD (216)</p>
              </div>
            </div>
            <div class="print-kop-badge">
              <span class="doc-class">Dokumen Eksekutif Direksi</span>
              <div class="sync-time">Sinkronisasi: ${nowStr}</div>
              <div style="font-size:6.8pt; color:#0284C7; font-weight:700; margin-top:2px;">910 SISTEM TERVERIFIKASI</div>
            </div>
          </div>

          <div class="print-action-title-box">
            <div class="print-action-title">
              ⚡ ${actionTitle}
            </div>
          </div>

          <div class="print-exec-callouts">
            <div class="print-callout-item primary">
              <div class="print-callout-header" style="color:#0284C7;">
                <span>🛡️</span> 1. Kesiapan Pasokan Nasional
              </div>
              <div class="print-callout-body">
                Daya Mampu Pasok (DMP) nasional mencapai <strong>${formatNum(kpi.total_dmp_mw)} MW</strong> melayani Beban Puncak <strong>${formatNum(kpi.total_bp_mw)} MW</strong> dengan surplus cadangan <strong>+${formatNum(kpi.total_cad_mw)} MW</strong> (RM ${rmPct}%). Sistem interkoneksi utama Jawa-Bali dan Sumatera beroperasi handal.
              </div>
            </div>

            <div class="print-callout-item alert">
              <div class="print-callout-header" style="color:#EF4444;">
                <span>🚨</span> 2. Mitigasi 51 Sistem Defisit
              </div>
              <div class="print-callout-body">
                Sebanyak <strong>${defCount} sistem</strong> teridentifikasi cadangan negatif (&lt; 0 MW), terkonsentrasi di Sulawesi (16 sistem, -325,1 MW), Sumatera (14 sistem), dan Kalimantan (8 sistem, -53,4 MW). Prioritas manuver peaker gas dan sewa genset darurat dibutuhkan segera.
              </div>
            </div>

            <div class="print-callout-item">
              <div class="print-callout-header" style="color:#64748B;">
                <span>📋</span> 3. Validasi 162 Sistem Belum Terisi
              </div>
              <div class="print-callout-body">
                Tercatat <strong>162 sistem isolated mikro</strong> (Sulawesi 8, Maluku 79, Papua 75) belum mengirimkan data beban secara realtime. Diinstruksikan kepada Unit Induk Wilayah terkait untuk memverifikasi telemetri pembangkitan.
              </div>
            </div>
          </div>

          <div class="print-kpi-grid">
            <div class="print-kpi-card">
              <div class="print-kpi-label">Total Sistem Terpantau</div>
              <div class="print-kpi-val">${kpi.total_sistem} <span style="font-size:8pt; font-weight:600; color:#64748B;">Sistem</span></div>
              <div class="print-kpi-sub">49 Interkoneksi • 645 Isolated • 216 ULD</div>
            </div>
            <div class="print-kpi-card">
              <div class="print-kpi-label">Daya Mampu Pasok (DMP)</div>
              <div class="print-kpi-val" style="color:#0284C7;">${formatNum(kpi.total_dmp_mw)} <span style="font-size:8pt; font-weight:600; color:#64748B;">MW</span></div>
              <div class="print-kpi-sub">Kapasitas pembangkit siap operasi</div>
            </div>
            <div class="print-kpi-card">
              <div class="print-kpi-label">Beban Puncak (BP)</div>
              <div class="print-kpi-val">${formatNum(kpi.total_bp_mw)} <span style="font-size:8pt; font-weight:600; color:#64748B;">MW</span></div>
              <div class="print-kpi-sub">Penyaluran listrik riil nasional</div>
            </div>
            <div class="print-kpi-card ${kpi.total_cad_mw < 0 ? 'defisit' : ''}">
              <div class="print-kpi-label">Cadangan Daya &amp; Margin</div>
              <div class="print-kpi-val" style="color:${kpi.total_cad_mw >= 0 ? '#10B981' : '#EF4444'};">
                ${kpi.total_cad_mw >= 0 ? '+' : ''}${formatNum(kpi.total_cad_mw)} <span style="font-size:8pt; font-weight:600; color:#64748B;">MW</span>
              </div>
              <div class="print-kpi-sub">Reserve Margin: <strong>${rmPct}%</strong> • ${defCount} Defisit</div>
            </div>
          </div>

          <div class="print-map-card">
            <div class="print-map-header">
              <span class="print-map-title">🗺️ SEBARAN GEOGRAFIS 910 SISTEM KELISTRIKAN INDONESIA (62 TITIK KOORDINAT UNIK)</span>
              <div class="print-map-legend">
                <span><span class="print-map-legend-dot" style="background:#EF4444;"></span> Defisit (51)</span>
                <span><span class="print-map-legend-dot" style="background:#F59E0B;"></span> Siaga (473)</span>
                <span><span class="print-map-legend-dot" style="background:#10B981;"></span> Normal (224)</span>
                <span><span class="print-map-legend-dot" style="background:#94A3B8;"></span> Belum Terisi (162)</span>
              </div>
            </div>

            <div style="width:100%; height:165px; display:flex; justify-content:center; align-items:center;">
              ${vectorMapSvg}
            </div>

            <div class="print-wilayah-callouts-grid">
              ${regions.map(r => `
                <div class="print-wilayah-chip ${r.defisit > 0 ? 'has-def' : ''}">
                  <div class="print-wilayah-name">
                    <span>${r.region}</span>
                    <span style="color:${r.defisit > 0 ? '#EF4444' : '#10B981'}; font-weight:700;">
                      ${r.defisit > 0 ? `🚨 ${r.defisit} Defisit` : '✓ Aman'}
                    </span>
                  </div>
                  <div class="print-wilayah-stats">
                    ${r.count} Sis • DMP: ${formatNum(r.dmp)} | BP: ${formatNum(r.bp)} MW
                  </div>
                  <div class="print-wilayah-stats" style="font-weight:700; color:${r.cad_mw >= 0 ? '#10B981' : '#EF4444'};">
                    Cad: ${r.cad_mw >= 0 ? '+' : ''}${formatNum(r.cad_mw)} MW (${r.reserve_margin_pct}%)
                  </div>
                </div>
              `).join('')}
            </div>
          </div>

          <div class="print-sub-footer">
            <span>PT PLN (Persero) • Dokumen Resmi Eksekutif Direksi</span>
            <span>Internal / Rahasia</span>
          </div>
        </div>

        <!-- HALAMAN 2 -->
        <div class="report-page-preview" id="previewPage2">
          <div class="print-kop-header">
            <div class="print-kop-left">
              <img src="/logo_pln.png" alt="PLN" class="print-pln-logo">
              <div class="print-kop-titles">
                <h2>PT PLN (PERSERO)</h2>
                <p>ANALITIK REGIONAL, KOMPOSISI JENIS SISTEM &amp; POLA OPERASI</p>
              </div>
            </div>
            <div class="print-kop-badge">
              <span class="doc-class">Halaman 2: Analitik</span>
              <div class="sync-time">${nowStr}</div>
            </div>
          </div>

          <div style="margin-bottom:6px;">
            <div style="font-size:9.5pt; font-weight:800; color:#0F2942;">
              📊 KOMPARASI DAYA MAMPU PASOK (DMP) VS BEBAN PUNCAK &amp; RESERVE MARGIN (7 REGIONAL)
            </div>
            <div style="font-size:7pt; color:#475569;">
              Evaluasi keandalan pasokan, margin cadangan, dan komposisi operasional di 7 Wilayah Regional PLN.
            </div>
          </div>

          ${chartsSvg}

          <div style="margin-top:8px; background:#F8FAFC; border:1px solid #CBD5E1; border-radius:4px; padding:6px 9px;">
            <div style="font-size:7.8pt; font-weight:800; color:#0F2942; margin-bottom:3px;">
              📌 CATATAN STRATEGIS MANAJEMEN OPERASI KELISTRIKAN
            </div>
            <ul style="margin:0 0 0 12px; padding:0; font-size:6.8pt; color:#334155; line-height:1.4;">
              <li><strong>Ketegangan Neraca Pasokan Sulawesi:</strong> Beban Puncak (3.240,8 MW) melampaui DMP (2.915,8 MW) menghasilkan defisit -325,1 MW (Reserve Margin -10,0%), terutama dipicu pertumbuhan beban industri smelter dan penurunan output PLTA akibat pola hidrologi.</li>
              <li><strong>Keseimbangan Pasokan Kalimantan:</strong> Reserve Margin tipis -1,7% (DMP 3.098,2 MW vs BP 3.151,6 MW, defisit -53,4 MW) membutuhkan penambahan pembangkitan gas peaker di sistem Interkoneksi Barito-Mahakam.</li>
              <li><strong>Ketahanan Sistem Jawa-Bali &amp; Sumatera:</strong> Cadangan Jawa Bali (+1.057,4 MW) dan Sumatera (+549,4 MW) berada pada level aman, namun 14 kantong isolated di Sumatera tetap defisit dan memerlukan sewa PLTD tambahan.</li>
              <li><strong>Pola Operasi Indonesia Timur:</strong> Maluku dan Papua didominasi sistem isolated dan ULD (216 ULD nasional, dengan 32 sistem beroperasi 6 jam). Diperlukan elektrifikasi PLTS Hybrid + BESS untuk mengonversi pola 6 jam / 12 jam menjadi 24 jam penuh.</li>
            </ul>
          </div>

          <div class="print-sub-footer">
            <span>PT PLN (Persero) • Dokumen Resmi Eksekutif Direksi</span>
            <span>Internal / Rahasia</span>
          </div>
        </div>

        <!-- HALAMAN 3 -->
        <div class="report-page-preview" id="previewPage3">
          <div class="print-kop-header">
            <div class="print-kop-left">
              <img src="/logo_pln.png" alt="PLN" class="print-pln-logo">
              <div class="print-kop-titles">
                <h2>PT PLN (PERSERO)</h2>
                <p>MATRIKS KONSOLIDASI PROVINSI &amp; DAFTAR AKSI PRIORITAS DEFISIT</p>
              </div>
            </div>
            <div class="print-kop-badge">
              <span class="doc-class">Halaman 3: Rencana Aksi</span>
              <div class="sync-time">${nowStr}</div>
            </div>
          </div>

          <div style="font-size:9pt; font-weight:800; color:#0F2942; margin-bottom:4px;">
            📋 MATRIKS KONSOLIDASI NERACA DAYA &amp; SEBARAN 51 SISTEM DEFISIT PER PROVINSI
          </div>
          ${provinceMatrixHtml}

          <!-- 3 Kategori Aksi Korporat -->
          <div style="font-size:8.5pt; font-weight:800; color:#0F2942; margin-top:8px; margin-bottom:4px;">
            🎯 3 KATEGORI AKSI KORPORAT PENANGANAN SISTEM DEFISIT &amp; VALIDASI
          </div>
          <div style="display:grid; grid-template-columns: repeat(3, 1fr); gap:6px;">
            <div style="background:#FEF2F2; border:1px solid #FCA5A5; border-radius:4px; padding:6px 8px;">
              <div style="font-size:7.2pt; font-weight:800; color:#DC2626; margin-bottom:2px;">
                ⚡ 1. Mitigasi Grid Interkoneksi (4 Sistem)
              </div>
              <div style="font-size:6.6pt; color:#334155; line-height:1.35;">
                • <strong>SULBAGSEL (-267,5 MW):</strong> Optimalisasi transfer hidro Poso &amp; sewa peaker gas darurat.<br>
                • <strong>Kalimantan (-60,2 MW) &amp; Khatulistiwa (-16,8 MW):</strong> Manuver peaker &amp; penyeimbangan transfer 150 kV.<br>
                • <strong>Ternate-Tidore (-9,9 MW):</strong> Relokasi genset diesel &amp; perbaikan unit sewa.
              </div>
            </div>

            <div style="background:#FFFBEB; border:1px solid #FCD34D; border-radius:4px; padding:6px 8px;">
              <div style="font-size:7.2pt; font-weight:800; color:#D97706; margin-bottom:2px;">
                🏝️ 2. Optimalisasi PLTD/Sewa Isolated (47 Sistem)
              </div>
              <div style="font-size:6.6pt; color:#334155; line-height:1.35;">
                • <strong>Leok (-72,2 MW) &amp; Tanakeke (-90 MW):</strong> Akselerasi suplai BBM &amp; genset cadangan darurat.<br>
                • <strong>Kepri (7 Sistem) &amp; Sulteng (6 Sistem):</strong> Penambahan mesin diesel modular sewa.<br>
                • <strong>NTT (3 Sistem) &amp; Maluku (4 Sistem):</strong> Peningkatan kesiapan unit isolated kepulauan.
              </div>
            </div>

            <div style="background:#F0F9FF; border:1px solid #BAE6FD; border-radius:4px; padding:6px 8px;">
              <div style="font-size:7.2pt; font-weight:800; color:#0284C7; margin-bottom:2px;">
                📡 3. Akselerasi Validasi 162 Sistem Belum Terisi
              </div>
              <div style="font-size:6.6pt; color:#334155; line-height:1.35;">
                • <strong>Instruksi GM UID/UIW:</strong> Penugasan unit Maluku (79 sis), Papua (75 sis), dan Sulawesi (8 sis).<br>
                • <strong>Pemasangan AMR/Telemetri:</strong> Digitalisasi metering pencatatan beban puncak harian.<br>
                • <strong>Target Integrasi:</strong> 100% data riil terhubung ke dashboard pusat monitoring.
              </div>
            </div>
          </div>

          <div class="print-sub-footer">
            <span>PT PLN (Persero) • Dokumen Resmi Eksekutif Direksi</span>
            <span>Internal / Rahasia</span>
          </div>
        </div>
      `;
    }

    function buildPrintVectorMapSvg(systems) {
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
    }

    function buildPrintChartsSvg(regions) {
      if (!regions || regions.length === 0) return '';
      let maxMw = 1000;
      regions.forEach(r => {
        if (r.dmp > maxMw) maxMw = r.dmp;
        if (r.bp > maxMw) maxMw = r.bp;
      });

      const labelW = 105;
      const barAreaW = 470;
      const rowH = 22;

      const barsSvg = regions.map((r, i) => {
        const y = i * (rowH + 3) + 18;
        const dmpW = Math.max(3, Math.round((r.dmp / maxMw) * barAreaW));
        const bpW = Math.max(3, Math.round((r.bp / maxMw) * barAreaW));
        const isDef = r.cad_mw < 0;
        const rmText = `${r.cad_mw >= 0 ? '+' : ''}${r.reserve_margin_pct}%`;
        const rmBg = isDef ? '#FEE2E2' : '#D1FAE5';
        const rmColor = isDef ? '#DC2626' : '#059669';

        return `
          <g transform="translate(0, ${y})">
            <text x="${labelW - 8}" y="11" text-anchor="end" font-size="7.5pt" font-weight="700" fill="#0F2942">${r.region}</text>
            <text x="${labelW - 8}" y="19" text-anchor="end" font-size="6pt" fill="#64748B">${r.count} Sis</text>
            <rect x="${labelW}" y="2" width="${dmpW}" height="8" fill="#0F2942" rx="1.5" />
            <text x="${labelW + dmpW + 3}" y="8.5" font-size="6pt" font-weight="700" fill="#0F2942">${formatNum(r.dmp)}</text>
            <rect x="${labelW}" y="11" width="${bpW}" height="8" fill="#0284C7" rx="1.5" />
            <text x="${labelW + bpW + 3}" y="17.5" font-size="6pt" font-weight="700" fill="#0284C7">${formatNum(r.bp)}</text>
            <rect x="${labelW + barAreaW + 55}" y="3" width="62" height="15" fill="${rmBg}" rx="2" stroke="${rmColor}" stroke-width="0.5"/>
            <text x="${labelW + barAreaW + 86}" y="13.5" text-anchor="middle" font-size="6.5pt" font-weight="800" fill="${rmColor}">${rmText} RM</text>
          </g>
        `;
      }).join('');

      const stackedH = 17;
      const stackedSvg = regions.map((r, i) => {
        const y = i * (stackedH + 3) + 16;
        const total = r.count || 1;
        const w24 = Math.round((r.count_24h / total) * 310);
        const w12 = Math.round((r.count_12h / total) * 310);
        const w6 = Math.max(0, 310 - w24 - w12);
        const wDef = Math.round((r.defisit / total) * 310);
        const wSiaga = Math.round((r.siaga / total) * 310);
        const wNorm = Math.round((r.normal / total) * 310);
        const wUnf = Math.max(0, 310 - wDef - wSiaga - wNorm);

        return `
          <g transform="translate(0, ${y})">
            <text x="80" y="12" text-anchor="end" font-size="7pt" font-weight="700" fill="#0F2942">${r.region}</text>
            <g transform="translate(90, 1)">
              <rect x="0" y="0" width="${w24}" height="13" fill="#0284C7" />
              <rect x="${w24}" y="0" width="${w12}" height="13" fill="#F59E0B" />
              <rect x="${w24 + w12}" y="0" width="${w6}" height="13" fill="#EF4444" />
              ${r.count_24h > 0 && w24 > 14 ? `<text x="${w24/2}" y="9.5" text-anchor="middle" font-size="5.5pt" font-weight="700" fill="#FFFFFF">${r.count_24h}</text>` : ''}
              ${r.count_12h > 0 && w12 > 14 ? `<text x="${w24 + w12/2}" y="9.5" text-anchor="middle" font-size="5.5pt" font-weight="700" fill="#FFFFFF">${r.count_12h}</text>` : ''}
              ${r.count_6h > 0 && w6 > 12 ? `<text x="${w24 + w12 + w6/2}" y="9.5" text-anchor="middle" font-size="5.5pt" font-weight="700" fill="#FFFFFF">${r.count_6h}</text>` : ''}
            </g>
            <g transform="translate(420, 1)">
              <rect x="0" y="0" width="${wDef}" height="13" fill="#EF4444" />
              <rect x="${wDef}" y="0" width="${wSiaga}" height="13" fill="#F59E0B" />
              <rect x="${wDef + wSiaga}" y="0" width="${wNorm}" height="13" fill="#10B981" />
              <rect x="${wDef + wSiaga + wNorm}" y="0" width="${wUnf}" height="13" fill="#94A3B8" />
              ${r.defisit > 0 && wDef > 12 ? `<text x="${wDef/2}" y="9.5" text-anchor="middle" font-size="5.5pt" font-weight="700" fill="#FFFFFF">${r.defisit}</text>` : ''}
              ${r.siaga > 0 && wSiaga > 14 ? `<text x="${wDef + wSiaga/2}" y="9.5" text-anchor="middle" font-size="5.5pt" font-weight="700" fill="#FFFFFF">${r.siaga}</text>` : ''}
              ${r.normal > 0 && wNorm > 14 ? `<text x="${wDef + wSiaga + wNorm/2}" y="9.5" text-anchor="middle" font-size="5.5pt" font-weight="700" fill="#FFFFFF">${r.normal}</text>` : ''}
            </g>
          </g>
        `;
      }).join('');

      return `
        <svg viewBox="0 0 740 200" width="100%" height="185" style="background:#FFFFFF; border:1px solid #CBD5E1; border-radius:4px; margin-bottom:8px;">
          <rect width="740" height="200" fill="#FFFFFF"/>
          <g transform="translate(105, 8)">
            <rect x="0" y="0" width="8" height="8" fill="#0F2942" rx="1.5"/>
            <text x="12" y="7" font-size="6.5pt" font-weight="700" fill="#0F2942">Daya Mampu Pasok (DMP MW)</text>
            <rect x="175" y="0" width="8" height="8" fill="#0284C7" rx="1.5"/>
            <text x="187" y="7" font-size="6.5pt" font-weight="700" fill="#0284C7">Beban Puncak (BP MW)</text>
          </g>
          ${barsSvg}
        </svg>

        <div style="font-size:8pt; font-weight:800; color:#0F2942; margin-bottom:3px;">
          ⏱️ DISTRIBUSI POLA JAM OPERASI (KIRI: 24 JAM / 12 JAM / 6 JAM) &amp; STATUS NERACA DAYA (KANAN)
        </div>
        <svg viewBox="0 0 740 165" width="100%" height="150" style="background:#FFFFFF; border:1px solid #CBD5E1; border-radius:4px;">
          <rect width="740" height="165" fill="#FFFFFF"/>
          <g transform="translate(90, 8)">
            <rect x="0" y="0" width="7" height="7" fill="#0284C7"/>
            <text x="10" y="6.5" font-size="6.2pt" font-weight="700" fill="#0284C7">24 Jam</text>
            <rect x="65" y="0" width="7" height="7" fill="#F59E0B"/>
            <text x="75" y="6.5" font-size="6.2pt" font-weight="700" fill="#F59E0B">12 Jam</text>
            <rect x="130" y="0" width="7" height="7" fill="#EF4444"/>
            <text x="140" y="6.5" font-size="6.2pt" font-weight="700" fill="#EF4444">6 Jam</text>
          </g>
          <g transform="translate(420, 8)">
            <rect x="0" y="0" width="7" height="7" fill="#EF4444"/>
            <text x="10" y="6.5" font-size="6.2pt" font-weight="700" fill="#EF4444">Defisit (51)</text>
            <rect x="65" y="0" width="7" height="7" fill="#F59E0B"/>
            <text x="75" y="6.5" font-size="6.2pt" font-weight="700" fill="#F59E0B">Siaga (473)</text>
            <rect x="125" y="0" width="7" height="7" fill="#10B981"/>
            <text x="135" y="6.5" font-size="6.2pt" font-weight="700" fill="#10B981">Normal (224)</text>
            <rect x="190" y="0" width="7" height="7" fill="#94A3B8"/>
            <text x="200" y="6.5" font-size="6.2pt" font-weight="700" fill="#64748B">Belum Terisi (162)</text>
          </g>
          ${stackedSvg}
        </svg>
      `;
    }

    function buildPrintProvinceMatrixTable(provinces) {
      if (!provinces || provinces.length === 0) return '<p>Data provinsi tidak tersedia.</p>';
      const defProvs = provinces.filter(p => p.defisit > 0).sort((a, b) => (b.defisit - a.defisit) || (a.cad_mw - b.cad_mw));
      const nonDefProvs = provinces.filter(p => p.defisit === 0);

      const nonDefCount = nonDefProvs.reduce((acc, p) => acc + (p.count || 0), 0);
      const nonDefDmp = nonDefProvs.reduce((acc, p) => acc + (p.dmp || 0), 0);
      const nonDefBp = nonDefProvs.reduce((acc, p) => acc + (p.bp || 0), 0);
      const nonDefCad = nonDefProvs.reduce((acc, p) => acc + (p.cad_mw || 0), 0);
      const nonDefInter = nonDefProvs.reduce((acc, p) => acc + (p.count_interkoneksi || 0), 0);
      const nonDefIso = nonDefProvs.reduce((acc, p) => acc + (p.count_isolated || 0), 0);
      const nonDefUld = nonDefProvs.reduce((acc, p) => acc + (p.count_uld || 0), 0);

      return `
        <table class="report-table">
          <thead>
            <tr>
              <th style="width:20px;">No</th>
              <th>Provinsi</th>
              <th>Regional</th>
              <th style="text-align:right;">Sistem (Inter/Iso/ULD)</th>
              <th style="text-align:right;">DMP (MW)</th>
              <th style="text-align:right;">BP (MW)</th>
              <th style="text-align:right;">Cad (MW)</th>
              <th style="text-align:right;">Defisit</th>
              <th>Daftar Sistem Defisit &amp; Besaran (MW)</th>
            </tr>
          </thead>
          <tbody>
            ${defProvs.map((p, idx) => {
              const defSysStr = (p.deficit_systems && p.deficit_systems.length > 0)
                ? p.deficit_systems.map(s => `<strong>${s.name}</strong> (${formatNum(s.cad_mw)} MW)`).join('; ')
                : '-';

              return `
                <tr>
                  <td>${idx + 1}</td>
                  <td><strong>${p.provinsi}</strong></td>
                  <td>${p.regional || p.pulau}</td>
                  <td class="num">${p.count} <span style="font-size:6pt; color:#64748B;">(${p.count_interkoneksi || 0}/${p.count_isolated || 0}/${p.count_uld || 0})</span></td>
                  <td class="num">${formatNum(p.dmp)}</td>
                  <td class="num">${formatNum(p.bp)}</td>
                  <td class="num" style="font-weight:700; color:${p.cad_mw < 0 ? '#EF4444' : '#10B981'};">
                    ${p.cad_mw >= 0 ? '+' : ''}${formatNum(p.cad_mw)}
                  </td>
                  <td class="num" style="font-weight:800; color:#EF4444;">
                    🔴 ${p.defisit}
                  </td>
                  <td style="font-size:6.5pt; color:#1E293B;">
                    ${defSysStr}
                  </td>
                </tr>
              `;
            }).join('')}
            <tr style="background:#F1F5F9; font-weight:700;">
              <td colspan="3"><strong>16 Provinsi Lainnya (Surplus Bebas Defisit: DKI Jakarta, Jabar, Jateng, Sumut, Sumsel, Kalbar, dll.)</strong></td>
              <td class="num">${nonDefCount} <span style="font-size:6pt; color:#64748B;">(${nonDefInter}/${nonDefIso}/${nonDefUld})</span></td>
              <td class="num">${formatNum(nonDefDmp)}</td>
              <td class="num">${formatNum(nonDefBp)}</td>
              <td class="num" style="color:#10B981;">+${formatNum(nonDefCad)}</td>
              <td class="num" style="color:#10B981;">✓ 0</td>
              <td style="font-size:6.5pt; color:#10B981;">Seluruh sistem beroperasi Normal / Siaga tanpa defisit</td>
            </tr>
            <tr style="background:#0F2942; color:#FFFFFF; font-weight:800;">
              <td colspan="3" style="color:#FFFFFF;">TOTAL KONSOLIDASI NASIONAL (35 PROVINSI)</td>
              <td class="num" style="color:#FFFFFF;">910 (49/645/216)</td>
              <td class="num" style="color:#FFFFFF;">${formatNum(appData.kpi_summary.total_dmp_mw)}</td>
              <td class="num" style="color:#FFFFFF;">${formatNum(appData.kpi_summary.total_bp_mw)}</td>
              <td class="num" style="color:#10B981;">+${formatNum(appData.kpi_summary.total_cad_mw)}</td>
              <td class="num" style="color:#FCA5A5;">51 SISTEM</td>
              <td style="color:#FFFFFF; font-size:6.5pt;">51 Sistem Defisit Tersebar di 19 Provinsi</td>
            </tr>
          </tbody>
        </table>
      `;
    }
  </script>
'''

s_idx = c.find('<script>')
if s_idx != -1:
    c = c[:s_idx] + new_script + '\n</body>\n</html>'
    with open('public/report_preview.html', 'w', encoding='utf-8') as f:
        f.write(c)
    print("Updated public/report_preview.html successfully!")
else:
    print("Could not find <script> in report_preview.html")
