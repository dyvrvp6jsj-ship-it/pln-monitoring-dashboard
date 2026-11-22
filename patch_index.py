import re

with open('public/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add script tag for indonesia_map_paths.js in <head>
if '/indonesia_map_paths.js' not in content:
    content = content.replace(
        '<script src="/leaflet/leaflet.js"></script>',
        '<script src="/leaflet/leaflet.js"></script>\n  <script src="/indonesia_map_paths.js"></script>'
    )
    print("1. Added /indonesia_map_paths.js script tag")

# 2. Add print button in header
if 'printExecutiveReport()' not in content:
    target_btn = '<button class="btn" onclick="openSyncModal()" title="Lihat detail sumber SharePoint & unggah pembaruan">\n        <span>📁 Sumber Data</span>\n      </button>'
    replacement_btn = target_btn + '''\n\n      <button class="btn btn-primary" onclick="printExecutiveReport()" title="Cetak Laporan Direksi Resmi (McKinsey Style A4 Portrait)" style="background:#0F2942; border-color:#0F2942; color:#FFFFFF; font-weight:700; display:flex; align-items:center; gap:6px;">
        <span>📄 Cetak Laporan Direksi</span>
      </button>'''
    if target_btn in content:
        content = content.replace(target_btn, replacement_btn)
        print("2. Added Cetak Laporan Direksi button in header")
    else:
        print("2. FAILED to find target button in header")

# 3. Clean up hardcoded 57
replacements_57 = [
    ('<div class="kpi-value" style="color:#EF4444;" id="kpiDefisitVal">57 <span style="font-size:14px; font-weight:600;">Sistem</span></div>',
     '<div class="kpi-value" style="color:#EF4444;" id="kpiDefisitVal">51 <span style="font-size:14px; font-weight:600;">Sistem</span></div>'),
    ('<span class="status-badge defisit" id="mapDeficitBadge">57 Defisit</span>',
     '<span class="status-badge defisit" id="mapDeficitBadge">51 Defisit</span>'),
    ('<div class="island-btn" style="border-color:#EF4444; color:#EF4444; margin-left:auto;" onclick="zoomToDeficitSystems()">🚨 Fokus 57 Defisit</div>',
     '<div class="island-btn" id="btnFokusDefisitMap" style="border-color:#EF4444; color:#EF4444; margin-left:auto;" onclick="zoomToDeficitSystems()">🚨 Fokus <span id="btnFokusDefisitCount">51</span> Defisit</div>'),
    ('<strong style="color:#EF4444; font-size:16px;" id="countDefisit">57 Sistem</strong>',
     '<strong style="color:#EF4444; font-size:16px;" id="countDefisit">51 Sistem</strong>'),
    ('<span>🚨 Sorotan 57 Sistem Defisit</span>',
     '<span id="spotlightDeficitTitle">🚨 Sorotan <span id="spotlightDeficitCount">51</span> Sistem Defisit</span>'),
    ('<div class="kpi-value" style="color:#EF4444;">57 <span style="font-size:13px;">Sistem</span></div>',
     '<div class="kpi-value" style="color:#EF4444;"><span id="kpiDefisitValModal">51</span> <span style="font-size:13px;">Sistem</span></div>'),
    ('<button class="btn" id="btnFilterDefisit" onclick="setFilterStatus(\'defisit\')">🔴 Defisit (57)</button>',
     '<button class="btn" id="btnFilterDefisit" onclick="setFilterStatus(\'defisit\')">🔴 Defisit (<span id="filterDefisitCount">51</span>)</button>'),
    ('<li><strong>Sistem Defisit (57):</strong> Analisis sistem dengan cadangan daya negatif.</li>',
     '<li><strong>Sistem Defisit:</strong> Analisis sistem dengan cadangan daya negatif.</li>'),
    ('<div class="chat-chip" onclick="askQuickPrompt(\'Sistem mana saja yang mengalami defisit?\')">🔴 57 Sistem Defisit?</div>',
     '<div class="chat-chip" onclick="askQuickPrompt(\'Sistem mana saja yang mengalami defisit?\')">🔴 Analisis Sistem Defisit</div>'),
    ('showToast("Memfokuskan peta pada 57 sistem defisit");',
     'showToast("Memfokuskan peta pada sistem defisit");')
]

for old, new in replacements_57:
    if old in content:
        content = content.replace(old, new)
        print(f"Replaced 57: {old[:40]}...")
    else:
        print(f"Skipped/Not found: {old[:40]}...")

# 4. Fix summary section title id
old_title = '<span>🇮🇩 Ringkasan Daya &amp; Cadangan Berdasarkan Provinsi di Indonesia</span>\n              <span class="badge" style="background:#0284C7; color:#FFFFFF; font-size:11px; font-weight:800; padding:2px 8px; border-radius:12px;" id="provinceCountBadge">38 Provinsi</span>'
new_title = '<span id="summarySectionTitle">🇮🇩 Ringkasan Daya &amp; Cadangan Berdasarkan Provinsi di Indonesia</span>\n              <span class="badge" style="background:#0284C7; color:#FFFFFF; font-size:11px; font-weight:800; padding:2px 8px; border-radius:12px;" id="provinceCountBadge">35 Provinsi</span>'
if old_title in content:
    content = content.replace(old_title, new_title)
    print("4. Fixed summary title and badge IDs")

# 5. Fix CSS for .status-count-row and .regional-header
old_status_row = '''.status-count-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 9px 12px;
      border-radius: 6px;
      background: var(--bg-card-alt);
      margin-bottom: 8px;
      border: 1px solid var(--border-color);
      cursor: pointer;
      transition: all 0.2s ease;
    }'''

new_status_row = '''.status-count-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 10px;
      padding: 9px 12px;
      border-radius: 6px;
      background: var(--bg-card-alt);
      margin-bottom: 8px;
      border: 1px solid var(--border-color);
      cursor: pointer;
      transition: all 0.2s ease;
      min-width: 0;
    }

    .status-count-row > div:first-child {
      min-width: 0;
      flex: 1;
      overflow: hidden;
    }

    .status-count-row strong {
      flex-shrink: 0;
      white-space: nowrap;
      text-align: right;
    }'''

if old_status_row in content:
    content = content.replace(old_status_row, new_status_row)
    print("5. Fixed .status-count-row CSS")

old_regional_header = '''.regional-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 12px;
      padding-bottom: 8px;
      border-bottom: 1px solid var(--border-color);
    }

    .regional-title {
      font-size: 13px;
      font-weight: 700;
      color: var(--text-main);
    }'''

new_regional_header = '''.regional-header {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      gap: 8px;
      margin-bottom: 12px;
      padding-bottom: 8px;
      border-bottom: 1px solid var(--border-color);
    }

    .regional-title {
      font-size: 13px;
      font-weight: 700;
      color: var(--text-main);
      line-height: 1.35;
      flex: 1;
      min-width: 0;
    }

    .regional-header > span:last-child {
      white-space: nowrap;
      flex-shrink: 0;
      font-size: 10px;
      color: var(--text-dim);
      background: var(--bg-card-alt);
      padding: 2px 6px;
      border-radius: 4px;
      border: 1px solid var(--border-color);
    }'''

if old_regional_header in content:
    content = content.replace(old_regional_header, new_regional_header)
    print("6. Fixed .regional-header CSS")

with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Finished basic patches in index.html")
