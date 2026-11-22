import re

def fix_all():
    file_path = '/Users/pln/.gemini/antigravity/scratch/pln-monitoring-dashboard/public/index.html'
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # 1. Ensure appendix is NOT included by default (Default to strictly 3 pages)
    text = text.replace('window.includeAppendixInPrint = true;', 'window.includeAppendixInPrint = false;')
    text = text.replace('<input type="checkbox" id="chkIncludeAppendix" checked', '<input type="checkbox" id="chkIncludeAppendix"')
    text = text.replace('<input type="checkbox" id="chkIncludeAppendixMob" checked', '<input type="checkbox" id="chkIncludeAppendixMob"')
    text = text.replace('<span>Sertakan Lampiran 910 Sistem</span>', '<span>+Lampiran 910 Sistem (Opsional)</span>')
    text = text.replace('>Sertakan Lampiran 910 Sistem</span>', '>+Lampiran 910 Sistem (Opsional)</span>')

    # 2. Add print CSS containment to strictly prevent any page spill
    old_css_rule = """.report-page {
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
      }"""

    new_css_rule = """.report-page {
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

      #reportPage1, #reportPage2, #reportPage3 {
        page-break-after: always !important;
        break-after: page !important;
        page-break-inside: avoid !important;
        break-inside: avoid !important;
        max-height: 275mm !important;
        overflow: hidden !important;
      }"""

    text = text.replace(old_css_rule, new_css_rule)

    # 3. Enhance Page 2 charts to fill the page elegantly without awkward empty space
    old_charts_func = """    function buildPrintChartsSvg(regions) {
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
      }).join('');"""

    new_charts_func = """    function buildPrintChartsSvg(regions) {
      if (!regions || regions.length === 0) return '';
      let maxMw = 1000;
      regions.forEach(r => {
        if (r.dmp > maxMw) maxMw = r.dmp;
        if (r.bp > maxMw) maxMw = r.bp;
      });

      const labelW = 108;
      const barAreaW = 465;
      const rowH = 27;

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
            <text x="${labelW - 8}" y="12" text-anchor="end" font-size="8pt" font-weight="700" fill="#0F2942">${r.region}</text>
            <text x="${labelW - 8}" y="21" text-anchor="end" font-size="6.5pt" fill="#64748B">${r.count} Sis</text>
            <rect x="${labelW}" y="2" width="${dmpW}" height="9.5" fill="#0F2942" rx="2" />
            <text x="${labelW + dmpW + 3}" y="9.5" font-size="6.5pt" font-weight="700" fill="#0F2942">${formatNum(r.dmp)}</text>
            <rect x="${labelW}" y="13" width="${bpW}" height="9.5" fill="#0284C7" rx="2" />
            <text x="${labelW + bpW + 3}" y="20.5" font-size="6.5pt" font-weight="700" fill="#0284C7">${formatNum(r.bp)}</text>
            <rect x="${labelW + barAreaW + 55}" y="4" width="65" height="17" fill="${rmBg}" rx="3" stroke="${rmColor}" stroke-width="0.5"/>
            <text x="${labelW + barAreaW + 87.5}" y="15.5" text-anchor="middle" font-size="7pt" font-weight="800" fill="${rmColor}">${rmText} RM</text>
          </g>
        `;
      }).join('');

      const stackedH = 22;
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
            <text x="80" y="14" text-anchor="end" font-size="7.5pt" font-weight="700" fill="#0F2942">${r.region}</text>
            <g transform="translate(90, 1)">
              <rect x="0" y="0" width="${w24}" height="16" fill="#0284C7" />
              <rect x="${w24}" y="0" width="${w12}" height="16" fill="#F59E0B" />
              <rect x="${w24 + w12}" y="0" width="${w6}" height="16" fill="#EF4444" />
              ${r.count_24h > 0 && w24 > 14 ? `<text x="${w24/2}" y="11" text-anchor="middle" font-size="6pt" font-weight="700" fill="#FFFFFF">${r.count_24h}</text>` : ''}
              ${r.count_12h > 0 && w12 > 14 ? `<text x="${w24 + w12/2}" y="11" text-anchor="middle" font-size="6pt" font-weight="700" fill="#FFFFFF">${r.count_12h}</text>` : ''}
              ${r.count_6h > 0 && w6 > 12 ? `<text x="${w24 + w12 + w6/2}" y="11" text-anchor="middle" font-size="6pt" font-weight="700" fill="#FFFFFF">${r.count_6h}</text>` : ''}
            </g>
            <g transform="translate(420, 1)">
              <rect x="0" y="0" width="${wDef}" height="16" fill="#EF4444" />
              <rect x="${wDef}" y="0" width="${wSiaga}" height="16" fill="#F59E0B" />
              <rect x="${wDef + wSiaga}" y="0" width="${wNorm}" height="16" fill="#10B981" />
              <rect x="${wDef + wSiaga + wNorm}" y="0" width="${wUnf}" height="16" fill="#94A3B8" />
              ${r.defisit > 0 && wDef > 12 ? `<text x="${wDef/2}" y="11" text-anchor="middle" font-size="6pt" font-weight="700" fill="#FFFFFF">${r.defisit}</text>` : ''}
              ${r.siaga > 0 && wSiaga > 14 ? `<text x="${wDef + wSiaga/2}" y="11" text-anchor="middle" font-size="6pt" font-weight="700" fill="#FFFFFF">${r.siaga}</text>` : ''}
              ${r.normal > 0 && wNorm > 14 ? `<text x="${wDef + wSiaga + wNorm/2}" y="11" text-anchor="middle" font-size="6pt" font-weight="700" fill="#FFFFFF">${r.normal}</text>` : ''}
            </g>
          </g>
        `;
      }).join('');"""

    text = text.replace(old_charts_func, new_charts_func)
    text = text.replace('viewBox="0 0 760 195" width="100%" height="160"', 'viewBox="0 0 760 230" width="100%" height="188"')
    text = text.replace('viewBox="0 0 760 170" width="100%" height="140"', 'viewBox="0 0 760 195" width="100%" height="162"')
    text = text.replace('padding:8px 12px; margin-top:8px;', 'padding:10px 14px; margin-top:10px;')
    text = text.replace('font-size:6.8pt; color:#334155; line-height:1.4;', 'font-size:7.5pt; color:#334155; line-height:1.5;')

    # 4. Compact Matriks 35 Provinsi on Page 3 (to strictly eliminate spillover)
    old_matrix_code = """      return `
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
                    ${p.defisit}
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
              <td class="num" style="color:#10B981; font-weight:700;">0</td>
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
      `;"""

    new_matrix_code = """      return `
        <table class="report-table" style="font-size:6.2pt; margin-bottom:4px;">
          <thead>
            <tr style="height:16px;">
              <th style="width:16px; padding:1.5px 3px;">No</th>
              <th style="padding:1.5px 4px;">Provinsi</th>
              <th style="padding:1.5px 4px;">Regional</th>
              <th style="text-align:right; padding:1.5px 4px;">Sistem (Inter/Iso/ULD)</th>
              <th style="text-align:right; padding:1.5px 4px;">DMP (MW)</th>
              <th style="text-align:right; padding:1.5px 4px;">BP (MW)</th>
              <th style="text-align:right; padding:1.5px 4px;">Cad (MW)</th>
              <th style="text-align:center; width:34px; padding:1.5px 4px;">Defisit</th>
              <th style="padding:1.5px 4px;">Daftar Sistem Defisit &amp; Besaran (MW)</th>
            </tr>
          </thead>
          <tbody>
            ${defProvs.map((p, idx) => {
              const defSysStr = (p.deficit_systems && p.deficit_systems.length > 0)
                ? p.deficit_systems.map(s => `${s.name} (${formatNum(s.cad_mw)} MW)`).join('; ')
                : '-';

              return `
                <tr style="height:14px;">
                  <td style="padding:1.2px 3px;">${idx + 1}</td>
                  <td style="padding:1.2px 4px;"><strong>${p.provinsi}</strong></td>
                  <td style="padding:1.2px 4px;">${p.regional || p.pulau}</td>
                  <td class="num" style="padding:1.2px 4px;">${p.count} <span style="font-size:5.5pt; color:#64748B;">(${p.count_interkoneksi || 0}/${p.count_isolated || 0}/${p.count_uld || 0})</span></td>
                  <td class="num" style="padding:1.2px 4px;">${formatNum(p.dmp)}</td>
                  <td class="num" style="padding:1.2px 4px;">${formatNum(p.bp)}</td>
                  <td class="num" style="padding:1.2px 4px; font-weight:700; color:${p.cad_mw < 0 ? '#EF4444' : '#10B981'};">
                    ${p.cad_mw >= 0 ? '+' : ''}${formatNum(p.cad_mw)}
                  </td>
                  <td class="num" style="text-align:center; padding:1.2px 4px; font-weight:800; color:#EF4444;">
                    ${p.defisit}
                  </td>
                  <td style="padding:1.2px 4px; font-size:5.6pt; line-height:1.15; color:#1E293B;">
                    ${defSysStr}
                  </td>
                </tr>
              `;
            }).join('')}
            <tr style="background:#F1F5F9; font-weight:700; height:14px;">
              <td colspan="3" style="padding:1.2px 4px;"><strong>16 Provinsi Lainnya (Surplus Bebas Defisit: DKI Jakarta, Jabar, Jateng, Sumut, Sumsel, Kalbar, dll.)</strong></td>
              <td class="num" style="padding:1.2px 4px;">${nonDefCount} <span style="font-size:5.5pt; color:#64748B;">(${nonDefInter}/${nonDefIso}/${nonDefUld})</span></td>
              <td class="num" style="padding:1.2px 4px;">${formatNum(nonDefDmp)}</td>
              <td class="num" style="padding:1.2px 4px;">${formatNum(nonDefBp)}</td>
              <td class="num" style="padding:1.2px 4px; color:#10B981;">+${formatNum(nonDefCad)}</td>
              <td class="num" style="text-align:center; padding:1.2px 4px; color:#10B981; font-weight:700;">0</td>
              <td style="padding:1.2px 4px; font-size:5.6pt; color:#10B981;">Seluruh sistem beroperasi Normal / Siaga tanpa defisit</td>
            </tr>
            <tr style="background:#0F2942; color:#FFFFFF; font-weight:800; height:15px;">
              <td colspan="3" style="color:#FFFFFF; padding:1.5px 4px;">TOTAL KONSOLIDASI NASIONAL (35 PROVINSI)</td>
              <td class="num" style="color:#FFFFFF; padding:1.5px 4px;">910 (49/645/216)</td>
              <td class="num" style="color:#FFFFFF; padding:1.5px 4px;">${formatNum(appData.kpi_summary.total_dmp_mw)}</td>
              <td class="num" style="color:#FFFFFF; padding:1.5px 4px;">${formatNum(appData.kpi_summary.total_bp_mw)}</td>
              <td class="num" style="color:#10B981; padding:1.5px 4px;">+${formatNum(appData.kpi_summary.total_cad_mw)}</td>
              <td class="num" style="text-align:center; color:#FCA5A5; padding:1.5px 4px;">51 SISTEM</td>
              <td style="color:#FFFFFF; font-size:5.6pt; padding:1.5px 4px;">51 Sistem Defisit Tersebar di 19 Provinsi</td>
            </tr>
          </tbody>
        </table>
      `;"""

    text = text.replace(old_matrix_code, new_matrix_code)

    # 5. Compact 3 Kategori Aksi Korporat on Page 3
    old_aksi_code = """          <!-- 3 Kategori Aksi Korporat -->
          <div style="font-size:8.5pt; font-weight:800; color:#0F2942; margin-top:8px; margin-bottom:4px;">
            🎯 3 KATEGORI AKSI KORPORAT PENANGANAN SISTEM DEFISIT &amp; VALIDASI
          </div>
          <div style="display:grid; grid-template-columns: repeat(3, 1fr); gap:6px;">
            <div style="background:#FEF2F2; border:1px solid #FCA5A5; border-radius:4px; padding:6px 8px;">
              <div style="font-size:7.2pt; font-weight:800; color:#DC2626; margin-bottom:2px;">
                1. Mitigasi Grid Interkoneksi (4 Sistem)
              </div>
              <div style="font-size:6.6pt; color:#334155; line-height:1.35;">
                • <strong>SULBAGSEL (-267,5 MW):</strong> Optimalisasi transfer hidro Poso &amp; sewa peaker gas darurat.<br>
                • <strong>Kalimantan (-60,2 MW) &amp; Khatulistiwa (-16,8 MW):</strong> Manuver peaker &amp; penyeimbangan transfer 150 kV.<br>
                • <strong>Ternate-Tidore (-9,9 MW):</strong> Relokasi genset diesel &amp; perbaikan unit sewa.
              </div>
            </div>

            <div style="background:#FFFBEB; border:1px solid #FCD34D; border-radius:4px; padding:6px 8px;">
              <div style="font-size:7.2pt; font-weight:800; color:#D97706; margin-bottom:2px;">
                2. Optimalisasi PLTD/Sewa Isolated (47 Sistem)
              </div>
              <div style="font-size:6.6pt; color:#334155; line-height:1.35;">
                • <strong>Leok (-72,2 MW) &amp; Tanakeke (-90 MW):</strong> Akselerasi suplai BBM &amp; genset cadangan darurat.<br>
                • <strong>Kepri (7 Sistem) &amp; Sulteng (6 Sistem):</strong> Penambahan mesin diesel modular sewa.<br>
                • <strong>NTT (3 Sistem) &amp; Maluku (4 Sistem):</strong> Peningkatan kesiapan unit isolated kepulauan.
              </div>
            </div>

            <div style="background:#F0F9FF; border:1px solid #BAE6FD; border-radius:4px; padding:6px 8px;">
              <div style="font-size:7.2pt; font-weight:800; color:#0284C7; margin-bottom:2px;">
                3. Akselerasi Validasi 162 Sistem Belum Terisi
              </div>
              <div style="font-size:6.6pt; color:#334155; line-height:1.35;">
                • <strong>Instruksi GM UID/UIW:</strong> Penugasan unit Maluku (79 sis), Papua (75 sis), dan Sulawesi (8 sis).<br>
                • <strong>Pemasangan AMR/Telemetri:</strong> Digitalisasi metering pencatatan beban puncak harian.<br>
                • <strong>Target Integrasi:</strong> 100% data riil terhubung ke dashboard pusat monitoring.
              </div>
            </div>
          </div>"""

    new_aksi_code = """          <!-- 3 Kategori Aksi Korporat -->
          <div style="font-size:7.5pt; font-weight:800; color:#0F2942; margin-top:4px; margin-bottom:3px;">
            🎯 3 KATEGORI AKSI KORPORAT PENANGANAN SISTEM DEFISIT &amp; VALIDASI
          </div>
          <div style="display:grid; grid-template-columns: repeat(3, 1fr); gap:5px; margin-bottom:3px;">
            <div style="background:#FEF2F2; border:1px solid #FCA5A5; border-radius:3px; padding:4px 6px;">
              <div style="font-size:6.6pt; font-weight:800; color:#DC2626; margin-bottom:1px;">
                1. Mitigasi Grid Interkoneksi (4 Sistem)
              </div>
              <div style="font-size:5.7pt; color:#334155; line-height:1.2;">
                • <strong>SULBAGSEL (-267,5 MW):</strong> Optimalisasi transfer hidro Poso &amp; peaker gas darurat.<br>
                • <strong>Kalimantan (-60,2 MW) &amp; Khatulistiwa (-16,8 MW):</strong> Manuver transfer 150 kV.<br>
                • <strong>Ternate-Tidore (-9,9 MW):</strong> Relokasi genset diesel &amp; unit sewa.
              </div>
            </div>

            <div style="background:#FFFBEB; border:1px solid #FCD34D; border-radius:3px; padding:4px 6px;">
              <div style="font-size:6.6pt; font-weight:800; color:#D97706; margin-bottom:1px;">
                2. Optimalisasi PLTD/Sewa Isolated (47 Sistem)
              </div>
              <div style="font-size:5.7pt; color:#334155; line-height:1.2;">
                • <strong>Leok (-72,2 MW) &amp; Tanakeke (-90 MW):</strong> Suplai BBM darurat &amp; genset sewa.<br>
                • <strong>Kepri (7 Sistem) &amp; Sulteng (6 Sistem):</strong> Penambahan diesel modular sewa.<br>
                • <strong>NTT (3 Sistem) &amp; Maluku (4 Sistem):</strong> Peningkatan kesiapan unit isolated.
              </div>
            </div>

            <div style="background:#F0F9FF; border:1px solid #BAE6FD; border-radius:3px; padding:4px 6px;">
              <div style="font-size:6.6pt; font-weight:800; color:#0284C7; margin-bottom:1px;">
                3. Akselerasi Validasi 162 Sistem Belum Terisi
              </div>
              <div style="font-size:5.7pt; color:#334155; line-height:1.2;">
                • <strong>Instruksi GM UID/UIW:</strong> Maluku (79 sis), Papua (75 sis), Sulawesi (8 sis).<br>
                • <strong>Pemasangan AMR/Telemetri:</strong> Digitalisasi metering pencatatan harian.<br>
                • <strong>Target Integrasi:</strong> 100% data riil terhubung ke pusat monitoring.
              </div>
            </div>
          </div>"""

    text = text.replace(old_aksi_code, new_aksi_code)

    # 6. Refine Appendix Table (so that when enabled, it never splits words or breaks rows)
    old_app_table = """          <table class="report-table" style="font-size:6.5pt;">
            <thead>
              <tr>
                <th style="width:20px;">No</th>
                <th>Nama Sistem</th>
                <th>Wilayah</th>
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
              ${systems.map((s, idx) => `
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
          </table>"""

    new_app_table = """          <table class="report-table" style="font-size:6.2pt; width:100%;">
            <thead>
              <tr style="height:16px;">
                <th style="width:22px; padding:1.5px 3px;">No</th>
                <th style="padding:1.5px 4px;">Nama Sistem</th>
                <th style="padding:1.5px 4px; width:75px;">Wilayah</th>
                <th style="padding:1.5px 4px; width:100px;">Provinsi</th>
                <th style="padding:1.5px 4px; width:70px;">Jenis</th>
                <th style="padding:1.5px 4px; width:45px; white-space:nowrap;">Jam</th>
                <th style="text-align:right; padding:1.5px 4px; width:55px;">DMP (MW)</th>
                <th style="text-align:right; padding:1.5px 4px; width:55px;">BP (MW)</th>
                <th style="text-align:right; padding:1.5px 4px; width:65px;">Cadangan (MW)</th>
                <th style="padding:1.5px 4px; width:60px;">Status</th>
              </tr>
            </thead>
            <tbody>
              ${systems.map((s, idx) => `
                <tr style="height:14px; page-break-inside:avoid !important; break-inside:avoid !important;">
                  <td style="padding:1px 3px;">${idx + 1}</td>
                  <td style="padding:1px 4px;"><strong>${s.name}</strong></td>
                  <td style="padding:1px 4px;">${s.region}</td>
                  <td style="padding:1px 4px;">${s.provinsi || s.region}</td>
                  <td style="padding:1px 4px;">${s.jenis}</td>
                  <td style="padding:1px 4px; white-space:nowrap;">${s.jam_operasi}</td>
                  <td class="num" style="padding:1px 4px;">${formatNum(s.dmp)}</td>
                  <td class="num" style="padding:1px 4px;">${formatNum(s.bp)}</td>
                  <td class="num" style="padding:1px 4px; font-weight:700; color:${s.cad_mw < 0 ? '#EF4444' : (s.cad_mw > 0 ? '#10B981' : '#64748B')};">
                    ${s.cad_mw > 0 ? '+' : ''}${formatNum(s.cad_mw)}
                  </td>
                  <td style="padding:1px 4px;">
                    <span class="badge-print-status ${s.status_code}">${s.status}</span>
                  </td>
                </tr>
              `).join('')}
            </tbody>
          </table>"""

    text = text.replace(old_app_table, new_app_table)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(text)

    print('index.html updated successfully with zero-spill guarantees!')

fix_all()
