with open('public/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

old_set_summary = '''function setSummaryViewMode(mode) {
      currentSummaryViewMode = mode;
      const btnProv = document.getElementById('btnViewProvinsi');
      const btnReg = document.getElementById('btnViewRegional');
      if (btnProv) btnProv.classList.toggle('active', mode === 'provinsi');
      if (btnReg) btnReg.classList.toggle('active', mode === 'regional');
      
      const provContainer = document.getElementById('provinceCardsContainer');
      const regContainer = document.getElementById('regionalCardsContainer');
      const islandChips = document.getElementById('provIslandChipsBar');
      const searchBox = document.getElementById('provSearchInput');

      if (mode === 'provinsi') {
        if (provContainer) provContainer.style.display = 'grid';
        if (regContainer) regContainer.style.display = 'none';
        if (islandChips) islandChips.style.display = 'flex';
        if (searchBox) searchBox.style.display = 'block';
      } else {
        if (provContainer) provContainer.style.display = 'none';
        if (regContainer) regContainer.style.display = 'grid';
        if (islandChips) islandChips.style.display = 'none';
        if (searchBox) searchBox.style.display = 'none';
      }
    }'''

new_set_summary = '''function setSummaryViewMode(mode) {
      currentSummaryViewMode = mode;
      const btnProv = document.getElementById('btnViewProvinsi');
      const btnReg = document.getElementById('btnViewRegional');
      if (btnProv) btnProv.classList.toggle('active', mode === 'provinsi');
      if (btnReg) btnReg.classList.toggle('active', mode === 'regional');
      
      const provContainer = document.getElementById('provinceCardsContainer');
      const regContainer = document.getElementById('regionalCardsContainer');
      const islandChips = document.getElementById('provIslandChipsBar');
      const searchBox = document.getElementById('provSearchInput');
      const titleSpan = document.getElementById('summarySectionTitle');
      const badgeSpan = document.getElementById('provinceCountBadge');

      if (mode === 'provinsi') {
        if (provContainer) provContainer.style.display = 'grid';
        if (regContainer) regContainer.style.display = 'none';
        if (islandChips) islandChips.style.display = 'flex';
        if (searchBox) searchBox.style.display = 'block';
        if (titleSpan) titleSpan.innerText = '🇮🇩 Ringkasan Daya & Cadangan Berdasarkan Provinsi di Indonesia';
        if (badgeSpan) badgeSpan.innerText = ((appData && appData.provinces) ? appData.provinces.length : 35) + ' Provinsi';
      } else {
        if (provContainer) provContainer.style.display = 'none';
        if (regContainer) regContainer.style.display = 'grid';
        if (islandChips) islandChips.style.display = 'none';
        if (searchBox) searchBox.style.display = 'none';
        if (titleSpan) titleSpan.innerText = '🌐 Ringkasan Daya & Cadangan Berdasarkan Wilayah Regional';
        if (badgeSpan) badgeSpan.innerText = '7 Wilayah';
      }
    }'''

if old_set_summary in c:
    c = c.replace(old_set_summary, new_set_summary)
    print("Replaced setSummaryViewMode successfully")
else:
    print("old_set_summary not found")

old_kpi_def = "document.getElementById('kpiDefisitVal').innerHTML = `${kpi.status_counts.defisit} <span style=\"font-size:14px; font-weight:600;\">Sistem</span>`;"
new_kpi_def = '''document.getElementById('kpiDefisitVal').innerHTML = `${kpi.status_counts.defisit} <span style="font-size:14px; font-weight:600;">Sistem</span>`;
      const defCountVal = kpi.status_counts.defisit;
      if (document.getElementById('btnFokusDefisitCount')) document.getElementById('btnFokusDefisitCount').innerText = defCountVal;
      if (document.getElementById('spotlightDeficitCount')) document.getElementById('spotlightDeficitCount').innerText = defCountVal;
      if (document.getElementById('filterDefisitCount')) document.getElementById('filterDefisitCount').innerText = defCountVal;
      if (document.getElementById('kpiDefisitValModal')) document.getElementById('kpiDefisitValModal').innerText = defCountVal;
      if (document.getElementById('mapDeficitBadge')) document.getElementById('mapDeficitBadge').innerText = `${defCountVal} Defisit`;'''

if old_kpi_def in c:
    c = c.replace(old_kpi_def, new_kpi_def)
    print("Replaced kpiDefisitVal in renderDashboard successfully")
else:
    print("old_kpi_def not found")

with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(c)
