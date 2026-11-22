with open('public/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Replace printExecutiveReport definition with renderExecutiveReportHtml + printExecutiveReport + beforeprint listener
target_def = 'function printExecutiveReport() {'
replacement_def = '''function renderExecutiveReportHtml() {
      if (!appData || !appData.systems) return false;

      const container = document.getElementById('executiveReportContainer');
      if (!container) return false;

      const kpi = appData.kpi_summary;
      const src = appData.source_info;
      const regions = appData.regions || [];
      const deficits = [...appData.systems].filter(s => s.cad_mw < 0).sort((a, b) => a.cad_mw - b.cad_mw);
      const nowStr = appData.last_updated_wib || (new Date().toLocaleString('id-ID', { timeZone: 'Asia/Jakarta' }) + ' WIB');

      const nationalCad = kpi.total_cad_mw || 0;
      const rmPct = kpi.overall_reserve_margin_pct || 0;
      const defCount = deficits.length;
      const actionTitle = `NERACA DAYA NASIONAL ${nationalCad >= 0 ? 'SURPLUS +' : ''}${formatNum(nationalCad)} MW (CADANGAN MARGIN ${rmPct}%); FOKUS PENANGANAN PADA ${defCount} SISTEM DEFISIT REGIONAL`;

      const vectorMapSvg = buildPrintVectorMapSvg(appData.systems);
      const chartsSvg = buildPrintChartsSvg(regions);
      const regionalTableHtml = buildPrintRegionalMatrixTable(regions);
      const deficitPriorityTableHtml = buildPrintDeficitPriorityTable(deficits);
      const appendixTablesHtml = buildPrintAppendixTable(appData.systems);

      container.innerHTML = `
        <!-- HALAMAN 1 -->
        <div class="report-page" id="reportPage1">
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

          <!-- 4 KPI Cards -->
          <div class="print-kpi-grid">
            <div class="print-kpi-card">
              <div class="print-kpi-label">Total Sistem Terpantau</div>
              <div class="print-kpi-val">${kpi.total_sistem} <span style="font-size:8.5pt; font-weight:600; color:#64748B;">Sistem</span></div>
              <div class="print-kpi-sub">49 Interkoneksi • 645 Isolated • 216 ULD</div>
            </div>
            <div class="print-kpi-card">
              <div class="print-kpi-label">Daya Mampu Pasok (DMP)</div>
              <div class="print-kpi-val" style="color:#0284C7;">${formatNum(kpi.total_dmp_mw)} <span style="font-size:8.5pt; font-weight:600; color:#64748B;">MW</span></div>
              <div class="print-kpi-sub">Kapasitas pembangkit siap operasi</div>
            </div>
            <div class="print-kpi-card">
              <div class="print-kpi-label">Beban Puncak (BP)</div>
              <div class="print-kpi-val">${formatNum(kpi.total_bp_mw)} <span style="font-size:8.5pt; font-weight:600; color:#64748B;">MW</span></div>
              <div class="print-kpi-sub">Penyaluran listrik riil nasional</div>
            </div>
            <div class="print-kpi-card ${kpi.total_cad_mw < 0 ? 'defisit' : ''}">
              <div class="print-kpi-label">Cadangan Daya &amp; Margin</div>
              <div class="print-kpi-val" style="color:${kpi.total_cad_mw >= 0 ? '#10B981' : '#EF4444'};">
                ${kpi.total_cad_mw >= 0 ? '+' : ''}${formatNum(kpi.total_cad_mw)} <span style="font-size:8.5pt; font-weight:600; color:#64748B;">MW</span>
              </div>
              <div class="print-kpi-sub">Reserve Margin: <strong>${rmPct}%</strong> • ${defCount} Defisit</div>
            </div>
          </div>

          <!-- Clean Vector Infographic Map -->
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

            <div style="width:100%; height:200px; display:flex; justify-content:center; align-items:center;">
              ${vectorMapSvg}
            </div>

            <!-- 7 Wilayah Callout Boxes -->
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

          <div class="print-page-footer">
            <span>PT PLN (Persero) • Executive Summary Neraca Daya 910 Sistem</span>
            <span>Halaman 1 dari 4+</span>
          </div>
        </div>

        <!-- HALAMAN 2 -->
        <div class="report-page" id="reportPage2">
          <div class="print-kop-header">
            <div class="print-kop-left">
              <img src="/logo_pln.png" alt="PLN" class="print-pln-logo">
              <div class="print-kop-titles">
                <h2>PT PLN (PERSERO)</h2>
                <p>ANALITIK REGIONAL, KOMPOSISI STATUS &amp; POLA JAM OPERASI</p>
              </div>
            </div>
            <div class="print-kop-badge">
              <span class="doc-class">Halaman 2: Analitik</span>
              <div class="sync-time">${nowStr}</div>
            </div>
          </div>

          <div style="margin-bottom:8px;">
            <div style="font-size:10pt; font-weight:800; color:#0F2942;">
              📊 KOMPARASI DAYA MAMPU PASOK (DMP) VS BEBAN PUNCAK &amp; RESERVE MARGIN
            </div>
            <div style="font-size:7.5pt; color:#475569;">
              Evaluasi keandalan pasokan dan rasio margin cadangan daya di 7 Wilayah Regional operasional PLN.
            </div>
          </div>

          ${chartsSvg}

          <div style="margin-top:10px; background:#F8FAFC; border:1px solid #CBD5E1; border-radius:6px; padding:8px 10px;">
            <div style="font-size:8pt; font-weight:800; color:#0F2942; margin-bottom:4px;">
              📌 CATATAN STRATEGIS MANAJEMEN OPERASI KELISTRIKAN
            </div>
            <ul style="margin:0 0 0 14px; padding:0; font-size:7.2pt; color:#334155; line-height:1.45;">
              <li><strong>Ketegangan Neraca Pasokan Sulawesi:</strong> Beban Puncak (3.240,8 MW) melampaui DMP (2.915,8 MW) menghasilkan defisit -325,1 MW (Reserve Margin -10,0%), terutama dipicu pertumbuhan beban industri smelter dan penurunan output PLTA akibat pola hidrologi.</li>
              <li><strong>Keseimbangan Pasokan Kalimantan:</strong> Reserve Margin tipis -1,7% (DMP 3.098,2 MW vs BP 3.151,6 MW, defisit -53,4 MW) membutuhkan penambahan pembangkitan gas peaker di sistem Interkoneksi Barito-Mahakam.</li>
              <li><strong>Ketahanan Sistem Jawa-Bali &amp; Sumatera:</strong> Cadangan Jawa Bali (+1.057,4 MW) dan Sumatera (+549,4 MW) berada pada level aman, namun 14 kantong isolated di Sumatera tetap defisit dan memerlukan sewa PLTD tambahan.</li>
              <li><strong>Pola Operasi Indonesia Timur:</strong> Maluku dan Papua didominasi sistem isolated dan ULD (216 ULD nasional, dengan 32 sistem beroperasi 6 jam). Diperlukan elektrifikasi PLTS Hybrid + BESS untuk mengonversi pola 6j/12j menjadi 24 jam.</li>
            </ul>
          </div>

          <div class="print-page-footer">
            <span>PT PLN (Persero) • Analisis Regional &amp; Pola Operasi</span>
            <span>Halaman 2 dari 4+</span>
          </div>
        </div>

        <!-- HALAMAN 3 -->
        <div class="report-page" id="reportPage3">
          <div class="print-kop-header">
            <div class="print-kop-left">
              <img src="/logo_pln.png" alt="PLN" class="print-pln-logo">
              <div class="print-kop-titles">
                <h2>PT PLN (PERSERO)</h2>
                <p>MATRIKS KONSOLIDASI 7 REGIONAL &amp; DAFTAR AKSI PRIORITAS 51 SISTEM DEFISIT</p>
              </div>
            </div>
            <div class="print-kop-badge">
              <span class="doc-class">Halaman 3: Rencana Aksi</span>
              <div class="sync-time">${nowStr}</div>
            </div>
          </div>

          <div style="font-size:9pt; font-weight:800; color:#0F2942; margin-bottom:4px;">
            📋 TABEL 1: MATRIKS KONSOLIDASI 7 WILAYAH REGIONAL
          </div>
          ${regionalTableHtml}

          <div style="font-size:9pt; font-weight:800; color:#EF4444; margin-top:8px; margin-bottom:4px;">
            🚨 TABEL 2: DAFTAR AKSI PRIORITAS SELURUH SISTEM DEFISIT (CADANGAN &lt; 0 MW) — DIURUTKAN DEFISIT TERBESAR
          </div>
          ${deficitPriorityTableHtml}

          <div class="print-page-footer">
            <span>PT PLN (Persero) • Matriks Regional &amp; Aksi Prioritas Defisit</span>
            <span>Halaman 3 dari 4+</span>
          </div>
        </div>

        <!-- HALAMAN 4+ -->
        <div class="report-page" id="reportPage4">
          <div class="print-kop-header">
            <div class="print-kop-left">
              <img src="/logo_pln.png" alt="PLN" class="print-pln-logo">
              <div class="print-kop-titles">
                <h2>PT PLN (PERSERO)</h2>
                <p>LAMPIRAN MATRIKS DETAIL SISTEM KELISTRIKAN NASIONAL (TERFILTER / LENGKAP)</p>
              </div>
            </div>
            <div class="print-kop-badge">
              <span class="doc-class">Lampiran Sistem</span>
              <div class="sync-time">${nowStr}</div>
            </div>
          </div>

          <div style="font-size:8.5pt; color:#475569; margin-bottom:6px;">
            Menampilkan data neraca pasokan daya sistem kelistrikan individual dengan pengulangan header otomatis pada setiap lembar cetak.
          </div>

          ${appendixTablesHtml}

          <div class="print-page-footer">
            <span>PT PLN (Persero) • Lampiran Detail Sistem Kelistrikan Nasional</span>
            <span>Halaman 4+</span>
          </div>
        </div>
      `;
      return true;
    }

    function printExecutiveReport() {
      if (!renderExecutiveReportHtml()) {
        showToast("Menyiapkan dokumen laporan direksi...", false);
        setTimeout(() => {
          if (renderExecutiveReportHtml()) window.print();
        }, 500);
        return;
      }
      setTimeout(() => {
        window.print();
      }, 250);
    }

    // Auto-prepare before printing or when preview is requested
    window.addEventListener('beforeprint', () => {
      renderExecutiveReportHtml();
    });

    function checkReportPreviewQuery() {
      const p = new URLSearchParams(window.location.search);
      if (p.get('preview') === 'report') {
        setTimeout(() => {
          renderExecutiveReportHtml();
          const el = document.getElementById('executiveReportContainer');
          if (el) {
            el.style.display = 'block';
            document.body.style.background = '#F1F5F9';
            el.style.maxWidth = '210mm';
            el.style.margin = '20px auto';
            el.style.boxShadow = '0 10px 30px rgba(0,0,0,0.15)';
            el.style.padding = '12mm';
          }
        }, 600);
      }
    }
'''

# Find existing printExecutiveReport up to buildPrintVectorMapSvg
idx_start = c.find('function printExecutiveReport() {')
idx_end = c.find('function buildPrintVectorMapSvg(systems) {')

if idx_start != -1 and idx_end != -1:
    c = c[:idx_start] + replacement_def + '\n    ' + c[idx_end:]
    print("Updated print report generation logic!")
else:
    print("Could not find start/end indices")

# Call checkReportPreviewQuery in DOMContentLoaded
c = c.replace('changeAutoRefresh(30);', 'changeAutoRefresh(30);\n      checkReportPreviewQuery();')

with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(c)
print("Finished patch_report_preview.py")
