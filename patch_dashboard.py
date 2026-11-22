import os

html_path = '/Users/pln/.gemini/antigravity/scratch/pln-monitoring-dashboard/public/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Add CSS for shared coordinate marker and filter button disabled state
css_target = '/* Radar Marker for Deficit */'
css_replacement = '''/* Shared Coordinates Marker & Divicon */
    .shared-coord-badge {
      background: #002E62;
      border: 1.8px solid #00A3E0;
      color: #FFFFFF;
      border-radius: 14px;
      padding: 2px 8px;
      font-size: 11px;
      font-weight: 800;
      display: inline-flex;
      align-items: center;
      gap: 4px;
      box-shadow: 0 0 10px rgba(0, 163, 224, 0.65);
      cursor: pointer;
      white-space: nowrap;
      transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    .shared-coord-badge:hover {
      transform: scale(1.1);
      box-shadow: 0 0 14px rgba(0, 163, 224, 0.9);
    }
    .shared-coord-badge.has-deficit {
      border-color: #EF4444;
      background: #991B1B;
      box-shadow: 0 0 12px rgba(239, 68, 68, 0.85);
    }
    .filter-btn-pill.disabled {
      opacity: 0.55;
      cursor: not-allowed !important;
      border-style: dashed;
    }

    /* Radar Marker for Deficit */'''

assert css_target in html, 'CSS target not found'
html = html.replace(css_target, css_replacement, 1)

# 2. Replace filter-section-bar
p1 = html.find('<div class="filter-section-bar">')
p2 = html.find('<!-- Interactive KPI Summary Cards -->', p1)
assert p1 != -1 and p2 != -1, 'filter-section-bar block not found'

new_filter_bar = '''<!-- Interactive Classification Bar (Kategori Sistem & Jam Operasi) -->
      <div class="filter-section-bar" style="flex-direction:column; align-items:stretch; gap:10px;">
        
        <!-- Row 1: Kategori Sistem (Workbook Resmi) -->
        <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
          <span class="filter-group-label" style="min-width:135px;">⚡ KATEGORI:</span>
          <div class="filter-btn-pill active" id="btnCatAll" onclick="setFilterCategory('all')">
            <span>Semua</span>
            <span class="badge-pill-count" id="badgeCatAll">910</span>
          </div>
          <div class="filter-btn-pill" id="btnCatInterkoneksi" onclick="setFilterCategory('interkoneksi')">
            <span>⚡ Interkoneksi</span>
            <span class="badge-pill-count" id="badgeCatInter">49</span>
          </div>
          <div class="filter-btn-pill disabled" id="btnCatInterkoneksiKecil" onclick="setFilterCategory('interkoneksi_kecil')" title="Belum ada klasifikasi tersendiri di workbook 910 sistem">
            <span>⚡ Interkoneksi Kecil</span>
            <span class="badge-pill-count" style="background:#475569;">0</span>
          </div>
          <div class="filter-btn-pill" id="btnCatIsolated24" onclick="setFilterCategory('isolated_24h')">
            <span>🏝️ Isolated 24 Jam</span>
            <span class="badge-pill-count" id="badgeCatIso24">412</span>
          </div>
          <div class="filter-btn-pill" id="btnCatIsolated12" onclick="setFilterCategory('isolated_12h')">
            <span>🏝️ Isolated 12 Jam</span>
            <span class="badge-pill-count" id="badgeCatIso12">197</span>
          </div>
          <div class="filter-btn-pill" id="btnCatIsolated6" onclick="setFilterCategory('isolated_6h')">
            <span>🏝️ Isolated 6 Jam</span>
            <span class="badge-pill-count" id="badgeCatIso6">36</span>
          </div>
          <div class="filter-btn-pill" id="btnCatUldAll" onclick="setFilterCategory('uld_all')">
            <span>🏘️ ULD Semua</span>
            <span class="badge-pill-count" id="badgeCatUldAll">216</span>
          </div>
          <div class="filter-btn-pill" id="btnCatUld24" onclick="setFilterCategory('uld_24h')">
            <span>🏘️ ULD 24 Jam</span>
            <span class="badge-pill-count" id="badgeCatUld24">76</span>
          </div>
          <div class="filter-btn-pill" id="btnCatUld12" onclick="setFilterCategory('uld_12h')">
            <span>🏘️ ULD 12 Jam</span>
            <span class="badge-pill-count" id="badgeCatUld12">108</span>
          </div>
          <div class="filter-btn-pill" id="btnCatUld6" onclick="setFilterCategory('uld_6h')">
            <span>🏘️ ULD 6 Jam</span>
            <span class="badge-pill-count" id="badgeCatUld6">32</span>
          </div>
        </div>

        <!-- Row 2: Jam Operasi Terpisah (Semua Jenis) -->
        <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
          <span class="filter-group-label" style="min-width:135px;">⏱️ JAM OPERASI:</span>
          <div class="filter-btn-pill active" id="btnPillJamAll" onclick="setFilterJam('all')">
            <span>Semua Jam</span>
            <span class="badge-pill-count">910</span>
          </div>
          <div class="filter-btn-pill" id="btnPillJam24" onclick="setFilterJam('24h')">
            <span>⏱️ 24 Jam (Semua)</span>
            <span class="badge-pill-count" id="badgeCount24h">537</span>
          </div>
          <div class="filter-btn-pill" id="btnPillJam12" onclick="setFilterJam('12h')">
            <span>🌙 12 Jam (Semua)</span>
            <span class="badge-pill-count" id="badgeCount12h">305</span>
          </div>
          <div class="filter-btn-pill" id="btnPillJam6" onclick="setFilterJam('6h')">
            <span>⚡ 6 Jam (Semua)</span>
            <span class="badge-pill-count" id="badgeCount6h">68</span>
          </div>
        </div>

      </div>\n      '''

html = html[:p1] + new_filter_bar + html[p2:]

# 3. Replace map-island-nav
p1 = html.find('<div class="map-island-nav">')
p2 = html.find('<div id="leafletMap"', p1)
assert p1 != -1 and p2 != -1, 'map-island-nav block not found'

new_island_nav = '''<div class="map-island-nav">
            <span style="font-size:10px; color:var(--text-dim); margin-right:4px;">NAVIGASI &amp; WILAYAH:</span>
            <div class="island-btn active" id="btnMapAll" onclick="zoomToIsland('all')">🇮🇩 Semua (910)</div>
            <div class="island-btn" id="btnMapJawa" onclick="zoomToIsland('jawa')">⚡ Jawa-Bali (44)</div>
            <div class="island-btn" id="btnMapSumatera" onclick="zoomToIsland('sumatera')">🌴 Sumatera (188)</div>
            <div class="island-btn" id="btnMapKalimantan" onclick="zoomToIsland('kalimantan')">🌲 Kalimantan (89)</div>
            <div class="island-btn" id="btnMapSulawesi" onclick="zoomToIsland('sulawesi')">🌊 Sulawesi (89)</div>
            <div class="island-btn" id="btnMapNusa" onclick="zoomToIsland('nusa')">🏝️ Nusa Tenggara (74)</div>
            <div class="island-btn" id="btnMapMaluku" onclick="zoomToIsland('maluku')">⛰️ Maluku (168)</div>
            <div class="island-btn" id="btnMapPapua" onclick="zoomToIsland('papua')" style="border-color:var(--pln-cyan); color:var(--pln-cyan); font-weight:700;">🦅 Papua (258)</div>
            <div class="island-btn" style="border-color:#EF4444; color:#EF4444; margin-left:auto;" onclick="zoomToDeficitSystems()">🚨 Fokus 57 Defisit</div>
          </div>\n          '''

html = html[:p1] + new_island_nav + html[p2:]

# 4. Replace filters and ISLAND_COORDINATES block
p1 = html.find('// Filters\n    let currentFilterStatus =')
p2 = html.find('function formatNum(n)', p1)
assert p1 != -1 and p2 != -1, 'filters and island coordinates block not found'

new_filters_block = '''// Filters State
    let currentFilterStatus = 'all'; // 'all', 'defisit', 'siaga', 'normal', 'unfilled'
    let currentFilterCategory = 'all'; // 'all', 'interkoneksi', 'isolated_24h', 'isolated_12h', 'isolated_6h', 'uld_all', 'uld_24h', 'uld_12h', 'uld_6h'
    let currentFilterJenis = 'all';  // backward-compatible
    let currentFilterJam = 'all';    // 'all', '24h', '12h', '6h'
    let currentFilterIsland = 'all'; // 'all', 'sumatera', 'jawa', 'kalimantan', 'sulawesi', 'maluku', 'papua', 'nusa'
    let currentFilterRegion = null;
    let currentSearchQuery = '';

    // Pagination
    let currentPage = 1;
    let pageSize = 50;
    let sortColumn = 'no';
    let sortAsc = true;
    let isChatOpen = false;

    // Island Geolocation Presets for Quick Map Pan & Zoom
    const ISLAND_COORDINATES = {
      all: { center: [-2.5, 118.0], zoom: 5 },
      jawa: { center: [-7.25, 110.14], zoom: 7 },
      sumatera: { center: [-0.78, 101.34], zoom: 6 },
      kalimantan: { center: [-0.5, 114.5], zoom: 6 },
      sulawesi: { center: [-2.5, 121.0], zoom: 6 },
      nusa: { center: [-8.6, 120.5], zoom: 7 },
      maluku: { center: [-3.2, 128.5], zoom: 7 },
      papua: { center: [-4.2, 137.5], zoom: 6 }
    };\n\n    '''

html = html[:p1] + new_filters_block + html[p2:]

# 5. Replace getFilteredList, filter functions, updateFilterBarUI, resetAllFilters, zoomToIsland, etc.
p1 = html.find('function getFilteredList() {')
p2 = html.find('function openSystemModal(no)', p1)
assert p1 != -1 and p2 != -1, 'getFilteredList block not found'

new_filter_funcs = '''function getFilteredList() {
      if (!appData) return [];
      let list = [...appData.systems];

      // 1. Status Filter
      if (currentFilterStatus !== 'all') {
        list = list.filter(s => s.status_code === currentFilterStatus);
      }

      // 2. Kategori Sistem & Pola Operasi (Official Workbook Breakdown)
      if (currentFilterCategory !== 'all') {
        if (currentFilterCategory === 'interkoneksi') {
          list = list.filter(s => s.jenis_code === 'interkoneksi');
        } else if (currentFilterCategory === 'interkoneksi_kecil') {
          list = [];
        } else if (currentFilterCategory === 'isolated_24h') {
          list = list.filter(s => s.jenis_code === 'isolated' && s.jam_code === '24h');
        } else if (currentFilterCategory === 'isolated_12h') {
          list = list.filter(s => s.jenis_code === 'isolated' && s.jam_code === '12h');
        } else if (currentFilterCategory === 'isolated_6h') {
          list = list.filter(s => s.jenis_code === 'isolated' && s.jam_code === '6h');
        } else if (currentFilterCategory === 'uld_all') {
          list = list.filter(s => s.jenis_code === 'uld');
        } else if (currentFilterCategory === 'uld_24h') {
          list = list.filter(s => s.jenis_code === 'uld' && s.jam_code === '24h');
        } else if (currentFilterCategory === 'uld_12h') {
          list = list.filter(s => s.jenis_code === 'uld' && s.jam_code === '12h');
        } else if (currentFilterCategory === 'uld_6h') {
          list = list.filter(s => s.jenis_code === 'uld' && s.jam_code === '6h');
        }
      }

      // 3. Jam Operasi Filter Terpisah (Semua Jenis)
      if (currentFilterJam !== 'all') {
        list = list.filter(s => s.jam_code === currentFilterJam);
      }

      // 4. Island / Gugus Pulau Filter (Termasuk Papua 258 Sistem)
      if (currentFilterIsland && currentFilterIsland !== 'all') {
        list = list.filter(s => s.island === currentFilterIsland);
      }

      // 5. Unit / Wilayah Regional Filter
      if (currentFilterRegion) {
        list = list.filter(s => 
          (s.region && s.region.toLowerCase() === currentFilterRegion.toLowerCase()) || 
          (s.unit && s.unit.toLowerCase().includes(currentFilterRegion.toLowerCase()))
        );
      }

      // 6. Search Query
      if (currentSearchQuery) {
        const q = currentSearchQuery.toLowerCase();
        list = list.filter(s => 
          String(s.no).includes(q) ||
          s.name.toLowerCase().includes(q) ||
          s.unit.toLowerCase().includes(q) ||
          (s.region && s.region.toLowerCase().includes(q)) ||
          s.jenis.toLowerCase().includes(q) ||
          s.jam_operasi.toLowerCase().includes(q) ||
          (s.keterangan && s.keterangan.toLowerCase().includes(q)) ||
          s.status.toLowerCase().includes(q)
        );
      }

      list.sort((a, b) => {
        let va = a[sortColumn];
        let vb = b[sortColumn];
        if (typeof va === 'string') va = va.toLowerCase();
        if (typeof vb === 'string') vb = vb.toLowerCase();
        if (va < vb) return sortAsc ? -1 : 1;
        if (va > vb) return sortAsc ? 1 : -1;
        return 0;
      });

      return list;
    }

    function renderDetailTable() {
      const filtered = getFilteredList();
      const totalItems = filtered.length;
      const totalPages = Math.ceil(totalItems / pageSize) || 1;

      if (currentPage > totalPages) currentPage = totalPages;
      if (currentPage < 1) currentPage = 1;

      const startIndex = (currentPage - 1) * pageSize;
      const endIndex = Math.min(startIndex + pageSize, totalItems);
      const pageItems = filtered.slice(startIndex, endIndex);

      const countDisp = document.getElementById('tableRowCountDisplay');
      if (countDisp) countDisp.innerText = `Menampilkan ${totalItems} dari ${appData ? appData.systems.length : 0} sistem`;
      const pagInfo = document.getElementById('paginationInfo');
      if (pagInfo) pagInfo.innerText = totalItems > 0 ? `Menampilkan ${startIndex + 1} - ${endIndex} dari ${totalItems} sistem` : 'Tidak ada sistem yang cocok';
      
      const curP = document.getElementById('currentPageLabel');
      if (curP) curP.innerText = currentPage;
      const totP = document.getElementById('totalPageLabel');
      if (totP) totP.innerText = totalPages;

      if (document.getElementById('btnFirstPage')) document.getElementById('btnFirstPage').disabled = (currentPage === 1);
      if (document.getElementById('btnPrevPage')) document.getElementById('btnPrevPage').disabled = (currentPage === 1);
      if (document.getElementById('btnNextPage')) document.getElementById('btnNextPage').disabled = (currentPage === totalPages);
      if (document.getElementById('btnLastPage')) document.getElementById('btnLastPage').disabled = (currentPage === totalPages);

      ['no', 'name', 'unit', 'region', 'jenis', 'jam_operasi', 'dmp', 'bp', 'cad_mw', 'cad_pct', 'status'].forEach(col => {
        const el = document.getElementById('sort-' + col);
        if (el) el.innerText = (sortColumn === col) ? (sortAsc ? '▲' : '▼') : '↕';
      });

      const tbody = document.getElementById('detailTableBody');
      if (!tbody) return;

      tbody.innerHTML = pageItems.map(s => `
        <tr id="row-detail-${s.no}" onmouseenter="onTableRowHover(${s.no}, event)" onmouseleave="onTableRowLeave(${s.no})" onclick="openSystemModal(${s.no})" style="cursor:pointer;">
          <td>${s.no}</td>
          <td><strong>${s.name}</strong></td>
          <td style="font-size:11px; color:var(--text-muted);">${s.unit}</td>
          <td>${s.region}</td>
          <td><span class="tag-badge ${s.jenis_code === 'isolated' ? 'tag-isolated' : (s.jenis_code === 'interkoneksi' ? 'tag-interkoneksi' : 'tag-uld')}">${s.jenis}</span></td>
          <td><span class="tag-badge ${s.jam_code === '24h' ? 'tag-jam-24' : (s.jam_code === '12h' ? 'tag-jam-12' : 'tag-jam-6')}">${s.jam_operasi}</span></td>
          <td><strong style="color:#00A3E0;">${formatNum(s.dmp)}</strong></td>
          <td><strong style="color:#FDB913;">${formatNum(s.bp)}</strong></td>
          <td style="color:${s.cad_mw < 0 ? '#EF4444' : '#10B981'}; font-weight:700;">
            ${s.cad_mw >= 0 ? '+' : ''}${formatNum(s.cad_mw)}
          </td>
          <td>${s.cad_pct}%</td>
          <td><span class="status-badge ${s.status_code}">${s.status}</span></td>
          <td style="max-width:280px; white-space:normal; font-size:11px; color:var(--text-muted); line-height:1.3;">
            ${s.keterangan ? (s.keterangan.length > 70 ? s.keterangan.substring(0, 70) + '…' : s.keterangan) : '-'}
          </td>
          <td>
            <button class="btn" style="padding:3px 8px; font-size:10.5px;" onclick="event.stopPropagation(); openSystemModal(${s.no})">Detail</button>
          </td>
        </tr>
      `).join('');
    }

    function changePage(delta) {
      currentPage += delta;
      renderDetailTable();
    }

    function goToPage(p) {
      currentPage = p;
      renderDetailTable();
    }

    function goToLastPage() {
      const filtered = getFilteredList();
      currentPage = Math.ceil(filtered.length / pageSize) || 1;
      renderDetailTable();
    }

    function onSearchChange(val) {
      currentSearchQuery = val.trim();
      currentPage = 1;
      updateFilterBarUI();
      renderDetailTable();
      initOrUpdateMap();
    }

    function setFilterStatus(status) {
      currentFilterStatus = status;
      currentPage = 1;
      updateFilterBarUI();
      renderDetailTable();
      initOrUpdateMap();
    }

    function setFilterCategory(cat) {
      if (cat === 'interkoneksi_kecil') {
        showToast("Klasifikasi Interkoneksi Kecil belum tersedia secara resmi di workbook 910 sistem (tergabung dalam 49 Interkoneksi).", true);
        return;
      }
      currentFilterCategory = cat;
      currentPage = 1;

      const allCatKeys = [
        'All', 'Interkoneksi', 'InterkoneksiKecil',
        'Isolated24', 'Isolated12', 'Isolated6',
        'UldAll', 'Uld24', 'Uld12', 'Uld6'
      ];
      allCatKeys.forEach(k => {
        const btn = document.getElementById('btnCat' + k);
        if (btn) {
          const match = (
            (k === 'All' && cat === 'all') ||
            (k === 'Interkoneksi' && cat === 'interkoneksi') ||
            (k === 'Isolated24' && cat === 'isolated_24h') ||
            (k === 'Isolated12' && cat === 'isolated_12h') ||
            (k === 'Isolated6' && cat === 'isolated_6h') ||
            (k === 'UldAll' && cat === 'uld_all') ||
            (k === 'Uld24' && cat === 'uld_24h') ||
            (k === 'Uld12' && cat === 'uld_12h') ||
            (k === 'Uld6' && cat === 'uld_6h')
          );
          btn.classList.toggle('active', match);
        }
      });

      updateFilterBarUI();
      renderDetailTable();
      initOrUpdateMap();
    }

    function setFilterJenis(jenis) {
      setFilterCategory(jenis);
    }

    function setFilterJam(jam) {
      currentFilterJam = jam;
      currentPage = 1;
      ['All', '24', '12', '6'].forEach(k => {
        const btn = document.getElementById('btnPillJam' + k);
        const match = (k === 'All' && jam === 'all') || (k + 'h' === jam);
        if (btn) btn.classList.toggle('active', match);
      });
      updateFilterBarUI();
      renderDetailTable();
      initOrUpdateMap();
    }

    function filterByRegion(reg) {
      switchTab('detail');
      currentFilterRegion = (currentFilterRegion === reg) ? null : reg;
      currentPage = 1;
      updateFilterBarUI();
      renderDetailTable();
      initOrUpdateMap();
      if (currentFilterRegion) showToast(`Menyaring wilayah: ${currentFilterRegion}`);
    }

    function filterTableByKpi(metric) {
      switchTab('detail');
      if (metric === 'cad_mw') {
        setFilterStatus('defisit');
      } else {
        sortColumn = metric;
        sortAsc = false;
        renderDetailTable();
        showToast(`Tabel diurutkan berdasarkan ${metric.toUpperCase()}`);
      }
    }

    function sortTable(col) {
      if (sortColumn === col) sortAsc = !sortAsc;
      else { sortColumn = col; sortAsc = true; }
      renderDetailTable();
    }

    function filterDetailTable(status) {
      switchTab('detail');
      setFilterStatus(status);
    }

    function updateFilterBarUI() {
      const bar = document.getElementById('activeFiltersBar');
      const container = document.getElementById('filterChipsContainer');
      const chips = [];

      if (currentFilterCategory !== 'all') {
        const catMap = {
          'interkoneksi': 'Kategori: Interkoneksi (49)',
          'isolated_24h': 'Kategori: Isolated 24 Jam (412)',
          'isolated_12h': 'Kategori: Isolated 12 Jam (197)',
          'isolated_6h': 'Kategori: Isolated 6 Jam (36)',
          'uld_all': 'Kategori: ULD Semua (216)',
          'uld_24h': 'Kategori: ULD 24 Jam (76)',
          'uld_12h': 'Kategori: ULD 12 Jam (108)',
          'uld_6h': 'Kategori: ULD 6 Jam (32)'
        };
        chips.push({
          label: catMap[currentFilterCategory] || currentFilterCategory,
          remove: () => setFilterCategory('all')
        });
      }

      if (currentFilterJam !== 'all') {
        chips.push({
          label: `Jam Nyala: ${currentFilterJam.replace('h', ' Jam')}`,
          remove: () => setFilterJam('all')
        });
      }

      if (currentFilterIsland && currentFilterIsland !== 'all') {
        const islMap = {
          papua: 'Wilayah: Papua (258 Sistem)',
          sumatera: 'Wilayah: Sumatera (188 Sistem)',
          maluku: 'Wilayah: Maluku (168 Sistem)',
          kalimantan: 'Wilayah: Kalimantan (89 Sistem)',
          sulawesi: 'Wilayah: Sulawesi (89 Sistem)',
          nusa: 'Wilayah: Nusa Tenggara (74 Sistem)',
          jawa: 'Wilayah: Jawa-Bali (44 Sistem)'
        };
        chips.push({
          label: islMap[currentFilterIsland] || currentFilterIsland,
          remove: () => zoomToIsland('all')
        });
      }

      if (currentFilterStatus !== 'all') {
        chips.push({
          label: `Status: ${currentFilterStatus.toUpperCase()}`,
          remove: () => setFilterStatus('all')
        });
      }

      if (currentFilterRegion) {
        chips.push({
          label: `Regional/Unit: ${currentFilterRegion}`,
          remove: () => filterByRegion(null)
        });
      }

      if (currentSearchQuery) {
        chips.push({
          label: `Cari: "${currentSearchQuery}"`,
          remove: () => {
            document.getElementById('searchInput').value = '';
            onSearchChange('');
          }
        });
      }

      const filteredCount = getFilteredList().length;
      if (chips.length > 0) {
        bar.classList.add('active');
        container.innerHTML = `
          <span style="font-weight:700; color:var(--pln-cyan); margin-right:4px;">[${filteredCount} Sistem Terpilih]</span>
          ` + chips.map((c, i) => `
          <span class="filter-chip">
            ${c.label}
            <span class="filter-chip-remove" onclick="filterChipsRemove(${i})">&times;</span>
          </span>
        `).join('');
        window._activeFilterRemovers = chips.map(c => c.remove);
      } else {
        bar.classList.remove('active');
        container.innerHTML = '';
      }
    }

    function filterChipsRemove(idx) {
      if (window._activeFilterRemovers && window._activeFilterRemovers[idx]) {
        window._activeFilterRemovers[idx]();
      }
    }

    function resetAllFilters() {
      currentFilterStatus = 'all';
      currentFilterCategory = 'all';
      currentFilterJenis = 'all';
      currentFilterJam = 'all';
      currentFilterIsland = 'all';
      currentFilterRegion = null;
      currentSearchQuery = '';
      currentPage = 1;
      const sInp = document.getElementById('searchInput');
      if (sInp) sInp.value = '';
      setFilterStatus('all');
      setFilterCategory('all');
      setFilterJam('all');
      zoomToIsland('all');
      showToast("Semua filter telah direset");
    }

    // Map Island Navigation & Regional Zoom
    function zoomToIsland(islandKey) {
      currentFilterIsland = islandKey;
      currentPage = 1;

      document.querySelectorAll('.island-btn').forEach(b => b.classList.remove('active'));
      const activeBtn = document.getElementById('btnMap' + islandKey.charAt(0).toUpperCase() + islandKey.slice(1));
      if (activeBtn) activeBtn.classList.add('active');

      if (leafletMap) {
        const target = ISLAND_COORDINATES[islandKey] || ISLAND_COORDINATES.all;
        leafletMap.flyTo(target.center, target.zoom, { duration: 1.2 });
      }

      updateFilterBarUI();
      renderDetailTable();
      initOrUpdateMap();

      if (islandKey !== 'all') {
        const islandLabels = {
          papua: 'Papua (258 Sistem)',
          sumatera: 'Sumatera (188 Sistem)',
          maluku: 'Maluku (168 Sistem)',
          kalimantan: 'Kalimantan (89 Sistem)',
          sulawesi: 'Sulawesi (89 Sistem)',
          nusa: 'Nusa Tenggara (74 Sistem)',
          jawa: 'Jawa-Bali (44 Sistem)'
        };
        showToast(`Wilayah terpilih: ${islandLabels[islandKey] || islandKey.toUpperCase()}`);
      }
    }

    function zoomToDeficitSystems() {
      if (!leafletMap || !appData) return;
      setFilterStatus('defisit');
      const defs = appData.systems.filter(s => s.status_code === 'defisit' && s.geo && s.geo.lat !== null);
      if (defs.length > 0) {
        const bounds = L.latLngBounds(defs.map(s => [s.geo.lat, s.geo.lng]));
        leafletMap.fitBounds(bounds, { padding: [50, 50], maxZoom: 7, duration: 1.2 });
        showToast("Memfokuskan peta pada 57 sistem defisit");
      }
    }

    function focusSpecificSystem(sysName) {
      if (!appData) return;
      const s = appData.systems.find(item => item.name.toLowerCase() === sysName.toLowerCase());
      if (!s) return;

      switchTab('overview');
      if (leafletMap && s.geo && s.geo.lat !== null && systemMarkersMap[s.no]) {
        leafletMap.flyTo([s.geo.lat, s.geo.lng], 8, { duration: 1.2 });
        const marker = systemMarkersMap[s.no];
        if (marker) {
          setTimeout(() => marker.openPopup(), 1200);
        }
      } else {
        openSystemModal(s.no);
        showToast(`Sistem ${s.name}: Koordinat lapangan belum tersedia. Membuka detail informasi.`);
      }
    }\n\n    '''

html = html[:p1] + new_filter_funcs + html[p2:]

# 6. Replace initOrUpdateMap with robust coordinate grouping and fallback
p1 = html.find('function initOrUpdateMap() {')
p2 = html.find('function resetMapZoom() {', p1)
assert p1 != -1 and p2 != -1, 'initOrUpdateMap block not found'

new_init_map = '''function initOrUpdateMap() {
      if (!leafletMap) {
        leafletMap = L.map('leafletMap', {
          center: [-2.5, 118.0],
          zoom: 5,
          minZoom: 4,
          maxZoom: 12,
          attributionControl: false,
          zoomControl: true
        });

        // Set default base layer to Vector GIS
        setMapBaseLayer('vector');

        const isDark = document.documentElement.getAttribute('data-theme') !== 'light';

        fetch('/leaflet/indonesia-provinces.geojson')
          .then(res => res.json())
          .then(data => {
            rawGeojsonData = data;
            geojsonLayer = L.geoJSON(data, {
              style: () => getProvinceStyle(isDark, currentMapLayerMode),
              onEachFeature: (feature, layer) => {
                const provName = feature.properties ? (feature.properties.NAME_1 || feature.properties.name || feature.properties.Propinsi || 'Provinsi Indonesia') : 'Provinsi Indonesia';
                layer.on({
                  mouseover: (e) => {
                    const l = e.target;
                    l.setStyle({
                      fillColor: isDark ? '#193E6B' : '#94A3B8',
                      fillOpacity: 1.0,
                      weight: 1.8,
                      color: isDark ? '#38BDF8' : '#0284C7'
                    });
                    showGlobalTooltip(e.originalEvent, `
                      <div class="tooltip-header"><span class="tooltip-title">📍 ${provName.toUpperCase()}</span></div>
                      <div style="font-size:10.5px; color:var(--text-dim);">Batas Wilayah Provinsi Resmi (Data GIS QGIS)</div>
                    `);
                  },
                  mousemove: (e) => {
                    positionGlobalTooltip(e.originalEvent);
                  },
                  mouseout: (e) => {
                    if (geojsonLayer) geojsonLayer.resetStyle(e.target);
                    hideGlobalTooltip();
                  }
                });
              }
            }).addTo(leafletMap);

            if (markerClusterGroup) markerClusterGroup.bringToFront();
          })
          .catch(() => {});

        // Safe MarkerCluster initialization
        try {
          if (typeof L.markerClusterGroup === 'function') {
            markerClusterGroup = L.markerClusterGroup({
              maxClusterRadius: 45, // Prevents cross-island cluster merging
              spiderfyOnMaxZoom: true,
              showCoverageOnHover: false,
              zoomToBoundsOnClick: true
            }).addTo(leafletMap);
          } else {
            markerClusterGroup = L.layerGroup().addTo(leafletMap);
          }
        } catch (e) {
          markerClusterGroup = L.layerGroup().addTo(leafletMap);
        }
      }

      if (!appData) return;

      const systemsToRender = getFilteredList();

      if (markerClusterGroup) {
        markerClusterGroup.clearLayers();
      }
      systemMarkersMap = {};

      // Group systems by exact coordinate (lat_lng key)
      // Solves stacked markers at identical coordinates without fake scatter/jitter:
      // Single marker with count and list of systems, labeled "Koordinat bersama"
      const coordGroups = {};
      systemsToRender.forEach(s => {
        if (!s.geo || s.geo.lat === null || s.geo.lng === null) return;
        const lat = s.geo.lat;
        const lng = s.geo.lng;
        if (lat < -11.5 || lat > 6.5 || lng < 94.5 || lng > 141.5) return;

        const key = `${lat.toFixed(4)}_${lng.toFixed(4)}`;
        if (!coordGroups[key]) {
          coordGroups[key] = {
            lat: lat,
            lng: lng,
            is_shared: s.geo.is_shared,
            label: s.geo.label,
            systems: []
          };
        }
        coordGroups[key].systems.push(s);
      });

      Object.values(coordGroups).forEach(group => {
        const count = group.systems.length;
        const lat = group.lat;
        const lng = group.lng;

        if (count === 1) {
          // Individual standalone marker (e.g. Sabang, Merauke)
          const s = group.systems[0];
          const isDefisit = s.status_code === 'defisit';

          let icon;
          if (isDefisit) {
            icon = L.divIcon({
              className: 'radar-marker-deficit',
              html: `
                <div class="radar-core"></div>
                <div class="radar-ring"></div>
              `,
              iconSize: [22, 22],
              iconAnchor: [11, 11]
            });
          } else {
            let color = '#10B981';
            if (s.status_code === 'siaga') color = '#F59E0B';
            else if (s.status_code === 'unfilled') color = '#94A3B8';

            icon = L.divIcon({
              className: 'custom-map-marker',
              html: `
                <div style="width:12px; height:12px; background:${color}; border:1.8px solid #FFF; border-radius:50%; box-shadow:0 0 6px ${color};"></div>
              `,
              iconSize: [12, 12],
              iconAnchor: [6, 6]
            });
          }

          const marker = L.marker([lat, lng], { icon });
          systemMarkersMap[s.no] = marker;

          marker.on('mouseover', (e) => {
            showGlobalTooltip(e.originalEvent, generateSystemTooltip(s));
            const row = document.getElementById('row-detail-' + s.no);
            if (row) row.classList.add('highlighted');
          });
          marker.on('mousemove', (e) => positionGlobalTooltip(e.originalEvent));
          marker.on('mouseout', () => {
            hideGlobalTooltip();
            const row = document.getElementById('row-detail-' + s.no);
            if (row) row.classList.remove('highlighted');
          });
          marker.on('click', () => openSystemModal(s.no));

          const popupHtml = `
            <div style="font-family:sans-serif; min-width:240px; color:#0F172A; font-size:11.5px;">
              <div style="font-weight:800; font-size:13px; margin-bottom:4px; color:#002E62;">${s.no}. Sistem ${s.name}</div>
              <div style="margin-bottom:6px; display:flex; gap:4px;">
                <span class="status-badge ${s.status_code}">${s.status}</span>
                <span class="tag-badge ${s.jenis_code === 'isolated' ? 'tag-isolated' : 'tag-interkoneksi'}">${s.jenis}</span>
              </div>
              <div style="font-size:10px; color:#64748B; margin-bottom:4px;">${s.unit} • Pola: <strong>${s.jam_operasi}</strong></div>
              <div>• DMP: <strong>${formatNum(s.dmp)} MW</strong></div>
              <div>• Beban Puncak: <strong>${formatNum(s.bp)} MW</strong></div>
              <div style="margin-top:4px; font-weight:700; color:${s.cad_mw < 0 ? '#EF4444' : '#10B981'};">
                Cadangan: ${s.cad_mw >= 0 ? '+' : ''}${formatNum(s.cad_mw)} MW (${s.cad_pct}%)
              </div>
              <div style="margin-top:4px; font-size:10px; color:#10B981;">📍 ${s.geo.label || 'Koordinat Terverifikasi'}</div>
              <div style="margin-top:8px;">
                <button style="background:#002E62; color:#FFF; border:none; padding:4px 8px; border-radius:4px; font-size:10px; cursor:pointer;" onclick="openSystemModal(${s.no})">Buka Detail Lengkap</button>
              </div>
            </div>
          `;
          marker.bindPopup(popupHtml);
          if (markerClusterGroup) markerClusterGroup.addLayer(marker);

        } else {
          // Shared coordinate marker for multiple systems at identical point
          const hasDeficit = group.systems.some(s => s.status_code === 'defisit');
          const deficitCount = group.systems.filter(s => s.status_code === 'defisit').length;
          const siagaCount = group.systems.filter(s => s.status_code === 'siaga').length;
          const normalCount = group.systems.filter(s => s.status_code === 'normal').length;
          const unitName = group.systems[0].unit;

          const icon = L.divIcon({
            className: 'shared-coord-divicon',
            html: `
              <div class="shared-coord-badge ${hasDeficit ? 'has-deficit' : ''}">
                <span style="font-size:10px;">🏢</span>
                <span>${count}</span>
              </div>
            `,
            iconSize: [44, 24],
            iconAnchor: [22, 12]
          });

          const marker = L.marker([lat, lng], { icon });

          group.systems.forEach(s => {
            systemMarkersMap[s.no] = marker;
          });

          marker.on('mouseover', (e) => {
            showGlobalTooltip(e.originalEvent, `
              <div class="tooltip-header">
                <span class="tooltip-title">📍 KOORDINAT BERSAMA (${count} SISTEM)</span>
              </div>
              <div style="font-size:11px; margin-bottom:4px; color:#38BDF8;">${unitName}</div>
              <div style="font-size:10px; color:var(--text-dim); margin-bottom:6px;">Lokasi Kantor Wilayah / Belum terverifikasi titik lapangan</div>
              <div style="display:flex; gap:6px; font-size:10px;">
                ${deficitCount > 0 ? `<span class="status-badge defisit">${deficitCount} Defisit</span>` : ''}
                ${siagaCount > 0 ? `<span class="status-badge siaga">${siagaCount} Siaga</span>` : ''}
                ${normalCount > 0 ? `<span class="status-badge normal">${normalCount} Normal</span>` : ''}
              </div>
              <div style="font-size:9.5px; color:#FDB913; margin-top:4px;">💡 Klik marker untuk melihat daftar seluruh ${count} sistem</div>
            `);
          });
          marker.on('mousemove', (e) => positionGlobalTooltip(e.originalEvent));
          marker.on('mouseout', () => hideGlobalTooltip());

          const popupHtml = `
            <div style="font-family:sans-serif; min-width:300px; max-width:360px; color:#0F172A; font-size:11.5px;">
              <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:6px; border-bottom:1px solid #CBD5E1; padding-bottom:6px;">
                <div>
                  <div style="font-weight:800; font-size:12.5px; color:#002E62;">📍 Koordinat Bersama: ${unitName}</div>
                  <div style="font-size:10px; color:#64748B;">Lokasi Bersama Kantor Wilayah (${count} Sistem)</div>
                </div>
                <span class="status-badge" style="background:#002E62; color:#FFF; font-size:10px; padding:2px 6px;">${count} Sistem</span>
              </div>
              <div style="margin-bottom:8px; display:flex; gap:6px; font-size:10px;">
                ${deficitCount > 0 ? `<span class="status-badge defisit">${deficitCount} Defisit</span>` : ''}
                ${siagaCount > 0 ? `<span class="status-badge siaga">${siagaCount} Siaga</span>` : ''}
                ${normalCount > 0 ? `<span class="status-badge normal">${normalCount} Normal</span>` : ''}
              </div>
              <div style="font-size:10px; color:#475569; margin-bottom:6px;">Daftar Sistem Kelistrikan (Klik untuk Buka Detail):</div>
              <div style="max-height:220px; overflow-y:auto; display:flex; flex-direction:column; gap:4px; padding-right:4px;">
                ${group.systems.map(s => `
                  <div style="display:flex; justify-content:space-between; align-items:center; background:#F8FAFC; border:1px solid #E2E8F0; padding:5px 8px; border-radius:4px; cursor:pointer;" onclick="openSystemModal(${s.no})">
                    <div>
                      <div style="font-weight:700; color:#002E62; font-size:11px;">${s.no}. ${s.name}</div>
                      <div style="font-size:9.5px; color:#64748B;">${s.jenis} • ${s.jam_operasi}</div>
                    </div>
                    <div style="text-align:right;">
                      <span class="status-badge ${s.status_code}" style="font-size:9px; padding:1px 5px;">${s.status}</span>
                      <div style="font-size:9.5px; font-weight:700; color:${s.cad_mw < 0 ? '#EF4444' : '#10B981'}; margin-top:2px;">
                        ${s.cad_mw >= 0 ? '+' : ''}${formatNum(s.cad_mw)} MW
                      </div>
                    </div>
                  </div>
                `).join('')}
              </div>
            </div>
          `;
          marker.bindPopup(popupHtml);
          if (markerClusterGroup) markerClusterGroup.addLayer(marker);
        }
      });
    }\n\n    '''

html = html[:p1] + new_init_map + html[p2:]

# 7. Update openSystemModal to show coordinate information
modal_target = 'document.getElementById(\'modalSystemName\').innerText = `${s.no}. Sistem ${s.name} (${s.region})`;'
modal_replacement = '''document.getElementById('modalSystemName').innerText = `${s.no}. Sistem ${s.name} (${s.region})`;
      const coordInfoHtml = s.geo ? (
        s.geo.is_shared ? 
          `<div style="font-size:11px; color:#F59E0B; margin-bottom:12px; background:rgba(245, 158, 11, 0.1); border:1px solid rgba(245, 158, 11, 0.3); padding:6px 10px; border-radius:6px;">📍 <strong>Koordinat Bersama:</strong> ${s.unit} (${s.geo.lat}, ${s.geo.lng}) • Belum terverifikasi ke titik lapangan</div>` :
          `<div style="font-size:11px; color:#10B981; margin-bottom:12px; background:rgba(16, 185, 129, 0.1); border:1px solid rgba(16, 185, 129, 0.3); padding:6px 10px; border-radius:6px;">📍 <strong>Koordinat Lapangan Terverifikasi:</strong> ${s.geo.lat}, ${s.geo.lng} (${s.geo.label || 'Presisi'})</div>`
      ) : `<div style="font-size:11px; color:#94A3B8; margin-bottom:12px; background:rgba(148, 163, 184, 0.1); border:1px solid rgba(148, 163, 184, 0.3); padding:6px 10px; border-radius:6px;">📍 <strong>Koordinat belum tersedia</strong> (Data neraca daya tetap valid dihitung dalam KPI)</div>`;'''

assert modal_target in html, 'modalSystemName target not found'
html = html.replace(modal_target, modal_replacement, 1)

content_target = '<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px; background:var(--bg-card-alt); padding:10px 14px; border-radius:8px;">'
content_replacement = '${coordInfoHtml}\n        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px; background:var(--bg-card-alt); padding:10px 14px; border-radius:8px;">'

assert content_target in html, 'content_target not found'
html = html.replace(content_target, content_replacement, 1)

# 8. Update badge counts in loadData()
load_data_badges = '''// Badge Counts
      document.getElementById('badgeCountInter').innerText = kpi.jenis_counts.interkoneksi || 49;
      document.getElementById('badgeCountIso').innerText = kpi.jenis_counts.isolated || 645;
      document.getElementById('badgeCountUld').innerText = kpi.jenis_counts.uld || 216;

      document.getElementById('badgeCount24h').innerText = kpi.jam_operasi_counts['24h'] || 537;
      document.getElementById('badgeCount12h').innerText = kpi.jam_operasi_counts['12h'] || 305;
      document.getElementById('badgeCount6h').innerText = kpi.jam_operasi_counts['6h'] || 68;'''

new_load_data_badges = '''// Badge Counts
      if (document.getElementById('badgeCountInter')) document.getElementById('badgeCountInter').innerText = kpi.jenis_counts.interkoneksi || 49;
      if (document.getElementById('badgeCountIso')) document.getElementById('badgeCountIso').innerText = kpi.jenis_counts.isolated || 645;
      if (document.getElementById('badgeCountUld')) document.getElementById('badgeCountUld').innerText = kpi.jenis_counts.uld || 216;

      if (document.getElementById('badgeCount24h')) document.getElementById('badgeCount24h').innerText = kpi.jam_operasi_counts['24h'] || 537;
      if (document.getElementById('badgeCount12h')) document.getElementById('badgeCount12h').innerText = kpi.jam_operasi_counts['12h'] || 305;
      if (document.getElementById('badgeCount6h')) document.getElementById('badgeCount6h').innerText = kpi.jam_operasi_counts['6h'] || 68;

      if (kpi.category_counts) {
        if (document.getElementById('badgeCatAll')) document.getElementById('badgeCatAll').innerText = kpi.category_counts.semua || 910;
        if (document.getElementById('badgeCatInter')) document.getElementById('badgeCatInter').innerText = kpi.category_counts.interkoneksi || 49;
        if (document.getElementById('badgeCatIso24')) document.getElementById('badgeCatIso24').innerText = kpi.category_counts.isolated_24h || 412;
        if (document.getElementById('badgeCatIso12')) document.getElementById('badgeCatIso12').innerText = kpi.category_counts.isolated_12h || 197;
        if (document.getElementById('badgeCatIso6')) document.getElementById('badgeCatIso6').innerText = kpi.category_counts.isolated_6h || 36;
        if (document.getElementById('badgeCatUldAll')) document.getElementById('badgeCatUldAll').innerText = kpi.category_counts.uld_total || 216;
        if (document.getElementById('badgeCatUld24')) document.getElementById('badgeCatUld24').innerText = kpi.category_counts.uld_24h || 76;
        if (document.getElementById('badgeCatUld12')) document.getElementById('badgeCatUld12').innerText = kpi.category_counts.uld_12h || 108;
        if (document.getElementById('badgeCatUld6')) document.getElementById('badgeCatUld6').innerText = kpi.category_counts.uld_6h || 32;
      }'''

if load_data_badges in html:
    html = html.replace(load_data_badges, new_load_data_badges, 1)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)

print('SUCCESSFULLY PATCHED public/index.html!')
