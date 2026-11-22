import re

with open('public/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Add Print CSS before </style>
print_css = '''
    /* ========================================================= */
    /* MCKINSEY EXECUTIVE PRINT REPORT STYLES (A4 PORTRAIT)      */
    /* ========================================================= */
    #executiveReportContainer {
      display: none;
    }

    @media print {
      @page {
        size: A4 portrait;
        margin: 10mm 12mm 12mm 12mm;
      }

      html, body {
        background: #FFFFFF !important;
        color: #0F172A !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif !important;
        -webkit-print-color-adjust: exact !important;
        print-color-adjust: exact !important;
        margin: 0 !important;
        padding: 0 !important;
        width: 100% !important;
      }

      /* Hide all regular web UI elements */
      header, .sub-bar, .active-filters-bar, .container,
      .filter-toolbar-unified, .tab-content, .chatbot-fab, .chatbot-drawer,
      .modal-overlay, #dynamicTooltip, #toast, .no-print,
      .map-island-nav, .leaflet-map-wrapper, .coord-drawer, .overview-layout,
      #provSummaryCardBox, .table-container, .pagination-box {
        display: none !important;
      }

      /* Show only executive report container */
      #executiveReportContainer {
        display: block !important;
        width: 100% !important;
        background: #FFFFFF !important;
        margin: 0 !important;
        padding: 0 !important;
      }

      .report-page {
        page-break-after: always;
        break-after: page;
        box-sizing: border-box;
        width: 100%;
        min-height: 268mm;
        padding: 0 0 10mm 0;
        position: relative;
        background: #FFFFFF;
      }

      .report-page:last-child {
        page-break-after: auto;
        break-after: auto;
      }

      .print-kop-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        border-bottom: 2.5px solid #0F2942;
        padding-bottom: 8px;
        margin-bottom: 12px;
      }

      .print-kop-left {
        display: flex;
        align-items: center;
        gap: 12px;
      }

      .print-pln-logo {
        width: 44px;
        height: 52px;
        object-fit: contain;
      }

      .print-kop-titles h2 {
        font-size: 14pt;
        font-weight: 800;
        color: #0F2942;
        margin: 0;
        letter-spacing: -0.3px;
        line-height: 1.15;
      }

      .print-kop-titles p {
        font-size: 8pt;
        color: #475569;
        margin: 2px 0 0 0;
        font-weight: 500;
      }

      .print-kop-badge {
        text-align: right;
      }

      .print-kop-badge .doc-class {
        background: #0F2942;
        color: #FFFFFF;
        font-size: 7.5pt;
        font-weight: 800;
        padding: 3px 8px;
        border-radius: 4px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        display: inline-block;
      }

      .print-kop-badge .sync-time {
        font-size: 7.5pt;
        color: #64748B;
        margin-top: 3px;
        font-weight: 600;
      }

      .print-action-title-box {
        background: #F8FAFC;
        border-left: 4.5px solid #0284C7;
        border-top: 1px solid #E2E8F0;
        border-right: 1px solid #E2E8F0;
        border-bottom: 1px solid #E2E8F0;
        padding: 8px 12px;
        border-radius: 0 6px 6px 0;
        margin-bottom: 10px;
      }

      .print-action-title {
        font-size: 10.5pt;
        font-weight: 800;
        color: #0F2942;
        line-height: 1.3;
      }

      .print-exec-callouts {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 8px;
        margin-bottom: 10px;
      }

      .print-callout-item {
        background: #FFFFFF;
        border: 1px solid #CBD5E1;
        border-radius: 6px;
        padding: 7px 9px;
      }

      .print-callout-item.alert {
        border-color: #EF4444;
        background: #FEF2F2;
      }

      .print-callout-item.primary {
        border-color: #0284C7;
        background: #F0F9FF;
      }

      .print-callout-header {
        font-size: 8pt;
        font-weight: 800;
        text-transform: uppercase;
        margin-bottom: 3px;
        display: flex;
        align-items: center;
        gap: 4px;
      }

      .print-callout-body {
        font-size: 7.2pt;
        color: #334155;
        line-height: 1.35;
      }

      .print-kpi-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 8px;
        margin-bottom: 10px;
      }

      .print-kpi-card {
        background: #FFFFFF;
        border: 1px solid #CBD5E1;
        border-radius: 6px;
        padding: 7px 10px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.03);
      }

      .print-kpi-card.defisit {
        border-color: #F87171;
      }

      .print-kpi-label {
        font-size: 7.5pt;
        color: #64748B;
        font-weight: 700;
        text-transform: uppercase;
      }

      .print-kpi-val {
        font-size: 13pt;
        font-weight: 800;
        color: #0F2942;
        margin: 2px 0;
        font-variant-numeric: tabular-nums;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      }

      .print-kpi-sub {
        font-size: 7pt;
        color: #64748B;
      }

      .print-map-card {
        background: #FFFFFF;
        border: 1px solid #CBD5E1;
        border-radius: 6px;
        padding: 8px 10px;
        margin-bottom: 8px;
      }

      .print-map-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 6px;
        border-bottom: 1px solid #E2E8F0;
        padding-bottom: 4px;
      }

      .print-map-title {
        font-size: 8.5pt;
        font-weight: 800;
        color: #0F2942;
      }

      .print-map-legend {
        display: flex;
        gap: 10px;
        font-size: 7pt;
        font-weight: 600;
        align-items: center;
      }

      .print-map-legend-dot {
        display: inline-block;
        width: 7px;
        height: 7px;
        border-radius: 50%;
        margin-right: 3px;
      }

      .print-wilayah-callouts-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 6px;
        margin-top: 6px;
      }

      .print-wilayah-chip {
        border: 1px solid #E2E8F0;
        border-radius: 4px;
        padding: 4px 6px;
        background: #F8FAFC;
      }

      .print-wilayah-chip.has-def {
        border-color: #FCA5A5;
        background: #FFF5F5;
      }

      .print-wilayah-name {
        font-size: 7.2pt;
        font-weight: 800;
        color: #0F2942;
        display: flex;
        justify-content: space-between;
      }

      .print-wilayah-stats {
        font-size: 6.5pt;
        color: #475569;
        margin-top: 2px;
        font-variant-numeric: tabular-nums;
      }

      .print-page-footer {
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-top: 1px solid #CBD5E1;
        padding-top: 4px;
        font-size: 7pt;
        color: #64748B;
      }

      /* Table formatting for page split */
      table.report-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 7.5pt;
        margin-bottom: 10px;
      }
      table.report-table thead {
        display: table-header-group !important;
      }
      table.report-table tr {
        break-inside: avoid !important;
        page-break-inside: avoid !important;
      }
      table.report-table th, table.report-table td {
        border: 1px solid #CBD5E1;
        padding: 4px 6px;
      }
      table.report-table th {
        background: #0F2942 !important;
        color: #FFFFFF !important;
        font-weight: 700;
        text-align: left;
        font-size: 7.2pt;
      }
      table.report-table td {
        color: #1E293B;
      }
      table.report-table tr:nth-child(even) td {
        background: #F8FAFC;
      }
      table.report-table td.num {
        text-align: right;
        font-variant-numeric: tabular-nums;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      }
      .badge-print-status {
        display: inline-block;
        padding: 1px 5px;
        border-radius: 3px;
        font-size: 6.5pt;
        font-weight: 800;
        text-transform: uppercase;
      }
      .badge-print-status.defisit { background: #FEE2E2; color: #DC2626; border: 1px solid #FCA5A5; }
      .badge-print-status.siaga { background: #FEF3C7; color: #D97706; border: 1px solid #FCD34D; }
      .badge-print-status.normal { background: #D1FAE5; color: #059669; border: 1px solid #6EE7B7; }
      .badge-print-status.unfilled { background: #F1F5F9; color: #64748B; border: 1px solid #CBD5E1; }
    }
'''

if '/* MCKINSEY EXECUTIVE PRINT REPORT STYLES (A4 PORTRAIT) */' not in html:
    html = html.replace('</style>', print_css + '\n  </style>')
    print("Added Print CSS into <style>")

# 2. Add executiveReportContainer HTML before closing </body>
report_html_skeleton = '''
  <!-- ========================================================= -->
  <!-- MCKINSEY EXECUTIVE PRINT REPORT CONTAINER (A4 PORTRAIT)   -->
  <!-- ========================================================= -->
  <div id="executiveReportContainer">
    <!-- Dynamically rendered by printExecutiveReport() -->
  </div>
'''

if '<div id="executiveReportContainer">' not in html:
    html = html.replace('</body>', report_html_skeleton + '\n</body>')
    print("Added #executiveReportContainer skeleton before </body>")

# 3. Add printExecutiveReport JavaScript implementation
print_js = '''
    // =========================================================
    // MCKINSEY EXECUTIVE REPORT GENERATOR & PRINT (A4 PORTRAIT)
    // =========================================================
    function printExecutiveReport() {
      if (!appData || !appData.systems) {
        showToast("Data sistem belum siap dicetak. Mohon tunggu sejenak.", true);
        return;
      }

      const container = document.getElementById('executiveReportContainer');
      if (!container) return;

      const kpi = appData.kpi_summary;
      const src = appData.source_info;
      const regions = appData.regions || [];
      const deficits = [...appData.systems].filter(s => s.cad_mw < 0).sort((a, b) => a.cad_mw - b.cad_mw);
      const nowStr = appData.last_updated_wib || (new Date().toLocaleString('id-ID', { timeZone: 'Asia/Jakarta' }) + ' WIB');

      // 1. Compute dynamic action title
      const nationalCad = kpi.total_cad_mw || 0;
      const rmPct = kpi.overall_reserve_margin_pct || 0;
      const defCount = deficits.length;
      const actionTitle = `NERACA DAYA NASIONAL ${nationalCad >= 0 ? 'SURPLUS +' : ''}${formatNum(nationalCad)} MW (CADANGAN MARGIN ${rmPct}%); FOKUS PENANGANAN PADA ${defCount} SISTEM DEFISIT REGIONAL`;

      // 2. Generate Vector Map SVG for Page 1
      const vectorMapSvg = buildPrintVectorMapSvg(appData.systems);

      // 3. Generate Charts SVG for Page 2
      const chartsSvg = buildPrintChartsSvg(regions);

      // 4. Generate Tables HTML for Page 3
      const regionalTableHtml = buildPrintRegionalMatrixTable(regions);
      const deficitPriorityTableHtml = buildPrintDeficitPriorityTable(deficits);

      // 5. Generate Appendix Tables for Page 4+
      const appendixTablesHtml = buildPrintAppendixTable(appData.systems);

      // Assemble 4 Pages
      container.innerHTML = `
        <!-- ========================================== -->
        <!-- HALAMAN 1: EXECUTIVE SUMMARY, KPI & MAP    -->
        <!-- ========================================== -->
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

        <!-- ========================================== -->
        <!-- HALAMAN 2: REGIONAL ANALYTICS & CHARTS     -->
        <!-- ========================================== -->
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

        <!-- ========================================== -->
        <!-- HALAMAN 3: MATRIKS KONSOLIDASI & DEFISIT   -->
        <!-- ========================================== -->
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

        <!-- ========================================== -->
        <!-- HALAMAN 4+: LAMPIRAN MATRIKS DETAIL SISTEM -->
        <!-- ========================================== -->
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

      // Trigger native print dialog (which saves to PDF perfectly)
      setTimeout(() => {
        window.print();
      }, 300);
    }

    // =========================================================
    // SVG BUILDERS FOR PRINT REPORT
    // =========================================================
    function buildPrintVectorMapSvg(systems) {
      const b = window.INDONESIA_MAP_BOUNDS || { width: 760, height: 260, min_lng: 94.5, max_lng: 141.5, min_lat: -11.5, max_lat: 6.5 };
      const mapPath = window.INDONESIA_SVG_MAP_PATH || '';

      // Cluster by exact coordinates
      const clusterMap = {};
      systems.forEach(s => {
        if (!s.geo || !s.geo.lat || !s.geo.lng) return;
        const key = `${s.geo.lat.toFixed(4)},${s.geo.lng.toFixed(4)}`;
        if (!clusterMap[key]) {
          clusterMap[key] = {
            lat: s.geo.lat,
            lng: s.geo.lng,
            is_shared: s.geo.is_shared,
            label: s.geo.label,
            island: s.island,
            systems: [],
            defCount: 0,
            siagaCount: 0,
            normalCount: 0,
            unfilledCount: 0
          };
        }
        const c = clusterMap[key];
        c.systems.push(s);
        if (s.cad_mw < 0) c.defCount++;
        else if (s.status_code === 'siaga') c.siagaCount++;
        else if (s.status_code === 'normal') c.normalCount++;
        else c.unfilledCount++;
      });

      // Render Bubbles
      const bubblesSvg = Object.values(clusterMap).map(c => {
        const x = ((c.lng - b.min_lng) / (b.max_lng - b.min_lng)) * 740 + 10;
        const y = ((b.max_lat - c.lat) / (b.max_lat - b.min_lat)) * 240 + 10;
        const count = c.systems.length;
        
        let fill = '#10B981';
        if (c.defCount > 0) fill = '#EF4444';
        else if (c.siagaCount > 0) fill = '#F59E0B';
        else if (c.normalCount > 0) fill = '#10B981';
        else fill = '#94A3B8';

        const r = Math.max(3.5, Math.min(12, Math.round(Math.sqrt(count) * 2.2)));
        
        let textSvg = '';
        if (count > 1) {
          textSvg = `<text x="${x.toFixed(1)}" y="${(y + 2.5).toFixed(1)}" text-anchor="middle" font-size="${count > 99 ? '6' : '7'}px" font-weight="700" fill="#FFFFFF">${count}</text>`;
        }

        let badgeSvg = '';
        if (c.defCount > 0 && count > 1) {
          badgeSvg = `<circle cx="${(x + r - 1).toFixed(1)}" cy="${(y - r + 1).toFixed(1)}" r="3" fill="#DC2626" stroke="#FFFFFF" stroke-width="0.8"/>`;
        }

        return `
          <g>
            <circle cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="${r}" fill="${fill}" stroke="#FFFFFF" stroke-width="1.2" opacity="0.9"/>
            ${textSvg}
            ${badgeSvg}
          </g>
        `;
      }).join('');

      return `
        <svg viewBox="0 0 760 260" width="100%" height="200" style="background:#FFFFFF; border-radius:4px;" xmlns="http://www.w3.org/2000/svg">
          <rect width="760" height="260" fill="#F8FAFC" rx="4"/>
          <path d="${mapPath}" fill="#E2E8F0" stroke="#94A3B8" stroke-width="0.75" />
          ${bubblesSvg}
        </svg>
      `;
    }

    function buildPrintChartsSvg(regions) {
      if (!regions || regions.length === 0) return '';

      // Find max DMP/BP for chart scale
      let maxMw = 1000;
      regions.forEach(r => {
        if (r.dmp > maxMw) maxMw = r.dmp;
        if (r.bp > maxMw) maxMw = r.bp;
      });

      const chartW = 730;
      const rowH = 26;
      const labelW = 110;
      const barAreaW = 460;
      const marginTagW = 140;

      // Chart 1: DMP vs BP Bars
      const barsSvg = regions.map((r, i) => {
        const y = i * (rowH + 4) + 20;
        const dmpW = Math.max(3, Math.round((r.dmp / maxMw) * barAreaW));
        const bpW = Math.max(3, Math.round((r.bp / maxMw) * barAreaW));
        const isDef = r.cad_mw < 0;
        const rmText = `${r.cad_mw >= 0 ? '+' : ''}${r.reserve_margin_pct}%`;
        const rmBg = isDef ? '#FEE2E2' : '#D1FAE5';
        const rmColor = isDef ? '#DC2626' : '#059669';

        return `
          <g transform="translate(0, ${y})">
            <!-- Region Label -->
            <text x="${labelW - 8}" y="12" text-anchor="end" font-size="8pt" font-weight="700" fill="#0F2942">${r.region}</text>
            <text x="${labelW - 8}" y="22" text-anchor="end" font-size="6.5pt" fill="#64748B">${r.count} Sis</text>

            <!-- DMP Bar (Navy) -->
            <rect x="${labelW}" y="2" width="${dmpW}" height="9" fill="#0F2942" rx="2" />
            <text x="${labelW + dmpW + 4}" y="9.5" font-size="6.5pt" font-weight="700" fill="#0F2942">${formatNum(r.dmp)}</text>

            <!-- BP Bar (Electric Blue) -->
            <rect x="${labelW}" y="13" width="${bpW}" height="9" fill="#0284C7" rx="2" />
            <text x="${labelW + bpW + 4}" y="20.5" font-size="6.5pt" font-weight="700" fill="#0284C7">${formatNum(r.bp)}</text>

            <!-- Reserve Margin Badge -->
            <rect x="${labelW + barAreaW + 55}" y="4" width="70" height="16" fill="${rmBg}" rx="3" stroke="${rmColor}" stroke-width="0.6"/>
            <text x="${labelW + barAreaW + 90}" y="15.5" text-anchor="middle" font-size="7pt" font-weight="800" fill="${rmColor}">${rmText} RM</text>
          </g>
        `;
      }).join('');

      // Chart 2: Stacked Bar for Jam Operasi & Status
      const stackedH = 20;
      const stackedSvg = regions.map((r, i) => {
        const y = i * (stackedH + 4) + 20;
        const total = r.count || 1;
        
        // Jam Nyala Segments
        const w24 = Math.round((r.count_24h / total) * 310);
        const w12 = Math.round((r.count_12h / total) * 310);
        const w6 = Math.max(0, 310 - w24 - w12);

        // Status Segments
        const wDef = Math.round((r.defisit / total) * 310);
        const wSiaga = Math.round((r.siaga / total) * 310);
        const wNorm = Math.round((r.normal / total) * 310);
        const wUnf = Math.max(0, 310 - wDef - wSiaga - wNorm);

        return `
          <g transform="translate(0, ${y})">
            <text x="80" y="14" text-anchor="end" font-size="7.5pt" font-weight="700" fill="#0F2942">${r.region}</text>
            
            <!-- Jam Operasi Stacked Bar -->
            <g transform="translate(90, 2)">
              <rect x="0" y="0" width="${w24}" height="15" fill="#0284C7" />
              <rect x="${w24}" y="0" width="${w12}" height="15" fill="#F59E0B" />
              <rect x="${w24 + w12}" y="0" width="${w6}" height="15" fill="#EF4444" />
              ${r.count_24h > 0 && w24 > 16 ? `<text x="${w24/2}" y="11" text-anchor="middle" font-size="6pt" font-weight="700" fill="#FFFFFF">${r.count_24h}</text>` : ''}
              ${r.count_12h > 0 && w12 > 16 ? `<text x="${w24 + w12/2}" y="11" text-anchor="middle" font-size="6pt" font-weight="700" fill="#FFFFFF">${r.count_12h}</text>` : ''}
              ${r.count_6h > 0 && w6 > 14 ? `<text x="${w24 + w12 + w6/2}" y="11" text-anchor="middle" font-size="6pt" font-weight="700" fill="#FFFFFF">${r.count_6h}</text>` : ''}
            </g>

            <!-- Status Neraca Stacked Bar -->
            <g transform="translate(420, 2)">
              <rect x="0" y="0" width="${wDef}" height="15" fill="#EF4444" />
              <rect x="${wDef}" y="0" width="${wSiaga}" height="15" fill="#F59E0B" />
              <rect x="${wDef + wSiaga}" y="0" width="${wNorm}" height="15" fill="#10B981" />
              <rect x="${wDef + wSiaga + wNorm}" y="0" width="${wUnf}" height="15" fill="#94A3B8" />
              ${r.defisit > 0 && wDef > 14 ? `<text x="${wDef/2}" y="11" text-anchor="middle" font-size="6pt" font-weight="700" fill="#FFFFFF">${r.defisit}</text>` : ''}
              ${r.siaga > 0 && wSiaga > 16 ? `<text x="${wDef + wSiaga/2}" y="11" text-anchor="middle" font-size="6pt" font-weight="700" fill="#FFFFFF">${r.siaga}</text>` : ''}
              ${r.normal > 0 && wNorm > 16 ? `<text x="${wDef + wSiaga + wNorm/2}" y="11" text-anchor="middle" font-size="6pt" font-weight="700" fill="#FFFFFF">${r.normal}</text>` : ''}
            </g>
          </g>
        `;
      }).join('');

      return `
        <!-- SVG Chart DMP vs BP -->
        <svg viewBox="0 0 740 230" width="100%" height="210" style="background:#FFFFFF; border:1px solid #CBD5E1; border-radius:6px; margin-bottom:10px;">
          <rect width="740" height="230" fill="#FFFFFF"/>
          <!-- Legend -->
          <g transform="translate(110, 10)">
            <rect x="0" y="0" width="10" height="10" fill="#0F2942" rx="2"/>
            <text x="14" y="8.5" font-size="7pt" font-weight="700" fill="#0F2942">Daya Mampu Pasok (DMP MW)</text>
            <rect x="180" y="0" width="10" height="10" fill="#0284C7" rx="2"/>
            <text x="194" y="8.5" font-size="7pt" font-weight="700" fill="#0284C7">Beban Puncak (BP MW)</text>
          </g>
          ${barsSvg}
        </svg>

        <!-- SVG Stacked Bars (Jam Operasi & Status) -->
        <div style="font-size:9pt; font-weight:800; color:#0F2942; margin-bottom:4px;">
          ⏱️ DISTRIBUSI POLA JAM OPERASI (KIRI) DAN KOMPOSISI STATUS OPERASIONAL (KANAN)
        </div>
        <svg viewBox="0 0 740 190" width="100%" height="175" style="background:#FFFFFF; border:1px solid #CBD5E1; border-radius:6px;">
          <rect width="740" height="190" fill="#FFFFFF"/>
          <!-- Header Legends -->
          <g transform="translate(90, 10)">
            <rect x="0" y="0" width="8" height="8" fill="#0284C7"/>
            <text x="12" y="7" font-size="6.5pt" font-weight="700" fill="#0284C7">24 Jam</text>
            <rect x="70" y="0" width="8" height="8" fill="#F59E0B"/>
            <text x="82" y="7" font-size="6.5pt" font-weight="700" fill="#F59E0B">12 Jam</text>
            <rect x="140" y="0" width="8" height="8" fill="#EF4444"/>
            <text x="152" y="7" font-size="6.5pt" font-weight="700" fill="#EF4444">6 Jam</text>
          </g>

          <g transform="translate(420, 10)">
            <rect x="0" y="0" width="8" height="8" fill="#EF4444"/>
            <text x="12" y="7" font-size="6.5pt" font-weight="700" fill="#EF4444">Defisit</text>
            <rect x="60" y="0" width="8" height="8" fill="#F59E0B"/>
            <text x="72" y="7" font-size="6.5pt" font-weight="700" fill="#F59E0B">Siaga</text>
            <rect x="115" y="0" width="8" height="8" fill="#10B981"/>
            <text x="127" y="7" font-size="6.5pt" font-weight="700" fill="#10B981">Normal</text>
            <rect x="175" y="0" width="8" height="8" fill="#94A3B8"/>
            <text x="187" y="7" font-size="6.5pt" font-weight="700" fill="#64748B">Belum Terisi</text>
          </g>
          ${stackedSvg}
        </svg>
      `;
    }

    function buildPrintRegionalMatrixTable(regions) {
      return `
        <table class="report-table">
          <thead>
            <tr>
              <th>Wilayah Regional</th>
              <th style="text-align:right;">Total Sistem</th>
              <th style="text-align:right;">Pola 24j</th>
              <th style="text-align:right;">Pola 12j</th>
              <th style="text-align:right;">Pola 6j</th>
              <th style="text-align:right;">DMP (MW)</th>
              <th style="text-align:right;">Beban Puncak (MW)</th>
              <th style="text-align:right;">Cadangan (MW)</th>
              <th style="text-align:right;">Margin (%)</th>
              <th style="text-align:right;">Defisit</th>
            </tr>
          </thead>
          <tbody>
            ${regions.map(r => `
              <tr>
                <td><strong>${r.region}</strong></td>
                <td class="num">${r.count}</td>
                <td class="num">${r.count_24h}</td>
                <td class="num">${r.count_12h}</td>
                <td class="num">${r.count_6h}</td>
                <td class="num" style="font-weight:700;">${formatNum(r.dmp)}</td>
                <td class="num">${formatNum(r.bp)}</td>
                <td class="num" style="font-weight:700; color:${r.cad_mw >= 0 ? '#10B981' : '#EF4444'};">
                  ${r.cad_mw >= 0 ? '+' : ''}${formatNum(r.cad_mw)}
                </td>
                <td class="num" style="font-weight:700; color:${r.reserve_margin_pct >= 0 ? '#10B981' : '#EF4444'};">
                  ${r.reserve_margin_pct}%
                </td>
                <td class="num" style="font-weight:800; color:${r.defisit > 0 ? '#EF4444' : '#10B981'};">
                  ${r.defisit > 0 ? `🔴 ${r.defisit}` : '✓ 0'}
                </td>
              </tr>
            `).join('')}
          </tbody>
        </table>
      `;
    }

    function buildPrintDeficitPriorityTable(deficits) {
      if (!deficits || deficits.length === 0) {
        return '<div style="font-size:8pt; color:#10B981; padding:8px;">✓ Tidak ada sistem yang berstatus Defisit.</div>';
      }

      return `
        <table class="report-table">
          <thead>
            <tr>
              <th style="width:24px;">No</th>
              <th>Nama Sistem</th>
              <th>Wilayah</th>
              <th>Unit Pelaksana</th>
              <th>Jenis</th>
              <th>Jam</th>
              <th style="text-align:right;">DMP (MW)</th>
              <th style="text-align:right;">BP (MW)</th>
              <th style="text-align:right;">Defisit (MW)</th>
              <th>Rekomendasi Aksi Mitigasi</th>
            </tr>
          </thead>
          <tbody>
            ${deficits.map((s, idx) => {
              let reco = "Optimalisasi sewa PLTD & percepatan pasokan bahan bakar";
              if (s.name.includes("SULBAGSEL")) reco = "Manuver transfer PLTA, perbaikan sewa PLTD/PLTU & peaker gas darurat";
              else if (s.name.includes("KALIMANTAN")) reco = "Penyeimbangan beban subsistem & percepatan sinkronisasi unit peaker";
              else if (s.name.includes("KHATULISTIWA")) reco = "Peningkatan transfer interkoneksi Sanggau & optimalisasi PLTD Siantan";
              else if (s.name.includes("TERNATE")) reco = "Penguatan pembangkit diesel sewa & relokasi genset unit kepulauan";
              else if (s.jenis_code === 'interkoneksi') reco = "Manuver transfer grid interkoneksi & pengurangan outage terencana";

              return `
                <tr>
                  <td>${idx + 1}</td>
                  <td><strong>${s.name}</strong></td>
                  <td>${s.region}</td>
                  <td>${s.unit}</td>
                  <td>${s.jenis}</td>
                  <td>${s.jam_operasi}</td>
                  <td class="num">${formatNum(s.dmp)}</td>
                  <td class="num">${formatNum(s.bp)}</td>
                  <td class="num" style="color:#EF4444; font-weight:800;">${formatNum(s.cad_mw)}</td>
                  <td style="font-size:7pt; color:#334155;">${reco}</td>
                </tr>
              `;
            }).join('')}
          </tbody>
        </table>
      `;
    }

    function buildPrintAppendixTable(systems) {
      // Use filtered list if user applied filters, otherwise all systems
      const list = (typeof getFilteredList === 'function') ? getFilteredList() : systems;

      return `
        <table class="report-table">
          <thead>
            <tr>
              <th style="width:24px;">No</th>
              <th>Nama Sistem</th>
              <th>Wilayah Regional</th>
              <th>Provinsi</th>
              <th>Jenis</th>
              <th>Jam Operasi</th>
              <th style="text-align:right;">DMP (MW)</th>
              <th style="text-align:right;">Beban Puncak (MW)</th>
              <th style="text-align:right;">Cadangan (MW)</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            ${list.map((s, idx) => `
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
      `;
    }
'''

if 'function printExecutiveReport()' not in html:
    html = html.replace('// App Startup', print_js + '\n    // App Startup')
    print("Added printExecutiveReport() and helper functions to JavaScript")

with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("build_executive_print.py COMPLETED successfully!")
