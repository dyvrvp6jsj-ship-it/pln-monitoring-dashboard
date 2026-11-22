with open('/Users/pln/.gemini/antigravity/scratch/pln-monitoring-dashboard/public/index.html') as f:
    html = f.read()

checks = [
    ('Download Report button', '📥 Download Report' in html),
    ('Checkbox checked default', 'id="chkIncludeAppendix" checked' in html),
    ('Checkbox label', 'Sertakan Lampiran 910 Sistem' in html),
    ('REPORT Kop badge', '<span class="doc-class">REPORT</span>' in html),
    ('Precision bounds', 'min_lng: 94.8, max_lng: 141.2, min_lat: -11.2, max_lat: 6.2' in html),
    ('Clean deficit number (no red circle emoji in table)', '🔴 ${p.defisit}' not in html),
    ('Clean 0 in surplus (no square root symbol)', '✓ 0' not in html),
    ('Near zero negative formatting', "return '-0,04';" in html),
    ('Bab 4 Lampiran heading', 'BAB 4 (LAMPIRAN)' in html),
    ('Report footer text', 'Report — Monitoring 910 Sistem Kelistrikan Nasional PLN' in html),
    ('Clean action categories (no emoji prefix 41. / 12.)', '1. Mitigasi Grid Interkoneksi' in html and '⚡ 1. Mitigasi' not in html),
]

for name, passed in checks:
    print(f'[{ "PASS" if passed else "FAIL" }] {name}')
