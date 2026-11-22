def sync_report_preview_html():
    file_path = '/Users/pln/.gemini/antigravity/scratch/pln-monitoring-dashboard/public/report_preview.html'
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # Add @page and update print CSS
    old_css = """    @media print {
      body { background: #FFFFFF; padding: 0; gap: 0; }
      .report-page-preview {
        box-shadow: none;
        border-radius: 0;
        width: 100%;
        max-height: 275mm !important;
        overflow: hidden !important;
        padding: 0 0 5mm 0;
        page-break-after: always !important;
        break-after: page !important;
        page-break-inside: avoid !important;
        break-inside: avoid !important;
      }
      .no-print { display: none !important; }
    }"""

    new_css = """    @page {
      size: A4 portrait;
      margin: 8mm 10mm;
    }
    @media print {
      html, body {
        background: #FFFFFF !important;
        padding: 0 !important;
        margin: 0 !important;
        gap: 0 !important;
      }
      .report-page-preview {
        box-shadow: none !important;
        border-radius: 0 !important;
        width: 100% !important;
        min-height: auto !important;
        height: auto !important;
        max-height: 275mm !important;
        overflow: hidden !important;
        padding: 0 !important;
        page-break-after: always !important;
        break-after: page !important;
        page-break-inside: avoid !important;
        break-inside: avoid !important;
      }
      .report-page-preview:last-child {
        page-break-after: auto !important;
        break-after: auto !important;
      }
      .no-print { display: none !important; }
    }"""

    text = text.replace(old_css, new_css)

    # In top toolbar of report_preview.html, show clear status: 3 Halaman Eksekutif
    old_top_bar = """  <div class="no-print" style="width:210mm; display:flex; justify-content:space-between; align-items:center; background:#FFFFFF; padding:12px 20px; border-radius:8px; box-shadow:0 4px 15px rgba(0,0,0,0.08);">
    <div style="font-weight:700; color:#0F2942; font-size:14px;">📄 Pratinjau Dokumen Eksekutif Direksi (A4 Portrait)</div>
    <button onclick="window.print()" style="background:#0F2942; color:#FFFFFF; border:none; padding:8px 18px; border-radius:6px; font-weight:700; cursor:pointer;">🖨️ Cetak / Simpan PDF</button>
  </div>"""

    new_top_bar = """  <div class="no-print" style="width:210mm; display:flex; justify-content:space-between; align-items:center; background:#FFFFFF; padding:12px 20px; border-radius:8px; box-shadow:0 4px 15px rgba(0,0,0,0.08);">
    <div>
      <div style="font-weight:800; color:#0F2942; font-size:14px;">📄 Pratinjau Laporan Resmi Direksi (Tepat 3 Halaman A4 Portrait)</div>
      <div style="font-size:11px; color:#64748B; margin-top:2px;">Dokumen padat eksekutif • Bebas halaman kosong meluber • Nol teks terpotong</div>
    </div>
    <div style="display:flex; align-items:center; gap:12px;">
      <button onclick="window.print()" style="background:#0F2942; color:#FFFFFF; border:none; padding:8px 18px; border-radius:6px; font-weight:700; cursor:pointer; font-size:12.5px; display:flex; align-items:center; gap:6px;">
        <span>📥 Download / Cetak PDF (3 Halaman)</span>
      </button>
    </div>
  </div>"""

    text = text.replace(old_top_bar, new_top_bar)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(text)

    print('report_preview.html synced successfully!')

sync_report_preview_html()
