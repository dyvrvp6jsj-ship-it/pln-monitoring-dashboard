import re

with open('public/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update number formatting in index.html to guarantee no "-0" or "-0,0"
old_format_num = """    function formatNum(val) {
      if (val === undefined || val === null || isNaN(val)) return '0,0';
      return Number(val).toLocaleString('id-ID', { minimumFractionDigits: 1, maximumFractionDigits: 1 });
    }"""

new_format_num = """    function formatNum(val) {
      if (val === undefined || val === null || isNaN(val)) return '0,0';
      const n = Number(val);
      if (Math.abs(n) < 0.05) return '0,0';
      return n.toLocaleString('id-ID', { minimumFractionDigits: 1, maximumFractionDigits: 1 });
    }"""

if old_format_num in html:
    html = html.replace(old_format_num, new_format_num)
    print("1. Updated formatNum to eliminate -0 and -0,0")

# 2. Add Mobile CSS & Refined Print CSS
css_additions = """
    /* ========================================================= */
    /* REFINED MCKINSEY / BCG PRINT REPORT STYLES (A4 PORTRAIT)  */
    /* ========================================================= */
    #executiveReportContainer {
      display: none;
    }

    @media print {
      @page {
        size: A4 portrait;
        margin: 8mm 10mm 8mm 10mm;
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
      #provSummaryCardBox, .table-container, .pagination-box,
      .mobile-bottom-nav, .mobile-menu-drawer, .mobile-hamburger-btn {
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
        page-break-inside: avoid;
        break-inside: avoid;
        box-sizing: border-box;
        width: 100%;
        margin: 0;
        padding: 0;
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
        border-bottom: 2px solid #0F2942;
        padding-bottom: 6px;
        margin-bottom: 8px;
      }

      .print-kop-left {
        display: flex;
        align-items: center;
        gap: 10px;
      }

      .print-pln-logo {
        width: 38px;
        height: 46px;
        object-fit: contain;
      }

      .print-kop-titles h2 {
        font-size: 13pt;
        font-weight: 800;
        color: #0F2942;
        margin: 0;
        letter-spacing: -0.3px;
        line-height: 1.1;
      }

      .print-kop-titles p {
        font-size: 7.5pt;
        color: #475569;
        margin: 1px 0 0 0;
        font-weight: 500;
      }

      .print-kop-badge {
        text-align: right;
      }

      .print-kop-badge .doc-class {
        background: #0F2942;
        color: #FFFFFF;
        font-size: 7pt;
        font-weight: 800;
        padding: 2px 7px;
        border-radius: 3px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        display: inline-block;
      }

      .print-kop-badge .sync-time {
        font-size: 7pt;
        color: #64748B;
        margin-top: 2px;
        font-weight: 600;
      }

      .print-action-title-box {
        background: #F8FAFC;
        border-left: 4px solid #0284C7;
        border: 1px solid #E2E8F0;
        border-left: 4px solid #0284C7;
        padding: 6px 10px;
        border-radius: 0 4px 4px 0;
        margin-bottom: 8px;
      }

      .print-action-title {
        font-size: 9.5pt;
        font-weight: 800;
        color: #0F2942;
        line-height: 1.25;
      }

      .print-exec-callouts {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 6px;
        margin-bottom: 8px;
      }

      .print-callout-item {
        background: #FFFFFF;
        border: 1px solid #CBD5E1;
        border-radius: 4px;
        padding: 5px 8px;
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
        font-size: 7.5pt;
        font-weight: 800;
        text-transform: uppercase;
        margin-bottom: 2px;
        display: flex;
        align-items: center;
        gap: 4px;
      }

      .print-callout-body {
        font-size: 6.8pt;
        color: #334155;
        line-height: 1.3;
      }

      .print-kpi-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 6px;
        margin-bottom: 8px;
      }

      .print-kpi-card {
        background: #FFFFFF;
        border: 1px solid #CBD5E1;
        border-radius: 4px;
        padding: 5px 8px;
      }

      .print-kpi-card.defisit {
        border-color: #F87171;
      }

      .print-kpi-label {
        font-size: 6.8pt;
        color: #64748B;
        font-weight: 700;
        text-transform: uppercase;
      }

      .print-kpi-val {
        font-size: 11.5pt;
        font-weight: 800;
        color: #0F2942;
        margin: 1px 0;
        font-variant-numeric: tabular-nums;
      }

      .print-kpi-sub {
        font-size: 6.5pt;
        color: #64748B;
      }

      .print-map-card {
        background: #FFFFFF;
        border: 1px solid #CBD5E1;
        border-radius: 4px;
        padding: 6px 8px;
      }

      .print-map-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 4px;
        border-bottom: 1px solid #E2E8F0;
        padding-bottom: 3px;
      }

      .print-map-title {
        font-size: 8pt;
        font-weight: 800;
        color: #0F2942;
      }

      .print-map-legend {
        display: flex;
        gap: 8px;
        font-size: 6.5pt;
        font-weight: 600;
        align-items: center;
      }

      .print-map-legend-dot {
        display: inline-block;
        width: 6px;
        height: 6px;
        border-radius: 50%;
        margin-right: 2px;
      }

      .print-wilayah-callouts-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 5px;
        margin-top: 6px;
      }

      .print-wilayah-chip {
        border: 1px solid #E2E8F0;
        border-radius: 4px;
        padding: 3px 5px;
        background: #F8FAFC;
      }

      .print-wilayah-chip.has-def {
        border-color: #FCA5A5;
        background: #FFF5F5;
      }

      .print-wilayah-name {
        font-size: 6.8pt;
        font-weight: 800;
        color: #0F2942;
        display: flex;
        justify-content: space-between;
      }

      .print-wilayah-stats {
        font-size: 6.2pt;
        color: #475569;
        margin-top: 1px;
        font-variant-numeric: tabular-nums;
      }

      .print-sub-footer {
        display: flex;
        justify-content: space-between;
        border-top: 1px solid #CBD5E1;
        padding-top: 3px;
        margin-top: 6px;
        font-size: 6.5pt;
        color: #64748B;
      }

      table.report-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 7pt;
        margin-bottom: 6px;
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
        padding: 3px 5px;
      }
      table.report-table th {
        background: #0F2942 !important;
        color: #FFFFFF !important;
        font-weight: 700;
        text-align: left;
        font-size: 6.8pt;
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
      }
      .badge-print-status {
        display: inline-block;
        padding: 1px 4px;
        border-radius: 3px;
        font-size: 6pt;
        font-weight: 800;
        text-transform: uppercase;
      }
      .badge-print-status.defisit { background: #FEE2E2; color: #DC2626; border: 1px solid #FCA5A5; }
      .badge-print-status.siaga { background: #FEF3C7; color: #D97706; border: 1px solid #FCD34D; }
      .badge-print-status.normal { background: #D1FAE5; color: #059669; border: 1px solid #6EE7B7; }
      .badge-print-status.unfilled { background: #F1F5F9; color: #64748B; border: 1px solid #CBD5E1; }
    }

    /* ========================================================= */
    /* 100% MOBILE RESPONSIVE STYLES (LAYAR HP < 768px)          */
    /* ========================================================= */
    .mobile-hamburger-btn {
      display: none;
    }
    .mobile-bottom-nav {
      display: none;
    }
    .mobile-menu-drawer {
      display: none;
    }

    @media (max-width: 768px) {
      html, body {
        overflow-x: hidden !important;
        width: 100% !important;
      }

      body {
        padding-bottom: 65px !important; /* Space for bottom nav */
      }

      .container {
        padding: 8px !important;
        width: 100% !important;
        box-sizing: border-box !important;
      }

      /* Header Mobile Compact */
      header {
        padding: 8px 12px !important;
        flex-wrap: nowrap !important;
        justify-content: space-between !important;
        gap: 6px !important;
      }

      .brand-section {
        gap: 8px !important;
        min-width: 0 !important;
        flex: 1 !important;
      }

      .pln-logo-box {
        width: 28px !important;
        height: 34px !important;
      }

      .brand-text h1 {
        font-size: 13px !important;
        white-space: nowrap !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
      }

      .brand-text p {
        display: none !important;
      }

      .badge-total {
        font-size: 9px !important;
        padding: 1px 5px !important;
      }

      /* Hide Desktop Header Controls */
      .header-controls .open-access-pill,
      .header-controls > div[style*="display:flex"],
      .header-controls button:not(.mobile-hamburger-btn) {
        display: none !important;
      }

      .header-controls .status-pill {
        font-size: 10px !important;
        padding: 3px 6px !important;
      }

      /* Show Mobile Hamburger */
      .mobile-hamburger-btn {
        display: flex !important;
        align-items: center;
        justify-content: center;
        background: #002E62 !important;
        color: #FFFFFF !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 6px !important;
        padding: 6px 10px !important;
        font-size: 15px !important;
        cursor: pointer;
      }

      /* Sub Bar Mobile */
      .sub-bar {
        display: none !important;
      }

      /* Active Filters Bar */
      .active-filters-bar {
        font-size: 10.5px !important;
        padding: 6px 8px !important;
      }

      /* 4 KPI Cards Grid Mobile (2 Columns) */
      .kpi-grid {
        grid-template-columns: repeat(2, 1fr) !important;
        gap: 8px !important;
      }

      .kpi-card {
        padding: 10px !important;
      }

      .kpi-title {
        font-size: 10px !important;
      }

      .kpi-value {
        font-size: 1.25rem !important;
      }

      .kpi-sub {
        font-size: 9.5px !important;
      }

      /* Horizontal Scrollable Unified Filter Toolbar */
      .filter-toolbar-unified {
        overflow-x: auto !important;
        white-space: nowrap !important;
        flex-wrap: nowrap !important;
        -webkit-overflow-scrolling: touch !important;
        padding: 8px !important;
        gap: 6px !important;
        justify-content: flex-start !important;
      }

      .filter-toolbar-unified .filter-group {
        flex-shrink: 0 !important;
      }

      /* Overview Layout Stacking */
      .overview-layout {
        display: flex !important;
        flex-direction: column !important;
        gap: 12px !important;
      }

      .map-container-box {
        width: 100% !important;
      }

      .map-island-nav {
        overflow-x: auto !important;
        white-space: nowrap !important;
        flex-wrap: nowrap !important;
        -webkit-overflow-scrolling: touch !important;
        padding: 6px !important;
      }

      .island-btn {
        flex-shrink: 0 !important;
        font-size: 10.5px !important;
        padding: 4px 8px !important;
      }

      .leaflet-map-wrapper {
        height: 360px !important;
      }

      /* Multi-System Interactive Coord Drawer as Bottom Sheet on Mobile */
      .coord-drawer {
        position: fixed !important;
        top: auto !important;
        bottom: 0 !important;
        left: 0 !important;
        right: 0 !important;
        width: 100% !important;
        height: 72vh !important;
        max-height: 72vh !important;
        border-radius: 18px 18px 0 0 !important;
        box-shadow: 0 -10px 30px rgba(0,0,0,0.3) !important;
        z-index: 1200 !important;
        transform: translateY(100%);
        transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
      }

      .coord-drawer.active {
        transform: translateY(0) !important;
      }

      /* Side Analytics Box */
      .side-analytics-box {
        width: 100% !important;
      }

      /* Regional & Province Cards Mobile 1-Column */
      .regional-grid,
      #provinceCardsContainer {
        grid-template-columns: 1fr !important;
        gap: 10px !important;
      }

      #provIslandChipsBar {
        overflow-x: auto !important;
        white-space: nowrap !important;
        flex-wrap: nowrap !important;
        -webkit-overflow-scrolling: touch !important;
        padding-bottom: 6px !important;
      }

      .island-chip {
        flex-shrink: 0 !important;
      }

      /* Floating Chatbot FAB positioned above Bottom Nav */
      .chatbot-fab {
        bottom: 68px !important;
        right: 14px !important;
        padding: 8px 14px !important;
        font-size: 11.5px !important;
      }

      .chatbot-drawer {
        width: 100% !important;
        height: 80vh !important;
        bottom: 0 !important;
        right: 0 !important;
        border-radius: 16px 16px 0 0 !important;
      }

      /* Mobile Bottom Navigation Bar */
      .mobile-bottom-nav {
        display: flex !important;
        position: fixed !important;
        bottom: 0 !important;
        left: 0 !important;
        right: 0 !important;
        height: 56px !important;
        background: #FFFFFF !important;
        border-top: 1px solid #E2E8F0 !important;
        z-index: 1000 !important;
        justify-content: space-around !important;
        align-items: center !important;
        box-shadow: 0 -2px 10px rgba(0,0,0,0.08) !important;
      }

      [data-theme="dark"] .mobile-bottom-nav {
        background: #0B1E36 !important;
        border-top-color: #1E3A5F !important;
      }

      .mob-nav-btn {
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        font-size: 10px !important;
        color: var(--text-muted) !important;
        cursor: pointer !important;
        padding: 4px 10px !important;
        font-weight: 600 !important;
        transition: all 0.15s ease !important;
      }

      .mob-nav-btn.active {
        color: #0284C7 !important;
        font-weight: 800 !important;
      }

      .mob-nav-btn .mob-icon {
        font-size: 16px !important;
        margin-bottom: 2px !important;
      }

      /* Mobile Navigation Menu Drawer */
      .mobile-menu-drawer {
        display: block !important;
        position: fixed !important;
        top: 0 !important;
        right: 0 !important;
        bottom: 0 !important;
        width: 290px !important;
        background: var(--bg-card) !important;
        border-left: 1px solid var(--border-color) !important;
        box-shadow: -5px 0 25px rgba(0,0,0,0.2) !important;
        z-index: 2000 !important;
        transform: translateX(100%);
        transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
        padding: 16px !important;
        box-sizing: border-box !important;
        overflow-y: auto !important;
      }

      .mobile-menu-drawer.active {
        transform: translateX(0) !important;
      }

      .mobile-drawer-header {
        display: flex !important;
        justify-content: space-between !important;
        align-items: center !important;
        padding-bottom: 12px !important;
        border-bottom: 1px solid var(--border-color) !important;
        margin-bottom: 14px !important;
      }

      .mobile-nav-item {
        display: flex !important;
        align-items: center !important;
        gap: 10px !important;
        padding: 10px 12px !important;
        border-radius: 8px !important;
        margin-bottom: 6px !important;
        background: var(--bg-card-alt) !important;
        border: 1px solid var(--border-color) !important;
        font-size: 12px !important;
        font-weight: 700 !important;
        color: var(--text-main) !important;
        cursor: pointer !important;
      }

      .mobile-nav-item:hover {
        border-color: #0284C7 !important;
      }
    }
"""

# Replace the existing print styles block with the refined print + mobile styles
p_start = html.find('/* ========================================================= */\n    /* MCKINSEY EXECUTIVE PRINT REPORT STYLES')
p_end = html.find('</style>', p_start)
if p_start != -1 and p_end != -1:
    html = html[:p_start] + css_additions.strip() + '\n  ' + html[p_end:]
    print("2. Replaced print styles with refined print + mobile responsive styles")
else:
    print("2. FAILED to locate print styles in <style>")

# 3. Add Hamburger Button and Print Appendix Checkbox to Header
header_btn_target = '<button class="btn btn-primary" onclick="printExecutiveReport()"'
header_addon = '''<!-- Print Appendix Checkbox -->
      <label class="print-opt-label" title="Centang untuk menyertakan lampiran detail 910 sistem saat cetak" style="display:inline-flex; align-items:center; gap:5px; font-size:11px; color:var(--text-muted); cursor:pointer;">
        <input type="checkbox" id="chkIncludeAppendix" onchange="window.includeAppendixInPrint = this.checked">
        <span style="font-weight:600;">+Lampiran 910 Sis</span>
      </label>

      <!-- Mobile Hamburger Button -->
      <button class="mobile-hamburger-btn" onclick="toggleMobileMenu()" id="btnMobileMenu" title="Menu Navigasi Mobile">
        <span>☰</span>
      </button>

      '''

if header_btn_target in html and 'id="chkIncludeAppendix"' not in html:
    html = html.replace(header_btn_target, header_addon + header_btn_target)
    print("3. Added appendix checkbox and mobile hamburger button to header")

# 4. Add IDs to key sections for smooth mobile navigation
if 'class="kpi-grid"' in html and 'id="kpiSection"' not in html:
    html = html.replace('class="kpi-grid"', 'class="kpi-grid" id="kpiSection"', 1)
    print("4. Added id='kpiSection' to main KPI grid")

if 'class="map-container-box"' in html and 'id="mapSection"' not in html:
    html = html.replace('class="map-container-box"', 'class="map-container-box" id="mapSection"', 1)
    print("4. Added id='mapSection' to map box")

if 'class="status-distribution-card" style="border-left: 3px solid #EF4444;"' in html:
    html = html.replace('class="status-distribution-card" style="border-left: 3px solid #EF4444;"', 'class="status-distribution-card" id="deficitSpotlightCard" style="border-left: 3px solid #EF4444;"')
    print("4. Added id='deficitSpotlightCard' to deficit spotlight card")

# 5. Add Mobile Drawer & Bottom Navigation Bar HTML before </body>
mobile_nav_html = '''
  <!-- Mobile Navigation Drawer -->
  <div id="mobileMenuDrawer" class="mobile-menu-drawer">
    <div class="mobile-drawer-header">
      <div style="display:flex; align-items:center; gap:8px;">
        <img src="/logo_pln.png" alt="PLN" style="width:24px; height:30px; object-fit:contain;">
        <span style="font-weight:800; font-size:13.5px; color:var(--text-main);">Navigasi Dashboard PLN</span>
      </div>
      <button class="btn btn-icon" onclick="toggleMobileMenu()">✕</button>
    </div>
    
    <div style="margin-bottom:14px;">
      <button class="btn btn-primary" onclick="printExecutiveReport(); toggleMobileMenu();" style="width:100%; justify-content:center; background:#0F2942; border-color:#0F2942; color:#fff; font-weight:700; margin-bottom:8px;">
        📄 Cetak Laporan Direksi
      </button>
      <label style="display:flex; align-items:center; gap:8px; font-size:11.5px; color:var(--text-muted); cursor:pointer;">
        <input type="checkbox" id="chkIncludeAppendixMob" onchange="document.getElementById('chkIncludeAppendix').checked = this.checked; window.includeAppendixInPrint = this.checked;">
        <span>Sertakan Lampiran 910 Sistem</span>
      </label>
    </div>

    <div style="margin-bottom:14px;">
      <div style="font-size:10px; font-weight:700; color:var(--text-dim); text-transform:uppercase; margin-bottom:6px;">Lompat ke Seksi:</div>
      <div class="mobile-nav-item" onclick="scrollToSection('kpiSection'); toggleMobileMenu();">
        <span>📊</span> 4 KPI Utama &amp; Status
      </div>
      <div class="mobile-nav-item" onclick="scrollToSection('mapSection'); toggleMobileMenu();">
        <span>🗺️</span> Peta Geografis 910 Sistem
      </div>
      <div class="mobile-nav-item" onclick="scrollToSection('deficitSpotlightCard'); toggleMobileMenu();">
        <span>🚨</span> Sorotan 51 Sistem Defisit
      </div>
      <div class="mobile-nav-item" onclick="scrollToSection('provSummaryCardBox'); toggleMobileMenu();">
        <span>🌐</span> Ringkasan Wilayah &amp; Provinsi
      </div>
      <div class="mobile-nav-item" onclick="switchTab('detail'); toggleMobileMenu();">
        <span>📑</span> Matriks Data Lengkap
      </div>
      <div class="mobile-nav-item" onclick="toggleChatbot(); toggleMobileMenu();">
        <span>⚡</span> Asisten AI PLN
      </div>
    </div>

    <div>
      <div style="font-size:10px; font-weight:700; color:var(--text-dim); text-transform:uppercase; margin-bottom:6px;">Aksi Tambahan:</div>
      <button class="btn" onclick="triggerManualRefresh(); toggleMobileMenu();" style="width:100%; margin-bottom:6px; justify-content:center;">
        🔄 Refresh Data Realtime
      </button>
      <button class="btn" onclick="copyNetworkIp(); toggleMobileMenu();" style="width:100%; margin-bottom:6px; justify-content:center;">
        🌐 Salin Akses Wi-Fi/LAN
      </button>
      <button class="btn" onclick="openSyncModal(); toggleMobileMenu();" style="width:100%; margin-bottom:6px; justify-content:center;">
        📁 Sumber Data SharePoint
      </button>
      <button class="btn" onclick="toggleTheme();" style="width:100%; justify-content:center;">
        🌙 Mode Gelap / Terang
      </button>
    </div>
  </div>

  <!-- Mobile Bottom Navigation Bar -->
  <nav class="mobile-bottom-nav" id="mobileBottomNav">
    <div class="mob-nav-btn active" id="mobNavKpi" onclick="mobileNavSelect(this, 'kpiSection')">
      <span class="mob-icon">📊</span>
      <span class="mob-label">KPI</span>
    </div>
    <div class="mob-nav-btn" id="mobNavMap" onclick="mobileNavSelect(this, 'mapSection')">
      <span class="mob-icon">🗺️</span>
      <span class="mob-label">Peta</span>
    </div>
    <div class="mob-nav-btn" id="mobNavDefisit" onclick="mobileNavSelect(this, 'deficitSpotlightCard')">
      <span class="mob-icon" style="color:#EF4444;">🚨</span>
      <span class="mob-label" style="color:#EF4444;">Defisit</span>
    </div>
    <div class="mob-nav-btn" id="mobNavWilayah" onclick="mobileNavSelect(this, 'provSummaryCardBox')">
      <span class="mob-icon">🌐</span>
      <span class="mob-label">Wilayah</span>
    </div>
    <div class="mob-nav-btn" id="mobNavChat" onclick="toggleChatbot()">
      <span class="mob-icon" style="color:var(--pln-yellow);">⚡</span>
      <span class="mob-label">AI PLN</span>
    </div>
  </nav>
'''

if 'id="mobileBottomNav"' not in html:
    html = html.replace('</body>', mobile_nav_html + '\n</body>')
    print("5. Added Mobile Drawer & Bottom Navigation Bar HTML")

with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("update_dashboard_v3.py COMPLETED successfully!")
