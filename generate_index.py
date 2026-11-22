# Generator for public/index.html
import os

HTML_CONTENT = r'''<!DOCTYPE html>
<html lang="id" data-theme="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Dashboard Realtime Monitoring 910 Sistem Kelistrikan Nasional PLN</title>
  <!-- Leaflet GIS Real Map Assets -->
  <link rel="stylesheet" href="/leaflet/leaflet.css" />
  <script src="/leaflet/leaflet.js"></script>
  <style>
    :root {
      --pln-blue: #002E62;
      --pln-blue-dark: #001736;
      --pln-blue-light: #004D99;
      --pln-cyan: #00A3E0;
      --pln-cyan-glow: rgba(0, 163, 224, 0.45);
      --pln-yellow: #FDB913;
      --pln-red: #EF4444;
      --pln-amber: #F59E0B;
      --pln-green: #10B981;
      --pln-purple: #8B5CF6;

      /* Dark Enterprise Theme */
      --bg-body: #050B14;
      --bg-header: #081322;
      --bg-card: #0D1C2F;
      --bg-card-hover: #132742;
      --bg-card-alt: #081322;
      --border-color: #1A3150;
      --border-light: #24426A;
      --text-main: #F1F5F9;
      --text-muted: #94A3B8;
      --text-dim: #64748B;
      --chart-grid: #13243B;
      --tooltip-bg: rgba(10, 24, 44, 0.96);
      --tooltip-border: #00A3E0;
    }

    [data-theme="light"] {
      --bg-body: #F4F6F9;
      --bg-header: #FFFFFF;
      --bg-card: #FFFFFF;
      --bg-card-hover: #F8FAFC;
      --bg-card-alt: #F1F5F9;
      --border-color: #CBD5E1;
      --border-light: #E2E8F0;
      --text-main: #0F172A;
      --text-muted: #475569;
      --text-dim: #94A3B8;
      --chart-grid: #E2E8F0;
      --tooltip-bg: rgba(255, 255, 255, 0.98);
      --tooltip-border: #0284C7;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }

    body {
      background-color: var(--bg-body);
      color: var(--text-main);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      transition: background-color 0.25s ease, color 0.25s ease;
      overflow-x: hidden;
    }

    /* Top Command Header */
    header {
      background: var(--bg-header);
      border-bottom: 2px solid var(--pln-cyan);
      padding: 10px 24px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 16px;
      position: sticky;
      top: 0;
      z-index: 50;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }

    .brand-section {
      display: flex;
      align-items: center;
      gap: 14px;
    }

    .pln-logo-box {
      width: 44px;
      height: 44px;
      background: linear-gradient(135deg, var(--pln-yellow) 0%, #D97706 100%);
      border-radius: 8px;
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: 0 4px 12px rgba(253, 185, 19, 0.35);
      font-size: 24px;
      flex-shrink: 0;
    }

    .brand-text h1 {
      font-size: 15px;
      font-weight: 800;
      letter-spacing: 0.5px;
      color: var(--text-main);
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .brand-text h1 span.badge-total {
      background: rgba(0, 163, 224, 0.2);
      border: 1px solid var(--pln-cyan);
      color: var(--pln-cyan);
      font-size: 11px;
      padding: 1px 7px;
      border-radius: 12px;
      font-weight: 700;
    }

    .brand-text p {
      font-size: 11px;
      color: var(--text-muted);
      margin-top: 2px;
    }

    .header-controls {
      display: flex;
      align-items: center;
      gap: 10px;
      flex-wrap: wrap;
    }

    .status-pill {
      display: flex;
      align-items: center;
      gap: 7px;
      padding: 5px 12px;
      border-radius: 20px;
      background: rgba(16, 185, 129, 0.15);
      border: 1px solid rgba(16, 185, 129, 0.4);
      font-size: 11px;
      font-weight: 600;
      color: #10B981;
    }

    .status-dot {
      width: 7px;
      height: 7px;
      border-radius: 50%;
      background: #10B981;
      box-shadow: 0 0 8px #10B981;
      animation: pulse-dot 1.8s infinite;
    }

    @keyframes pulse-dot {
      0%, 100% { opacity: 1; transform: scale(1); }
      50% { opacity: 0.4; transform: scale(0.85); }
    }

    .open-access-pill {
      display: flex;
      align-items: center;
      gap: 8px;
      padding: 5px 12px;
      border-radius: 20px;
      background: rgba(0, 163, 224, 0.15);
      border: 1px solid var(--pln-cyan);
      font-size: 11px;
      font-weight: 600;
      color: var(--pln-cyan);
      cursor: pointer;
      transition: all 0.2s ease;
    }

    .open-access-pill:hover {
      background: rgba(0, 163, 224, 0.28);
      box-shadow: 0 0 12px var(--pln-cyan-glow);
    }

    .btn {
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      color: var(--text-main);
      padding: 6px 12px;
      border-radius: 6px;
      font-size: 11.5px;
      font-weight: 600;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s ease;
      user-select: none;
    }

    .btn:hover {
      background: var(--bg-card-hover);
      border-color: var(--pln-cyan);
    }

    .btn-primary {
      background: var(--pln-blue);
      border-color: var(--pln-cyan);
      color: #FFF;
      box-shadow: 0 2px 8px rgba(0, 163, 224, 0.25);
    }

    .btn-primary:hover {
      background: var(--pln-blue-light);
      border-color: var(--pln-yellow);
    }

    .btn.active {
      background: var(--pln-blue);
      border-color: var(--pln-cyan);
      color: #FFF;
      box-shadow: 0 0 10px var(--pln-cyan-glow);
    }

    .btn-icon {
      padding: 6px 9px;
      font-size: 13px;
    }

    /* Sub Navigation Bar */
    .sub-bar {
      background: var(--bg-card-alt);
      border-bottom: 1px solid var(--border-color);
      padding: 6px 24px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 12px;
    }

    .nav-tabs {
      display: flex;
      gap: 4px;
      overflow-x: auto;
    }

    .nav-tab {
      padding: 6px 14px;
      border-radius: 6px;
      font-size: 11.5px;
      font-weight: 600;
      color: var(--text-muted);
      cursor: pointer;
      transition: all 0.15s ease;
      white-space: nowrap;
      user-select: none;
    }

    .nav-tab:hover {
      color: var(--text-main);
      background: var(--bg-card);
    }

    .nav-tab.active {
      color: #FFF;
      background: var(--pln-blue);
      box-shadow: 0 2px 6px rgba(0, 46, 98, 0.4);
    }

    .meta-ticker {
      font-size: 11px;
      color: var(--text-dim);
      display: flex;
      gap: 16px;
      align-items: center;
    }

    .meta-ticker strong {
      color: var(--text-main);
    }

    /* Main Container */
    main {
      padding: 20px 24px;
      flex: 1;
      max-width: 1720px;
      margin: 0 auto;
      width: 100%;
    }

    .tab-content {
      display: none;
    }

    .tab-content.active {
      display: block;
      animation: fadeIn 0.25s ease;
    }

    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(4px); }
      to { opacity: 1; transform: translateY(0); }
    }

    /* System Classification Pills Bar */
    .filter-section-bar {
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: 10px;
      padding: 12px 18px;
      margin-bottom: 18px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 12px;
      box-shadow: 0 4px 14px rgba(0, 0, 0, 0.12);
    }

    .filter-group-wrap {
      display: flex;
      align-items: center;
      gap: 8px;
      flex-wrap: wrap;
    }

    .filter-group-label {
      font-size: 11px;
      font-weight: 700;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.5px;
      display: flex;
      align-items: center;
      gap: 4px;
    }

    .filter-btn-pill {
      padding: 5px 12px;
      font-size: 11.5px;
      font-weight: 600;
      border-radius: 20px;
      background: var(--bg-card-alt);
      border: 1px solid var(--border-color);
      color: var(--text-muted);
      cursor: pointer;
      transition: all 0.2s ease;
      user-select: none;
      display: inline-flex;
      align-items: center;
      gap: 6px;
    }

    .filter-btn-pill:hover {
      background: var(--bg-card-hover);
      color: var(--text-main);
      border-color: var(--pln-cyan);
    }

    .filter-btn-pill.active {
      background: var(--pln-blue);
      border-color: var(--pln-cyan);
      color: #FFF;
      box-shadow: 0 0 10px var(--pln-cyan-glow);
    }

    .badge-pill-count {
      font-size: 10px;
      padding: 1px 6px;
      border-radius: 10px;
      background: rgba(255, 255, 255, 0.15);
      font-weight: 700;
    }

    /* KPI Summary Grid */
    .kpi-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
      gap: 16px;
      margin-bottom: 20px;
    }

    .kpi-card {
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: 10px;
      padding: 16px;
      position: relative;
      overflow: hidden;
      transition: all 0.2s ease;
      box-shadow: 0 4px 14px rgba(0, 0, 0, 0.15);
      cursor: pointer;
    }

    .kpi-card:hover {
      transform: translateY(-3px);
      border-color: var(--pln-cyan);
      box-shadow: 0 8px 24px rgba(0, 163, 224, 0.25);
    }

    .kpi-card::before {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      height: 3px;
      background: var(--card-accent, var(--pln-cyan));
    }

    .kpi-header {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 8px;
    }

    .kpi-title {
      font-size: 11px;
      font-weight: 700;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }

    .kpi-icon {
      font-size: 18px;
      opacity: 0.85;
    }

    .kpi-value {
      font-size: 24px;
      font-weight: 800;
      color: var(--text-main);
      letter-spacing: -0.5px;
      line-height: 1.1;
      margin-bottom: 6px;
    }

    .kpi-sub {
      font-size: 11px;
      color: var(--text-dim);
      display: flex;
      align-items: center;
      gap: 6px;
    }

    /* Overview Layout (Map & Side Spotlight) */
    .overview-layout {
      display: grid;
      grid-template-columns: 2.2fr 1fr;
      gap: 20px;
      margin-bottom: 20px;
    }

    @media (max-width: 1200px) {
      .overview-layout {
        grid-template-columns: 1fr;
      }
    }

    .map-container-box {
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: 10px;
      padding: 16px;
      display: flex;
      flex-direction: column;
      box-shadow: 0 4px 14px rgba(0, 0, 0, 0.15);
    }

    .box-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 12px;
      padding-bottom: 10px;
      border-bottom: 1px solid var(--border-color);
      flex-wrap: wrap;
      gap: 10px;
    }

    .box-title {
      font-size: 14px;
      font-weight: 700;
      color: var(--text-main);
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .map-island-nav {
      display: flex;
      align-items: center;
      gap: 6px;
      flex-wrap: wrap;
      margin-bottom: 10px;
      padding: 6px 10px;
      background: var(--bg-card-alt);
      border-radius: 8px;
      border: 1px solid var(--border-color);
    }

    .island-btn {
      padding: 4px 10px;
      font-size: 11px;
      font-weight: 600;
      border-radius: 6px;
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      color: var(--text-muted);
      cursor: pointer;
      transition: all 0.2s ease;
      user-select: none;
    }

    .island-btn:hover {
      background: var(--bg-card-hover);
      color: var(--text-main);
      border-color: var(--pln-cyan);
    }

    .island-btn.active {
      background: var(--pln-blue);
      color: #FFF;
      border-color: var(--pln-cyan);
      box-shadow: 0 0 10px var(--pln-cyan-glow);
    }

    .leaflet-map-wrapper {
      height: 520px;
      width: 100%;
      border-radius: 8px;
      overflow: hidden;
      border: 1px solid var(--border-color);
      position: relative;
      background: #061224;
      transition: background 0.25s ease;
    }

    [data-theme="light"] .leaflet-map-wrapper {
      background: #E0F2FE;
    }

    /* Zero Watermark */
    .leaflet-control-attribution {
      display: none !important;
    }

    /* Radar Marker for Deficit */
    .radar-marker-deficit {
      position: relative;
      width: 22px;
      height: 22px;
      cursor: pointer;
    }

    .radar-core {
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      width: 12px;
      height: 12px;
      background: #EF4444;
      border: 2px solid #FFFFFF;
      border-radius: 50%;
      box-shadow: 0 0 10px #EF4444;
      z-index: 2;
    }

    .radar-ring {
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      width: 24px;
      height: 24px;
      border: 2px solid #EF4444;
      border-radius: 50%;
      animation: radar-ping 1.8s infinite cubic-bezier(0, 0, 0.2, 1);
    }

    @keyframes radar-ping {
      0% { width: 12px; height: 12px; opacity: 1; }
      100% { width: 38px; height: 38px; opacity: 0; }
    }

    .radar-marker-pulse-active {
      filter: drop-shadow(0 0 14px #00A3E0) brightness(1.3);
      transform: scale(1.4);
      transition: transform 0.2s ease;
      z-index: 9999 !important;
    }

    /* Right Side Analytics */
    .side-analytics-box {
      display: flex;
      flex-direction: column;
      gap: 16px;
    }

    .status-distribution-card {
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: 10px;
      padding: 16px;
      box-shadow: 0 4px 14px rgba(0, 0, 0, 0.15);
    }

    .status-count-row {
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
    }

    .status-count-row:hover {
      border-color: var(--pln-cyan);
      transform: translateX(4px);
    }

    .status-badge {
      display: inline-flex;
      align-items: center;
      gap: 5px;
      padding: 2px 7px;
      border-radius: 4px;
      font-size: 10px;
      font-weight: 700;
      text-transform: uppercase;
    }

    .status-badge.defisit {
      background: rgba(239, 68, 68, 0.15);
      color: #EF4444;
      border: 1px solid rgba(239, 68, 68, 0.4);
    }

    .status-badge.siaga {
      background: rgba(245, 158, 11, 0.15);
      color: #F59E0B;
      border: 1px solid rgba(245, 158, 11, 0.4);
    }

    .status-badge.normal {
      background: rgba(16, 185, 129, 0.15);
      color: #10B981;
      border: 1px solid rgba(16, 185, 129, 0.4);
    }

    .status-badge.unfilled {
      background: rgba(148, 163, 184, 0.15);
      color: #94A3B8;
      border: 1px solid rgba(148, 163, 184, 0.4);
    }

    .tag-badge {
      font-size: 10px;
      font-weight: 600;
      padding: 2px 6px;
      border-radius: 4px;
      display: inline-flex;
      align-items: center;
      gap: 3px;
    }

    .tag-isolated {
      background: rgba(139, 92, 246, 0.15);
      color: #A78BFA;
      border: 1px solid rgba(139, 92, 246, 0.4);
    }

    .tag-interkoneksi {
      background: rgba(0, 163, 224, 0.15);
      color: #38BDF8;
      border: 1px solid rgba(0, 163, 224, 0.4);
    }

    .tag-uld {
      background: rgba(245, 158, 11, 0.15);
      color: #FBBF24;
      border: 1px solid rgba(245, 158, 11, 0.4);
    }

    .tag-jam-24 {
      background: rgba(16, 185, 129, 0.15);
      color: #34D399;
      border: 1px solid rgba(16, 185, 129, 0.4);
    }

    .tag-jam-12 {
      background: rgba(249, 115, 22, 0.15);
      color: #FB923C;
      border: 1px solid rgba(249, 115, 22, 0.4);
    }

    .tag-jam-6 {
      background: rgba(239, 68, 68, 0.15);
      color: #F87171;
      border: 1px solid rgba(239, 68, 68, 0.4);
    }

    /* Scrollable Deficit Spotlight */
    .deficit-scroll-box {
      max-height: 260px;
      overflow-y: auto;
      display: flex;
      flex-direction: column;
      gap: 6px;
      padding-right: 4px;
    }

    .deficit-scroll-box::-webkit-scrollbar {
      width: 5px;
    }

    .deficit-scroll-box::-webkit-scrollbar-thumb {
      background: var(--border-color);
      border-radius: 3px;
    }

    /* Regional Cards Grid */
    .regional-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 16px;
      margin-bottom: 20px;
    }

    .regional-card {
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: 10px;
      padding: 16px;
      box-shadow: 0 4px 14px rgba(0, 0, 0, 0.15);
      transition: all 0.2s ease;
      cursor: pointer;
    }

    .regional-card:hover {
      border-color: var(--pln-cyan);
      transform: translateY(-3px);
      box-shadow: 0 8px 24px rgba(0, 163, 224, 0.25);
    }

    .regional-header {
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
    }

    .metric-row {
      display: flex;
      justify-content: space-between;
      font-size: 11.5px;
      margin-bottom: 6px;
      color: var(--text-muted);
    }

    .metric-row strong {
      color: var(--text-main);
    }

    /* Tables & Pagination */
    .table-container {
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: 10px;
      overflow: hidden;
      box-shadow: 0 4px 14px rgba(0, 0, 0, 0.15);
    }

    .table-toolbar {
      padding: 14px 18px;
      background: var(--bg-card-alt);
      border-bottom: 1px solid var(--border-color);
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 12px;
    }

    .search-box {
      position: relative;
      min-width: 280px;
    }

    .search-input {
      width: 100%;
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      padding: 7px 12px 7px 32px;
      border-radius: 6px;
      font-size: 11.5px;
      color: var(--text-main);
      outline: none;
    }

    .search-input:focus {
      border-color: var(--pln-cyan);
      box-shadow: 0 0 0 2px rgba(0, 163, 224, 0.2);
    }

    .search-icon {
      position: absolute;
      left: 10px;
      top: 50%;
      transform: translateY(-50%);
      font-size: 12px;
      color: var(--text-dim);
    }

    .data-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 11.5px;
      text-align: left;
    }

    .data-table th {
      background: var(--bg-card-alt);
      padding: 10px 14px;
      font-weight: 700;
      color: var(--text-muted);
      border-bottom: 2px solid var(--border-color);
      white-space: nowrap;
      cursor: pointer;
      user-select: none;
    }

    .data-table th:hover {
      color: var(--pln-cyan);
    }

    .data-table td {
      padding: 9px 14px;
      border-bottom: 1px solid var(--border-color);
      color: var(--text-main);
      white-space: nowrap;
      transition: background 0.15s ease;
    }

    .data-table tr:hover td {
      background: var(--bg-card-hover);
    }

    .data-table tr.highlighted td {
      background: rgba(0, 163, 224, 0.2) !important;
      border-color: var(--pln-cyan) !important;
    }

    /* Pagination Footer */
    .table-pagination-footer {
      padding: 10px 18px;
      background: var(--bg-card-alt);
      border-top: 1px solid var(--border-color);
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 12px;
      font-size: 11.5px;
    }

    .pagination-controls {
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .page-btn {
      padding: 4px 10px;
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      color: var(--text-main);
      border-radius: 5px;
      cursor: pointer;
      font-size: 11px;
      font-weight: 600;
      transition: all 0.15s ease;
    }

    .page-btn:hover:not(:disabled) {
      border-color: var(--pln-cyan);
      background: var(--bg-card-hover);
    }

    .page-btn:disabled {
      opacity: 0.4;
      cursor: not-allowed;
    }

    /* Active Filters Chips Bar */
    .active-filters-bar {
      display: none;
      align-items: center;
      gap: 8px;
      flex-wrap: wrap;
      padding: 10px 14px;
      background: var(--bg-card-alt);
      border: 1px solid var(--pln-cyan);
      border-radius: 8px;
      margin-bottom: 16px;
    }

    .active-filters-bar.active {
      display: flex;
    }

    .filter-chip {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 4px 10px;
      background: rgba(0, 163, 224, 0.15);
      border: 1px solid var(--pln-cyan);
      border-radius: 20px;
      font-size: 11px;
      font-weight: 600;
      color: var(--pln-cyan);
    }

    .filter-chip-remove {
      cursor: pointer;
      font-weight: 800;
      color: #FFF;
      background: rgba(239, 68, 68, 0.85);
      border-radius: 50%;
      width: 15px;
      height: 15px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 10px;
      line-height: 1;
    }

    /* Universal Glassmorphic Dynamic Tooltip */
    #dynamicTooltip {
      position: fixed;
      pointer-events: none;
      background: var(--tooltip-bg);
      border: 1px solid var(--tooltip-border);
      color: var(--text-main);
      padding: 12px 16px;
      border-radius: 10px;
      font-size: 11.5px;
      box-shadow: 0 16px 36px rgba(0, 0, 0, 0.65), 0 0 24px rgba(0, 163, 224, 0.3);
      z-index: 99999;
      display: none;
      opacity: 0;
      transition: opacity 0.15s ease, transform 0.1s ease;
      max-width: 360px;
      line-height: 1.5;
      backdrop-filter: blur(14px);
      -webkit-backdrop-filter: blur(14px);
      transform: scale(0.96);
    }

    #dynamicTooltip.show {
      display: block;
      opacity: 1;
      transform: scale(1);
    }

    .tooltip-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 10px;
      margin-bottom: 8px;
      padding-bottom: 6px;
      border-bottom: 1px solid var(--border-color);
    }

    .tooltip-title {
      font-weight: 800;
      font-size: 13px;
      color: var(--text-main);
    }

    .tooltip-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 6px 12px;
      margin-bottom: 8px;
      font-size: 11px;
    }

    .tooltip-hint {
      margin-top: 6px;
      padding-top: 6px;
      border-top: 1px dashed var(--border-color);
      font-size: 10px;
      color: var(--pln-cyan);
      display: flex;
      align-items: center;
      gap: 4px;
    }

    /* Modals */
    .modal-overlay {
      position: fixed;
      inset: 0;
      background: rgba(0, 0, 0, 0.75);
      backdrop-filter: blur(4px);
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 1000;
      opacity: 0;
      pointer-events: none;
      transition: opacity 0.2s ease;
      padding: 20px;
    }

    .modal-overlay.active {
      opacity: 1;
      pointer-events: auto;
    }

    .modal-window {
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: 12px;
      width: 660px;
      max-width: 100%;
      max-height: 85vh;
      overflow-y: auto;
      box-shadow: 0 20px 50px rgba(0, 0, 0, 0.6);
      transform: translateY(20px);
      transition: transform 0.2s ease;
    }

    .modal-overlay.active .modal-window {
      transform: translateY(0);
    }

    .modal-header {
      padding: 14px 20px;
      border-bottom: 1px solid var(--border-color);
      display: flex;
      align-items: center;
      justify-content: space-between;
      background: var(--bg-card-alt);
    }

    .modal-title {
      font-size: 14px;
      font-weight: 700;
      color: var(--text-main);
    }

    .modal-close {
      background: none;
      border: none;
      color: var(--text-muted);
      font-size: 20px;
      cursor: pointer;
    }

    .modal-body {
      padding: 20px;
      font-size: 12px;
      line-height: 1.6;
      color: var(--text-muted);
    }

    /* Floating Chatbot Widget */
    .chatbot-fab {
      position: fixed;
      bottom: 24px;
      right: 24px;
      z-index: 1000;
      background: linear-gradient(135deg, #002E62 0%, #00A3E0 100%);
      color: #FFFFFF;
      border: 2px solid rgba(255, 255, 255, 0.25);
      border-radius: 50px;
      padding: 12px 20px;
      display: flex;
      align-items: center;
      gap: 10px;
      cursor: pointer;
      box-shadow: 0 8px 25px rgba(0, 163, 224, 0.45);
      font-weight: 700;
      font-size: 13px;
      transition: all 0.25s ease;
      user-select: none;
    }

    .chatbot-fab:hover {
      transform: translateY(-3px) scale(1.03);
      box-shadow: 0 12px 30px rgba(0, 163, 224, 0.6);
      border-color: var(--pln-yellow);
    }

    .chatbot-drawer {
      position: fixed;
      bottom: 84px;
      right: 24px;
      width: 440px;
      max-width: calc(100vw - 32px);
      height: 600px;
      max-height: calc(100vh - 110px);
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: 14px;
      box-shadow: 0 20px 50px rgba(0, 0, 0, 0.6);
      display: flex;
      flex-direction: column;
      z-index: 1001;
      opacity: 0;
      pointer-events: none;
      transform: translateY(20px) scale(0.96);
      transform-origin: bottom right;
      transition: all 0.25s ease;
      overflow: hidden;
    }

    .chatbot-drawer.open {
      opacity: 1;
      pointer-events: auto;
      transform: translateY(0) scale(1);
    }

    .chatbot-header {
      background: linear-gradient(135deg, var(--pln-blue-dark) 0%, var(--bg-header) 100%);
      border-bottom: 1px solid var(--border-color);
      padding: 12px 16px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
    }

    .chatbot-header-info {
      display: flex;
      align-items: center;
      gap: 10px;
    }

    .chatbot-avatar {
      width: 36px;
      height: 36px;
      border-radius: 50%;
      background: linear-gradient(135deg, var(--pln-cyan) 0%, var(--pln-blue) 100%);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 18px;
    }

    .chatbot-title {
      font-size: 13px;
      font-weight: 700;
      color: var(--text-main);
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .chatbot-status-pill {
      font-size: 9px;
      padding: 1px 6px;
      border-radius: 10px;
      background: rgba(16, 185, 129, 0.2);
      color: #10B981;
      font-weight: 600;
    }

    .chatbot-body {
      flex: 1;
      overflow-y: auto;
      padding: 16px;
      display: flex;
      flex-direction: column;
      gap: 12px;
      background: var(--bg-body);
    }

    .chat-bubble {
      max-width: 88%;
      padding: 10px 14px;
      border-radius: 10px;
      font-size: 11.5px;
      line-height: 1.5;
      word-break: break-word;
    }

    .chat-bubble.bot {
      align-self: flex-start;
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      color: var(--text-main);
      border-bottom-left-radius: 2px;
    }

    .chat-bubble.user {
      align-self: flex-end;
      background: var(--pln-blue);
      border: 1px solid var(--pln-cyan);
      color: #FFFFFF;
      border-bottom-right-radius: 2px;
    }

    .chat-meta {
      font-size: 9.5px;
      color: var(--text-dim);
      margin-top: 4px;
    }

    .chat-bubble.user .chat-meta {
      color: rgba(255, 255, 255, 0.65);
      text-align: right;
    }

    .chat-typing {
      display: none;
      align-items: center;
      gap: 4px;
      padding: 8px 12px;
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: 10px;
      align-self: flex-start;
    }

    .chat-typing span {
      width: 6px;
      height: 6px;
      background: var(--pln-cyan);
      border-radius: 50%;
      animation: blink 1.4s infinite both;
    }

    .chat-typing span:nth-child(2) { animation-delay: 0.2s; }
    .chat-typing span:nth-child(3) { animation-delay: 0.4s; }

    @keyframes blink {
      0%, 80%, 100% { opacity: 0.2; transform: scale(0.8); }
      40% { opacity: 1; transform: scale(1.1); }
    }

    .chatbot-suggestions {
      padding: 8px 12px;
      background: var(--bg-card-alt);
      border-top: 1px solid var(--border-color);
      display: flex;
      gap: 6px;
      overflow-x: auto;
    }

    .chat-chip {
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      color: var(--text-muted);
      padding: 4px 9px;
      border-radius: 12px;
      font-size: 10.5px;
      cursor: pointer;
      transition: all 0.15s ease;
      white-space: nowrap;
    }

    .chat-chip:hover {
      background: var(--pln-blue);
      border-color: var(--pln-cyan);
      color: #FFF;
    }

    .chatbot-input-row {
      display: flex;
      align-items: center;
      gap: 8px;
      padding: 10px 14px;
      background: var(--bg-card);
      border-top: 1px solid var(--border-color);
    }

    .chatbot-input {
      flex: 1;
      background: var(--bg-card-alt);
      border: 1px solid var(--border-color);
      border-radius: 8px;
      padding: 9px 12px;
      font-size: 12px;
      color: var(--text-main);
      outline: none;
    }

    .chatbot-input:focus {
      border-color: var(--pln-cyan);
    }

    .chatbot-send-btn {
      background: var(--pln-blue);
      color: #FFFFFF;
      border: 1px solid var(--pln-cyan);
      border-radius: 8px;
      padding: 9px 14px;
      cursor: pointer;
      font-size: 12px;
      font-weight: 700;
      display: flex;
      align-items: center;
      gap: 4px;
    }

    #toast {
      position: fixed;
      bottom: 24px;
      left: 24px;
      background: #10B981;
      color: #FFF;
      padding: 10px 18px;
      border-radius: 6px;
      font-size: 12px;
      font-weight: 600;
      box-shadow: 0 10px 25px rgba(0, 0, 0, 0.5);
      display: flex;
      align-items: center;
      gap: 8px;
      transform: translateY(100px);
      opacity: 0;
      transition: all 0.25s ease;
      z-index: 1500;
    }

    #toast.show {
      transform: translateY(0);
      opacity: 1;
    }
  </style>
</head>
<body>

  <!-- Universal Dynamic Tooltip Element -->
  <div id="dynamicTooltip"></div>

  <!-- Top Command Header -->
  <header>
    <div class="brand-section">
      <div class="pln-logo-box">⚡</div>
      <div class="brand-text">
        <h1>
          MONITORING REALTIME 910 SISTEM KELISTRIKAN NASIONAL PLN
          <span class="badge-total">910 Sistem Aktif</span>
        </h1>
        <p>Konsolidasi Lengkap: Sistem Interkoneksi (49), Isolated (645), dan ULD (216) • Jam Nyala: 24 Jam, 12 Jam, 6 Jam</p>
      </div>
    </div>

    <div class="header-controls">
      <div class="status-pill">
        <span class="status-dot"></span>
        <span id="syncStatusLabel">Data 910 Sistem Terverifikasi (WIB)</span>
      </div>

      <div class="open-access-pill" onclick="copyNetworkIp()" title="Klik untuk menyalin tautan akses Wi-Fi/LAN">
        <span>🌐 Akses LAN:</span>
        <strong id="networkIpDisplay">http://192.168.0.116:8080</strong>
        <span style="font-size:10px;">📋 Salin</span>
      </div>

      <div style="display:flex; align-items:center; gap:6px;">
        <select id="autoRefreshSelect" class="btn" style="padding:6px 10px;" onchange="changeAutoRefresh(this.value)">
          <option value="15">Auto: 15s</option>
          <option value="30" selected>Auto: 30s</option>
          <option value="60">Auto: 60s</option>
          <option value="0">Auto: Nonaktif</option>
        </select>
        <span id="countdownLabel" style="font-size:11px; color:var(--text-dim); min-width:60px;">Auto: 30d</span>
      </div>

      <button class="btn btn-primary" onclick="triggerManualRefresh()" title="Sinkronkan data sekarang">
        <span>🔄 Refresh</span>
      </button>

      <button class="btn" onclick="openSyncModal()" title="Lihat detail sumber SharePoint & unggah pembaruan">
        <span>📁 Sumber Data</span>
      </button>

      <button class="btn btn-icon" onclick="toggleTheme()" id="btnTheme" title="Ganti Tema (Dark/Light)">
        <span>🌙</span>
      </button>

      <button class="btn btn-icon" onclick="toggleFullscreen()" title="Layar Penuh">
        <span>⛶</span>
      </button>
    </div>
  </header>

  <!-- Sub Navigation Bar -->
  <div class="sub-bar">
    <div class="nav-tabs">
      <div class="nav-tab active" onclick="switchTab('overview')">📊 Executive Overview</div>
      <div class="nav-tab" onclick="switchTab('isolated')">🏝️ Sistem Isolated (645)</div>
      <div class="nav-tab" onclick="switchTab('pembangkit')">⚡ Pembangkit</div>
      <div class="nav-tab" onclick="switchTab('gardu_induk')">🏢 Gardu Induk</div>
      <div class="nav-tab" onclick="switchTab('transmisi')">🗼 Transmisi & Interkoneksi</div>
      <div class="nav-tab" onclick="switchTab('distribusi')">🔌 Distribusi & Beban</div>
      <div class="nav-tab" onclick="switchTab('detail')">📑 Matriks Data (910 Sistem)</div>
    </div>

    <div class="meta-ticker">
      <span>Sinkronisasi Terakhir: <strong id="lastUpdatedWib">—</strong></span>
      <span>Total Sistem: <strong id="totalSistemBadge">910 Sistem</strong></span>
    </div>
  </div>

  <!-- Main Content Areas -->
  <main>

    <!-- Active Cross-Filter Chips Bar -->
    <div id="activeFiltersBar" class="active-filters-bar">
      <strong style="font-size:11px; color:var(--text-dim);">FILTER AKTIF:</strong>
      <div id="filterChipsContainer" style="display:flex; gap:6px; flex-wrap:wrap;"></div>
      <button class="btn" style="padding:2px 8px; font-size:10px; margin-left:auto;" onclick="resetAllFilters()">Reset Semua Filter</button>
    </div>

    <!-- ========================================== -->
    <!-- TAB 1: EXECUTIVE OVERVIEW -->
    <!-- ========================================== -->
    <section id="tab-overview" class="tab-content active">

      <!-- Interactive Classification Bar (Jenis & Jam Nyala) -->
      <div class="filter-section-bar">
        <div class="filter-group-wrap">
          <span class="filter-group-label">⚡ JENIS SISTEM:</span>
          <div class="filter-btn-pill active" id="btnPillJenisAll" onclick="setFilterJenis('all')">
            <span>Semua</span>
            <span class="badge-pill-count" id="badgeCountAllJenis">910</span>
          </div>
          <div class="filter-btn-pill" id="btnPillJenisInterkoneksi" onclick="setFilterJenis('interkoneksi')">
            <span>⚡ Interkoneksi (Grid)</span>
            <span class="badge-pill-count" id="badgeCountInter">49</span>
          </div>
          <div class="filter-btn-pill" id="btnPillJenisIsolated" onclick="setFilterJenis('isolated')">
            <span>🏝️ Isolated (Mandiri)</span>
            <span class="badge-pill-count" id="badgeCountIso">645</span>
          </div>
          <div class="filter-btn-pill" id="btnPillJenisUld" onclick="setFilterJenis('uld')">
            <span>🏘️ ULD (Listrik Desa)</span>
            <span class="badge-pill-count" id="badgeCountUld">216</span>
          </div>
        </div>

        <div class="filter-group-wrap">
          <span class="filter-group-label">⏱️ JAM NYALA:</span>
          <div class="filter-btn-pill active" id="btnPillJamAll" onclick="setFilterJam('all')">
            <span>Semua</span>
            <span class="badge-pill-count">910</span>
          </div>
          <div class="filter-btn-pill" id="btnPillJam24" onclick="setFilterJam('24h')">
            <span>⏱️ 24 Jam</span>
            <span class="badge-pill-count" id="badgeCount24h">537</span>
          </div>
          <div class="filter-btn-pill" id="btnPillJam12" onclick="setFilterJam('12h')">
            <span>🌙 12 Jam</span>
            <span class="badge-pill-count" id="badgeCount12h">305</span>
          </div>
          <div class="filter-btn-pill" id="btnPillJam6" onclick="setFilterJam('6h')">
            <span>⚡ 6 Jam</span>
            <span class="badge-pill-count" id="badgeCount6h">68</span>
          </div>
        </div>
      </div>
      
      <!-- Interactive KPI Summary Cards -->
      <div class="kpi-grid">
        <div class="kpi-card" id="cardKpiTotal" style="--card-accent: #00A3E0;" onclick="switchTab('detail')">
          <div class="kpi-header">
            <span class="kpi-title">Total Sistem Nasional</span>
            <span class="kpi-icon">🇮🇩</span>
          </div>
          <div class="kpi-value" id="kpiTotalSistem">910 <span style="font-size:14px; font-weight:600;">Sistem</span></div>
          <div class="kpi-sub">49 Interkoneksi • 645 Isolated • 216 ULD</div>
        </div>

        <div class="kpi-card" id="cardKpiDmp" style="--card-accent: #38BDF8;" onclick="filterTableByKpi('dmp')">
          <div class="kpi-header">
            <span class="kpi-title">Daya Mampu Pasok (DMP)</span>
            <span class="kpi-icon">🔋</span>
          </div>
          <div class="kpi-value" id="kpiDmp">56.763,5 <span style="font-size:14px; font-weight:600;">MW</span></div>
          <div class="kpi-sub">Total kapasitas pasok siap operasi</div>
        </div>

        <div class="kpi-card" id="cardKpiBp" style="--card-accent: #FDB913;" onclick="filterTableByKpi('bp')">
          <div class="kpi-header">
            <span class="kpi-title">Beban Puncak (BP)</span>
            <span class="kpi-icon">📈</span>
          </div>
          <div class="kpi-value" id="kpiBp">55.246,0 <span style="font-size:14px; font-weight:600;">MW</span></div>
          <div class="kpi-sub">Serapan beban konsumen nasional</div>
        </div>

        <div class="kpi-card" id="cardKpiCad" style="--card-accent: #10B981;" onclick="filterTableByKpi('cad_mw')">
          <div class="kpi-header">
            <span class="kpi-title">Cadangan Daya Nasional</span>
            <span class="kpi-icon">🛡️</span>
          </div>
          <div class="kpi-value" id="kpiCad">+1.517,7 <span style="font-size:14px; font-weight:600;">MW</span></div>
          <div class="kpi-sub" id="kpiCadSub">Reserve Margin: <strong>2,75%</strong> • <em>Klik saring</em></div>
        </div>

        <div class="kpi-card" id="cardKpiDefisit" style="--card-accent: #EF4444;" onclick="filterDetailTable('defisit')">
          <div class="kpi-header">
            <span class="kpi-title">Sistem Defisit Terpantau</span>
            <span class="kpi-icon">🚨</span>
          </div>
          <div class="kpi-value" style="color:#EF4444;" id="kpiDefisitVal">57 <span style="font-size:14px; font-weight:600;">Sistem</span></div>
          <div class="kpi-sub">Cadangan Daya &lt; 0 MW • <em>Klik fokus</em></div>
        </div>
      </div>

      <!-- Layout: Real Leaflet GIS Map + Right Side Analytics -->
      <div class="overview-layout">
        
        <!-- Peta Indonesia GIS Real with Island Navigator -->
        <div class="map-container-box">
          <div class="box-header">
            <div class="box-title">
              <span>🗺️ Sebaran Geografis 910 Sistem Kelistrikan Indonesia</span>
              <span class="status-badge defisit" id="mapDeficitBadge">57 Defisit</span>
            </div>
            <div style="display:flex; align-items:center; gap:6px; flex-wrap:wrap;">
              <span style="font-size:10px; color:var(--text-dim);">LAYER:</span>
              <button class="btn active" id="btnLayerVector" style="padding:4px 8px; font-size:10px;" onclick="setMapBaseLayer('vector')" title="Vektor GIS Asli Indonesia (100% Bersih & Offline)">🗺️ Vektor GIS</button>
              <button class="btn" id="btnLayerEsri" style="padding:4px 8px; font-size:10px;" onclick="setMapBaseLayer('esri')" title="ESRI Dark/Light Gray Canvas">🌑 ESRI Canvas</button>
              <button class="btn" id="btnLayerOsm" style="padding:4px 8px; font-size:10px;" onclick="setMapBaseLayer('osm')" title="OpenStreetMap Standar">🌐 OpenStreetMap</button>
              <button class="btn" style="padding:4px 8px; font-size:10px;" onclick="resetMapZoom()">🔍 Reset Zoom</button>
            </div>
          </div>

          <!-- Interactive Island Navigator Toolbar -->
          <div class="map-island-nav">
            <span style="font-size:10px; color:var(--text-dim); margin-right:4px;">NAVIGASI:</span>
            <div class="island-btn active" id="btnMapAll" onclick="zoomToIsland('all')">🇮🇩 Semua</div>
            <div class="island-btn" id="btnMapJawa" onclick="zoomToIsland('jawa')">⚡ Jawa-Bali</div>
            <div class="island-btn" id="btnMapSumatera" onclick="zoomToIsland('sumatera')">🌴 Sumatera</div>
            <div class="island-btn" id="btnMapKalimantan" onclick="zoomToIsland('kalimantan')">🌲 Kalimantan</div>
            <div class="island-btn" id="btnMapSulawesi" onclick="zoomToIsland('sulawesi')">🌊 Sulawesi</div>
            <div class="island-btn" id="btnMapNusa" onclick="zoomToIsland('nusa')">🏝️ Nusa Tenggara</div>
            <div class="island-btn" id="btnMapMalukuPapua" onclick="zoomToIsland('maluku_papua')">⛰️ Maluku & Papua</div>
            <div class="island-btn" style="border-color:#EF4444; color:#EF4444; margin-left:auto;" onclick="zoomToDeficitSystems()">🚨 Fokus 57 Defisit</div>
          </div>

          <div id="leafletMap" class="leaflet-map-wrapper"></div>
          
          <div style="display:flex; justify-content:space-between; align-items:center; margin-top:10px; font-size:11px; color:var(--text-dim);">
            <div style="display:flex; gap:14px; flex-wrap:wrap;">
              <span>🔴 <strong>Defisit</strong> (Radar)</span>
              <span>🟡 <strong>Siaga</strong> (Ketat)</span>
              <span>🟢 <strong>Normal</strong> (Aman)</span>
              <span>⚪ <strong>Belum Terisi</strong></span>
            </div>
            <span>💡 Arahkan kursor ke marker titik untuk melihat jenis & jam nyala</span>
          </div>
        </div>

        <!-- Right Side: Status Distribution & Executive Deficit Notice -->
        <div class="side-analytics-box">
          
          <!-- Status Distribution -->
          <div class="status-distribution-card">
            <div class="box-title" style="margin-bottom:12px;">
              <span>📊 Distribusi Status Neraca Daya (910 Sistem)</span>
            </div>

            <div class="status-count-row" id="rowStatusDefisit" onclick="filterDetailTable('defisit')">
              <div style="display:flex; align-items:center; gap:8px;">
                <span class="status-badge defisit">DEFISIT</span>
                <span style="font-size:11px; color:var(--text-muted);">Cadangan Negatif</span>
              </div>
              <strong style="color:#EF4444; font-size:16px;" id="countDefisit">57 Sistem</strong>
            </div>

            <div class="status-count-row" id="rowStatusSiaga" onclick="filterDetailTable('siaga')">
              <div style="display:flex; align-items:center; gap:8px;">
                <span class="status-badge siaga">SIAGA</span>
                <span style="font-size:11px; color:var(--text-muted);">Margin Ketat</span>
              </div>
              <strong style="color:#F59E0B; font-size:16px;" id="countSiaga">467 Sistem</strong>
            </div>

            <div class="status-count-row" id="rowStatusNormal" onclick="filterDetailTable('normal')">
              <div style="display:flex; align-items:center; gap:8px;">
                <span class="status-badge normal">NORMAL</span>
                <span style="font-size:11px; color:var(--text-muted);">Surplus Aman</span>
              </div>
              <strong style="color:#10B981; font-size:16px;" id="countNormal">224 Sistem</strong>
            </div>

            <div class="status-count-row" id="rowStatusUnfilled" onclick="filterDetailTable('unfilled')">
              <div style="display:flex; align-items:center; gap:8px;">
                <span class="status-badge unfilled">BELUM TERISI</span>
                <span style="font-size:11px; color:var(--text-muted);">Perlu Validasi Unit</span>
              </div>
              <strong style="color:#94A3B8; font-size:16px;" id="countUnfilled">162 Sistem</strong>
            </div>
          </div>

          <!-- Executive Deficit Spotlight -->
          <div class="status-distribution-card" style="border-left: 3px solid #EF4444;">
            <div class="box-title" style="color:#EF4444; margin-bottom:10px;">
              <span>🚨 Sorotan 57 Sistem Defisit</span>
            </div>

            <div class="deficit-scroll-box" id="deficitSpotlightContainer">
              <!-- Populated by JS -->
            </div>

            <div style="margin-top:10px; padding-top:8px; border-top:1px solid var(--border-color); font-size:10.5px; color:var(--text-dim); display:flex; justify-content:space-between; align-items:center;">
              <span>💡 Klik sistem untuk fokus peta</span>
              <button class="btn" style="padding:2px 8px; font-size:10px;" onclick="filterDetailTable('defisit')">Lihat Semua di Tabel</button>
            </div>
          </div>

        </div>

      </div>

      <!-- Regional Overview Summary Cards -->
      <div style="margin-top: 10px;">
        <div class="box-title" style="margin-bottom:12px;">
          <span>🌐 Ringkasan Daya & Cadangan Berdasarkan Wilayah Regional</span>
        </div>
        <div class="regional-grid" id="regionalCardsContainer">
          <!-- Populated by JS -->
        </div>
      </div>

    </section>

    <!-- ========================================== -->
    <!-- TAB 2: SISTEM ISOLATED (645 SISTEM) -->
    <!-- ========================================== -->
    <section id="tab-isolated" class="tab-content">
      <div class="box-header">
        <div class="box-title">
          <span>🏝️ Pemantauan Khusus 645 Sistem Isolated (Mandiri / Kepulauan)</span>
        </div>
        <div style="font-size:11px; color:var(--text-muted);">
          Sistem mandiri di pulau-pulau dan wilayah 3T tanpa interkoneksi grid regional
        </div>
      </div>

      <div class="kpi-grid">
        <div class="kpi-card" style="--card-accent: #8B5CF6;" onclick="filterIsolatedByJam('all')">
          <div class="kpi-title">Total Sistem Isolated</div>
          <div class="kpi-value" style="color:#A78BFA;">645 <span style="font-size:13px;">Sistem</span></div>
          <div class="kpi-sub">70,9% dari total sistem kelistrikan nasional</div>
        </div>
        <div class="kpi-card" style="--card-accent: #10B981;" onclick="filterIsolatedByJam('24h')">
          <div class="kpi-title">Isolated 24 Jam Penuh</div>
          <div class="kpi-value" style="color:#10B981;">412 <span style="font-size:13px;">Sistem</span></div>
          <div class="kpi-sub">Beroperasi siang dan malam (Leok, Karimun, Natuna)</div>
        </div>
        <div class="kpi-card" style="--card-accent: #F97316;" onclick="filterIsolatedByJam('12h')">
          <div class="kpi-title">Isolated 12 Jam (Malam)</div>
          <div class="kpi-value" style="color:#F97316;">197 <span style="font-size:13px;">Sistem</span></div>
          <div class="kpi-sub">Nyala pk 18:00 – 06:00 (Tanakeke, pulau-pulau 3T)</div>
        </div>
        <div class="kpi-card" style="--card-accent: #EF4444;" onclick="filterIsolatedByJam('6h')">
          <div class="kpi-title">Isolated 6 Jam (Puncak)</div>
          <div class="kpi-value" style="color:#EF4444;">36 <span style="font-size:13px;">Sistem</span></div>
          <div class="kpi-sub">Nyala pk 18:00 – 24:00 (Desa terluar terpencil)</div>
        </div>
      </div>

      <div class="table-container" style="margin-top:16px;">
        <div class="table-toolbar">
          <strong style="font-size:12.5px;">Daftar 645 Sistem Isolated Nasional Beserta Jam Operasi & Neraca Daya</strong>
          <button class="btn btn-primary" onclick="switchTab('detail'); setFilterJenis('isolated');">Buka di Matriks Lengkap</button>
        </div>
        <div style="overflow-x:auto;">
          <table class="data-table">
            <thead>
              <tr>
                <th>No</th>
                <th>Nama Sistem</th>
                <th>Unit / Wilayah</th>
                <th>Regional</th>
                <th>Jam Operasi</th>
                <th>DMP (MW)</th>
                <th>Beban Puncak (MW)</th>
                <th>Cadangan (MW)</th>
                <th>Status</th>
                <th>Keterangan Validasi</th>
                <th>Aksi</th>
              </tr>
            </thead>
            <tbody id="isolatedTableBody">
              <!-- Populated by JS -->
            </tbody>
          </table>
        </div>
      </div>
    </section>

    <!-- ========================================== -->
    <!-- TAB 3: PEMBANGKIT -->
    <!-- ========================================== -->
    <section id="tab-pembangkit" class="tab-content">
      <div class="box-header">
        <div class="box-title">
          <span>⚡ Analitik Sektor Pembangkit (Generation Assets)</span>
        </div>
        <div style="font-size:11px; color:var(--text-muted);">
          Total DMP Nasional: <strong>56.763,5 MW</strong> • Beban Puncak: <strong>55.246,0 MW</strong>
        </div>
      </div>

      <div class="kpi-grid">
        <div class="kpi-card" style="--card-accent: #00A3E0;">
          <div class="kpi-title">Pembangkit Interkoneksi</div>
          <div class="kpi-value">49 <span style="font-size:13px;">Grid</span></div>
          <div class="kpi-sub">Pemasok beban kontinental & tol listrik</div>
        </div>
        <div class="kpi-card" style="--card-accent: #A78BFA;">
          <div class="kpi-title">Pembangkit Isolated</div>
          <div class="kpi-value">645 <span style="font-size:13px;">Sentra</span></div>
          <div class="kpi-sub">Didominasi PLTD, PLTM, dan PLTS pulau</div>
        </div>
        <div class="kpi-card" style="--card-accent: #FDB913;">
          <div class="kpi-title">Unit Listrik Desa (ULD)</div>
          <div class="kpi-value">216 <span style="font-size:13px;">Lokasi</span></div>
          <div class="kpi-sub">Elektrifikasi pedesaan dan perbatasan</div>
        </div>
        <div class="kpi-card" style="--card-accent: #EF4444;">
          <div class="kpi-title">Sistem Mengalami Defisit</div>
          <div class="kpi-value" style="color:#EF4444;">57 <span style="font-size:13px;">Sistem</span></div>
          <div class="kpi-sub">Prioritas perbaikan mesin & logistik BBM</div>
        </div>
      </div>

      <div class="table-container" style="margin-top:16px;">
        <div class="table-toolbar">
          <strong style="font-size:12.5px;">Tabel Kapasitas Pembangkit (DMP, BP, CAD) Per Sistem</strong>
        </div>
        <div style="overflow-x:auto;">
          <table class="data-table">
            <thead>
              <tr>
                <th>No</th>
                <th>Sistem</th>
                <th>Unit / Wilayah</th>
                <th>Jenis</th>
                <th>Jam Nyala</th>
                <th>DMP (MW)</th>
                <th>Beban Puncak (MW)</th>
                <th>Cadangan (MW)</th>
                <th>Status</th>
                <th>Aksi</th>
              </tr>
            </thead>
            <tbody id="pembangkitTableBody">
              <!-- Populated by JS -->
            </tbody>
          </table>
        </div>
      </div>
    </section>

    <!-- ========================================== -->
    <!-- TAB 4: GARDU INDUK -->
    <!-- ========================================== -->
    <section id="tab-gardu_induk" class="tab-content">
      <div class="box-header">
        <div class="box-title">
          <span>🏢 Analitik Kesiapan Gardu Induk & Titik Injeksi Beban</span>
        </div>
        <div style="font-size:11px; color:var(--text-muted);">
          Pemantauan Kapasitas Pasok dan Titik Injeksi GI di Seluruh Sistem
        </div>
      </div>

      <div class="kpi-grid">
        <div class="kpi-card" style="--card-accent: #00A3E0;">
          <div class="kpi-title">Total Sistem Terlayani</div>
          <div class="kpi-value">910 <span style="font-size:13px;">Sistem</span></div>
          <div class="kpi-sub">Seluruh kepulauan Indonesia</div>
        </div>
        <div class="kpi-card" style="--card-accent: #10B981;">
          <div class="kpi-title">Kapasitas Injeksi Pasok</div>
          <div class="kpi-value">56.763,5 <span style="font-size:13px;">MW</span></div>
          <div class="kpi-sub">Total daya siap salur</div>
        </div>
        <div class="kpi-card" style="--card-accent: #FDB913;">
          <div class="kpi-title">Beban Puncak Tersalur</div>
          <div class="kpi-value">55.246,0 <span style="font-size:13px;">MW</span></div>
          <div class="kpi-sub">Total serapan daya beban</div>
        </div>
        <div class="kpi-card" style="--card-accent: #3B82F6;">
          <div class="kpi-title">Injeksi Terbesar (Jamali)</div>
          <div class="kpi-value" style="font-size:20px;">Jamali <span style="font-size:13px;">(~35.086 MW)</span></div>
          <div class="kpi-sub">Grid 500/150 kV Pulau Jawa-Bali</div>
        </div>
      </div>

      <div class="table-container" style="margin-top:16px;">
        <div class="table-toolbar">
          <strong style="font-size:12.5px;">Matriks Penyaluran Gardu Induk Tiap Sistem</strong>
        </div>
        <div style="overflow-x:auto;">
          <table class="data-table">
            <thead>
              <tr>
                <th>No</th>
                <th>Sistem Kelistrikan</th>
                <th>Wilayah Operasi</th>
                <th>Jenis</th>
                <th>Jam Nyala</th>
                <th>DMP (MW)</th>
                <th>Beban Puncak (MW)</th>
                <th>Cadangan (MW)</th>
                <th>Status</th>
                <th>Aksi</th>
              </tr>
            </thead>
            <tbody id="garduIndukTableBody">
              <!-- Populated by JS -->
            </tbody>
          </table>
        </div>
      </div>
    </section>

    <!-- ========================================== -->
    <!-- TAB 5: TRANSMISI & INTERKONEKSI -->
    <!-- ========================================== -->
    <section id="tab-transmisi" class="tab-content">
      <div class="box-header">
        <div class="box-title">
          <span>🗼 Keandalan Transmisi & Jaringan Interkoneksi Regional</span>
        </div>
        <div style="font-size:11px; color:var(--text-muted);">
          SUTET 500 kV, SUTT 150/275 kV, dan Interkoneksi Eksternal SESCO
        </div>
      </div>

      <div class="kpi-grid">
        <div class="kpi-card" style="--card-accent: #00A3E0;" onclick="focusSpecificSystem('Khatulistiwa')">
          <div class="kpi-title">Transfer Interkoneksi SESCO</div>
          <div class="kpi-value" style="color:#00A3E0;">80,0 <span style="font-size:13px;">MW</span></div>
          <div class="kpi-sub">Impor 275 kV Sarawak - Khatulistiwa</div>
        </div>
        <div class="kpi-card" style="--card-accent: #10B981;" onclick="zoomToIsland('sumatera')">
          <div class="kpi-title">Tol Listrik Sumatera</div>
          <div class="kpi-value">275 <span style="font-size:13px;">kV</span></div>
          <div class="kpi-sub">Interkoneksi aktif Sumatera Utara - Selatan</div>
        </div>
        <div class="kpi-card" style="--card-accent: #3B82F6;" onclick="zoomToIsland('jawa')">
          <div class="kpi-title">Grid Interkoneksi Jamali</div>
          <div class="kpi-value">500 <span style="font-size:13px;">kV</span></div>
          <div class="kpi-sub">Tulang punggung transmisi Jawa-Madura-Bali</div>
        </div>
        <div class="kpi-card" style="--card-accent: #F59E0B;" onclick="zoomToIsland('kalimantan')">
          <div class="kpi-title">Interkoneksi Kalimantan</div>
          <div class="kpi-value">150 <span style="font-size:13px;">kV</span></div>
          <div class="kpi-sub">Grid interkoneksi Kalselteng - Kaltim</div>
        </div>
      </div>

      <div class="table-container" style="margin-top:16px;">
        <div class="table-toolbar">
          <strong style="font-size:12.5px;">Daftar 49 Sistem Interkoneksi Utama Nasional</strong>
        </div>
        <div style="overflow-x:auto;">
          <table class="data-table">
            <thead>
              <tr>
                <th>No</th>
                <th>Sistem Interkoneksi</th>
                <th>Wilayah / Unit</th>
                <th>Regional</th>
                <th>DMP (MW)</th>
                <th>Beban Puncak (MW)</th>
                <th>Cadangan (MW)</th>
                <th>Status</th>
                <th>Aksi</th>
              </tr>
            </thead>
            <tbody id="transmisiTableBody">
              <!-- Populated by JS -->
            </tbody>
          </table>
        </div>
      </div>
    </section>

    <!-- ========================================== -->
    <!-- TAB 6: DISTRIBUSI & BEBAN -->
    <!-- ========================================== -->
    <section id="tab-distribusi" class="tab-content">
      <div class="box-header">
        <div class="box-title">
          <span>🔌 Analitik Distribusi Beban Konsumsi (Peak Load Dispatch)</span>
        </div>
        <div style="font-size:11px; color:var(--text-muted);">
          Distribusi Total Beban Puncak Nasional: <strong>55.246,0 MW</strong>
        </div>
      </div>

      <div class="kpi-grid">
        <div class="kpi-card" style="--card-accent: #FDB913;" onclick="focusSpecificSystem('Jamali')">
          <div class="kpi-title">Beban Terbesar (Jamali)</div>
          <div class="kpi-value">~35.086,0 <span style="font-size:13px;">MW</span></div>
          <div class="kpi-sub">>60% total konsumsi nasional</div>
        </div>
        <div class="kpi-card" style="--card-accent: #3B82F6;" onclick="zoomToIsland('sumatera')">
          <div class="kpi-title">Beban Region Sumatera</div>
          <div class="kpi-value">~9.037,0 <span style="font-size:13px;">MW</span></div>
          <div class="kpi-sub">Sumatera + Batam + Nias + Belitung + Isolated</div>
        </div>
        <div class="kpi-card" style="--card-accent: #10B981;" onclick="zoomToIsland('kalimantan')">
          <div class="kpi-title">Beban Region Kalimantan</div>
          <div class="kpi-value">~2.829,0 <span style="font-size:13px;">MW</span></div>
          <div class="kpi-sub">Grid Kalseltengtim + Khatulistiwa + Isolated</div>
        </div>
        <div class="kpi-card" style="--card-accent: #8B5CF6;" onclick="zoomToIsland('sulawesi')">
          <div class="kpi-title">Beban Region Sulawesi</div>
          <div class="kpi-value">~2.752,0 <span style="font-size:13px;">MW</span></div>
          <div class="kpi-sub">Sulbagsel + Sulutgo + Bau-Bau + Isolated</div>
        </div>
      </div>

      <div class="table-container" style="margin-top:16px;">
        <div class="table-toolbar">
          <strong style="font-size:12.5px;">Matriks Distribusi Beban Puncak Per Wilayah</strong>
        </div>
        <div style="overflow-x:auto;">
          <table class="data-table">
            <thead>
              <tr>
                <th>No</th>
                <th>Sistem</th>
                <th>Regional</th>
                <th>Jenis</th>
                <th>Jam Nyala</th>
                <th>Beban Puncak (MW)</th>
                <th>Pangsa Beban (%)</th>
                <th>DMP (MW)</th>
                <th>Cadangan (MW)</th>
                <th>Status</th>
                <th>Aksi</th>
              </tr>
            </thead>
            <tbody id="distribusiTableBody">
              <!-- Populated by JS -->
            </tbody>
          </table>
        </div>
      </div>
    </section>

    <!-- ========================================== -->
    <!-- TAB 7: DETAIL DATA (910 SISTEM) -->
    <!-- ========================================== -->
    <section id="tab-detail" class="tab-content">
      <div class="box-header">
        <div class="box-title">
          <span>📑 Matriks Lengkap Data 910 Sistem Kelistrikan Nasional PLN</span>
        </div>
        <div style="display:flex; gap:8px;">
          <button class="btn" onclick="exportCSV()">📥 Ekspor CSV (910 Sistem)</button>
          <button class="btn" onclick="exportJSON()">📥 Ekspor JSON</button>
        </div>
      </div>

      <div class="table-container">
        <div class="table-toolbar">
          <div style="display:flex; align-items:center; gap:10px; flex-wrap:wrap;">
            <div class="search-box">
              <span class="search-icon">🔍</span>
              <input type="text" id="searchInput" class="search-input" placeholder="Cari nama sistem, unit, wilayah, keterangan..." oninput="onSearchChange(this.value)">
            </div>

            <!-- Quick Status Filters -->
            <div style="display:flex; gap:6px; flex-wrap:wrap;">
              <button class="btn active" id="btnFilterAll" onclick="setFilterStatus('all')">Semua (910)</button>
              <button class="btn" id="btnFilterDefisit" onclick="setFilterStatus('defisit')">🔴 Defisit (57)</button>
              <button class="btn" id="btnFilterSiaga" onclick="setFilterStatus('siaga')">🟡 Siaga (467)</button>
              <button class="btn" id="btnFilterNormal" onclick="setFilterStatus('normal')">🟢 Normal (224)</button>
              <button class="btn" id="btnFilterUnfilled" onclick="setFilterStatus('unfilled')">⚪ Belum Terisi (162)</button>
            </div>
          </div>

          <div style="display:flex; align-items:center; gap:12px;">
            <div style="font-size:11px; color:var(--text-dim);" id="tableRowCountDisplay">
              Menampilkan 910 sistem
            </div>
            <select id="pageSizeSelect" class="btn" style="padding:4px 8px; font-size:11px;" onchange="changePageSize(this.value)">
              <option value="25">25 per hal</option>
              <option value="50" selected>50 per hal</option>
              <option value="100">100 per hal</option>
              <option value="9999">Tampilkan Semua</option>
            </select>
          </div>
        </div>

        <div style="overflow-x:auto;">
          <table class="data-table" id="mainDetailTable">
            <thead>
              <tr>
                <th onclick="sortTable('no')">No <span id="sort-no">↕</span></th>
                <th onclick="sortTable('name')">Nama Sistem <span id="sort-name">↕</span></th>
                <th onclick="sortTable('unit')">Unit / Wilayah <span id="sort-unit">↕</span></th>
                <th onclick="sortTable('region')">Regional <span id="sort-region">↕</span></th>
                <th onclick="sortTable('jenis')">Jenis <span id="sort-jenis">↕</span></th>
                <th onclick="sortTable('jam_operasi')">Jam Nyala <span id="sort-jam_operasi">↕</span></th>
                <th onclick="sortTable('dmp')">DMP (MW) <span id="sort-dmp">↕</span></th>
                <th onclick="sortTable('bp')">BP (MW) <span id="sort-bp">↕</span></th>
                <th onclick="sortTable('cad_mw')">Cadangan (MW) <span id="sort-cad_mw">↕</span></th>
                <th onclick="sortTable('cad_pct')">Cadangan (%) <span id="sort-cad_pct">↕</span></th>
                <th onclick="sortTable('status')">Status <span id="sort-status">↕</span></th>
                <th>Keterangan Validasi</th>
                <th>Aksi</th>
              </tr>
            </thead>
            <tbody id="detailTableBody">
              <!-- Populated by JS -->
            </tbody>
          </table>
        </div>

        <!-- Table Pagination Footer -->
        <div class="table-pagination-footer">
          <div id="paginationInfo">Menampilkan 1 - 50 dari 910 sistem</div>
          <div class="pagination-controls">
            <button class="page-btn" id="btnFirstPage" onclick="goToPage(1)">⏮️ Pertama</button>
            <button class="page-btn" id="btnPrevPage" onclick="changePage(-1)">◀️ Sebelumnya</button>
            <span style="font-size:11px; margin:0 6px;">Halaman <strong id="currentPageLabel">1</strong> dari <strong id="totalPageLabel">19</strong></span>
            <button class="page-btn" id="btnNextPage" onclick="changePage(1)">Berikutnya ▶️</button>
            <button class="page-btn" id="btnLastPage" onclick="goToLastPage()">Terakhir ⏭️</button>
          </div>
        </div>
      </div>
    </section>

  </main>

  <!-- ========================================== -->
  <!-- MODAL: DETAIL SISTEM SPESIFIK -->
  <!-- ========================================== -->
  <div id="systemDetailModal" class="modal-overlay" onclick="if(event.target===this) closeSystemModal()">
    <div class="modal-window">
      <div class="modal-header">
        <div class="modal-title" id="modalSystemName">Detail Sistem Kelistrikan</div>
        <button class="modal-close" onclick="closeSystemModal()">&times;</button>
      </div>
      <div class="modal-body" id="modalSystemContent">
        <!-- Injected by JS -->
      </div>
    </div>
  </div>

  <!-- ========================================== -->
  <!-- MODAL: SUMBER DATA & UPLOAD EXCEL -->
  <!-- ========================================== -->
  <div id="syncModal" class="modal-overlay" onclick="if(event.target===this) closeSyncModal()">
    <div class="modal-window">
      <div class="modal-header">
        <div class="modal-title">📁 Sumber Data SharePoint & Unggah Pembaruan</div>
        <button class="modal-close" onclick="closeSyncModal()">&times;</button>
      </div>
      <div class="modal-body">
        <p><strong>Sumber Data Resmi:</strong></p>
        <p style="background:var(--bg-card-alt); padding:8px; border-radius:6px; word-break:break-all; font-family:monospace; font-size:10px; margin:4px 0 10px; border:1px solid var(--border-color); color:var(--pln-cyan);">
          https://ptpln365-my.sharepoint.com/:x:/g/personal/mohammad_anang_ptpln365_onmicrosoft_com/IQAP_S2PC7-nTYf6tBRkQH84AVwSj7Q2cMy0F3SeSkPgDho?e=xNbMWb
        </p>

        <p><strong>Metadata Workbook Terdeteksi:</strong></p>
        <ul style="margin:4px 0 12px 18px; color:var(--text-main); font-size:11.5px;">
          <li>Judul Berkas: <strong id="modalWbTitle">Monitoring Status 910 Sistem Kelistrikan</strong></li>
          <li>Editor Terakhir: <strong id="modalWbAuthor">MOHAMMAD ANANG FACHRUDIN</strong></li>
          <li>Lembar Kerja Sumber: <strong id="modalWbSheets">Rekap Sistem (910 Sistem), Ringkasan</strong></li>
          <li>Status Integritas: <span style="color:#10B981; font-weight:700;">100% Data Riil Terverifikasi (910 Sistem)</span></li>
        </ul>

        <div style="background:rgba(0,163,224,0.08); border:1px solid rgba(0,163,224,0.3); border-radius:6px; padding:12px; margin-bottom:14px;">
          <strong style="color:var(--pln-cyan); font-size:12px;">Unggah File Excel Pembaruan (.xlsx):</strong>
          <p style="font-size:11px; margin:4px 0 8px;">Unggah file Excel pembaruan untuk disinkronkan seketika ke dashboard tanpa merusak struktur data.</p>
          <input type="file" id="fileUploadInput" accept=".xlsx" style="font-size:11px;" onchange="uploadNewExcel(event)">
        </div>

        <div style="text-align:right;">
          <button class="btn btn-primary" onclick="triggerManualRefresh(); closeSyncModal();">Sinkronkan Ulang Sekarang</button>
        </div>
      </div>
    </div>
  </div>

  <!-- ========================================== -->
  <!-- FLOATING CHATBOT WIDGET -->
  <!-- ========================================== -->
  <button id="chatbotToggle" class="chatbot-fab" onclick="toggleChatbot()" title="Buka Asisten Cerdas AI PLN">
    <div style="font-size:20px;">⚡</div>
    <span>Asisten AI PLN</span>
  </button>

  <div id="chatbotDrawer" class="chatbot-drawer" role="dialog" aria-label="Asisten AI Monitoring PLN">
    <div class="chatbot-header">
      <div class="chatbot-header-info">
        <div class="chatbot-avatar">⚡</div>
        <div>
          <div class="chatbot-title">
            Asisten Cerdas PLN
            <span class="chatbot-status-pill">Online (910 Sistem)</span>
          </div>
          <div class="chatbot-subtitle">Tanya Teknis & Non-Teknis 910 Sistem Realtime</div>
        </div>
      </div>
      <div style="display:flex; gap:6px;">
        <button class="btn btn-icon" onclick="clearChatHistory()" title="Bersihkan">🗑️</button>
        <button class="btn btn-icon" onclick="toggleChatbot()" title="Tutup">✕</button>
      </div>
    </div>

    <div id="chatbotBody" class="chatbot-body">
      <div class="chat-bubble bot">
        <div style="font-weight:700; color:var(--pln-cyan); margin-bottom:4px;">👋 Halo! Saya Asisten AI Monitoring 910 Sistem PLN.</div>
        <div>Saya siap membantu menganalisis seluruh data <strong>910 Sistem Kelistrikan Nasional</strong>:</div>
        <ul style="margin:6px 0 6px 16px; font-size:11px;">
          <li><strong>Sistem Isolated (645):</strong> Pola jam nyala 24 jam (412 sistem), 12 jam (197 sistem), dan 6 jam (36 sistem).</li>
          <li><strong>Interkoneksi (49) & ULD (216):</strong> Neraca daya grid besar dan listrik pedesaan.</li>
          <li><strong>Sistem Defisit (57):</strong> Analisis sistem dengan cadangan daya negatif.</li>
          <li><strong>Pencarian Spesifik:</strong> Tanyakan sistem mana pun (e.g. Tanakeke, Leok, Karimun, Sulbagsel, Jamali).</li>
        </ul>
        <div class="chat-meta">⚡ Asisten AI PLN • Sekarang</div>
      </div>

      <div id="chatTyping" class="chat-typing">
        <span></span><span></span><span></span>
        <span style="font-size:10px; color:var(--text-dim); margin-left:6px;">Menganalisis 910 sistem...</span>
      </div>
    </div>

    <!-- Quick Suggestions -->
    <div class="chatbot-suggestions">
      <div class="chat-chip" onclick="askQuickPrompt('Bagaimana kondisi sistem isolated di Indonesia?')">🏝️ Sistem Isolated?</div>
      <div class="chat-chip" onclick="askQuickPrompt('Jelaskan jam operasi 24 jam, 12 jam, dan 6 jam')">⏱️ Jam Nyala 24/12/6?</div>
      <div class="chat-chip" onclick="askQuickPrompt('Sistem mana saja yang mengalami defisit?')">🔴 57 Sistem Defisit?</div>
      <div class="chat-chip" onclick="askQuickPrompt('Jelaskan tentang Unit Listrik Desa (ULD)')">🏘️ ULD (Listrik Desa)?</div>
      <div class="chat-chip" onclick="askQuickPrompt('Bagaimana status sistem Tanakeke?')">📍 Sistem Tanakeke?</div>
      <div class="chat-chip" onclick="askQuickPrompt('Bagaimana kondisi sistem Leok?')">📍 Sistem Leok?</div>
      <div class="chat-chip" onclick="askQuickPrompt('Ringkasan 910 sistem kelistrikan PLN')">📊 Ringkasan 910 Sistem</div>
    </div>

    <!-- Input Bar -->
    <div class="chatbot-input-row">
      <input type="text" id="chatInput" class="chatbot-input" placeholder="Tanyakan seputar 910 sistem kelistrikan... (Enter)" onkeydown="if(event.key==='Enter') sendChatMessage()">
      <button class="chatbot-send-btn" onclick="sendChatMessage()">
        <span>Kirim</span>
        <span>➤</span>
      </button>
    </div>
  </div>

  <!-- Toast Notification -->
  <div id="toast">
    <span id="toastIcon">✓</span>
    <span id="toastMsg">Data berhasil dimuat!</span>
  </div>

  <!-- ========================================== -->
  <!-- APPLICATION JAVASCRIPT LOGIC -->
  <!-- ========================================== -->
  <script>
    let appData = null;
    let leafletMap = null;
    let markersLayerGroup = null;
    let geojsonLayer = null;
    let mapTileLayer = null;
    let systemMarkersMap = {};

    let autoRefreshTimer = null;
    let autoRefreshSeconds = 30;
    let countdownRemaining = 30;
    let countdownTicker = null;

    // Filters
    let currentFilterStatus = 'all'; // 'all', 'defisit', 'siaga', 'normal', 'unfilled'
    let currentFilterJenis = 'all';  // 'all', 'interkoneksi', 'isolated', 'uld'
    let currentFilterJam = 'all';    // 'all', '24h', '12h', '6h'
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
      nusa: { center: [-8.6, 119.5], zoom: 7 },
      maluku_papua: { center: [-3.5, 134.0], zoom: 6 }
    };

    function formatNum(n) {
      if (n === null || n === undefined || isNaN(n)) return '0';
      return Number(n).toLocaleString('id-ID', { maximumFractionDigits: 1 });
    }

    function showToast(msg, isError = false) {
      const toast = document.getElementById('toast');
      const msgEl = document.getElementById('toastMsg');
      const iconEl = document.getElementById('toastIcon');

      msgEl.innerText = msg;
      iconEl.innerText = isError ? '⚠️' : '✓';
      toast.style.backgroundColor = isError ? '#DC2626' : '#10B981';

      toast.classList.add('show');
      setTimeout(() => {
        toast.classList.remove('show');
      }, 3000);
    }

    // Dynamic Tooltip
    const tooltipEl = document.getElementById('dynamicTooltip');

    function showGlobalTooltip(evt, htmlContent) {
      if (!tooltipEl) return;
      tooltipEl.innerHTML = htmlContent;
      tooltipEl.style.display = 'block';
      tooltipEl.classList.add('show');
      positionGlobalTooltip(evt);
    }

    function hideGlobalTooltip() {
      if (!tooltipEl) return;
      tooltipEl.classList.remove('show');
      tooltipEl.style.display = 'none';
    }

    function positionGlobalTooltip(evt) {
      if (!tooltipEl || !evt) return;
      const pad = 16;
      let x = evt.clientX + pad;
      let y = evt.clientY + pad;

      const rect = tooltipEl.getBoundingClientRect();
      const winW = window.innerWidth;
      const winH = window.innerHeight;

      if (x + rect.width > winW - 12) {
        x = evt.clientX - rect.width - pad;
      }
      if (y + rect.height > winH - 12) {
        y = evt.clientY - rect.height - pad;
      }
      if (x < 10) x = 10;
      if (y < 10) y = 10;

      tooltipEl.style.left = x + 'px';
      tooltipEl.style.top = y + 'px';
    }

    document.addEventListener('mousemove', (e) => {
      if (tooltipEl && tooltipEl.style.display === 'block') {
        positionGlobalTooltip(e);
      }
    });

    function generateSystemTooltip(s) {
      if (!s) return '';
      const isDefisit = s.cad_mw < 0;
      return `
        <div class="tooltip-header">
          <div class="tooltip-title">${s.no}. ${s.name}</div>
          <span class="status-badge ${s.status_code}">${s.status}</span>
        </div>
        <div style="font-size:10.5px; color:var(--text-dim); margin-bottom:6px;">
          ${s.unit} • <strong>${s.region}</strong>
        </div>
        <div style="display:flex; gap:6px; margin-bottom:8px;">
          <span class="tag-badge ${s.jenis_code === 'isolated' ? 'tag-isolated' : (s.jenis_code === 'interkoneksi' ? 'tag-interkoneksi' : 'tag-uld')}">${s.jenis}</span>
          <span class="tag-badge ${s.jam_code === '24h' ? 'tag-jam-24' : (s.jam_code === '12h' ? 'tag-jam-12' : 'tag-jam-6')}">${s.jam_operasi}</span>
        </div>
        <div class="tooltip-grid">
          <div>• DMP: <strong style="color:#00A3E0;">${formatNum(s.dmp)} MW</strong></div>
          <div>• Beban: <strong style="color:#FDB913;">${formatNum(s.bp)} MW</strong></div>
          <div>• Terpasang: <strong>${formatNum(s.daya_terpasang)} MW</strong></div>
          <div>• Cadangan: <strong style="color:${isDefisit ? '#EF4444' : '#10B981'};">${s.cad_mw >= 0 ? '+' : ''}${formatNum(s.cad_mw)} MW</strong></div>
        </div>
        <div style="font-size:10px; color:var(--text-muted); margin-top:4px;">${s.keterangan}</div>
        <div class="tooltip-hint">💡 Klik marker untuk membuka detail lengkap</div>
      `;
    }

    function copyNetworkIp() {
      const el = document.getElementById('networkIpDisplay');
      const url = el ? el.innerText : 'http://192.168.0.116:8080';
      navigator.clipboard.writeText(url).then(() => {
        showToast("Tautan akses disalin: " + url);
      }).catch(() => {
        showToast("Akses di: " + url);
      });
    }

    async function checkServerStatus() {
      try {
        const res = await fetch('/api/status');
        const st = await res.json();
        if (st && st.network_url) {
          const el = document.getElementById('networkIpDisplay');
          if (el) el.innerText = st.network_url;
        }
      } catch (e) {}
    }

    async function loadData(isRefresh = false) {
      try {
        const endpoint = isRefresh ? '/api/refresh' : '/api/data';
        const res = await fetch(endpoint, { method: isRefresh ? 'POST' : 'GET' });
        const json = await res.json();
        const data = isRefresh ? json.data : json;

        if (data && data.systems) {
          appData = data;
          renderDashboard(appData);
          if (isRefresh) showToast("Data 910 sistem berhasil disinkronkan!");
        }
      } catch (err) {
        showToast("Gagal memuat data: " + err.message, true);
      }
    }

    function triggerManualRefresh() {
      loadData(true);
    }

    function renderDashboard(data) {
      const kpi = data.kpi_summary;
      const src = data.source_info;

      document.getElementById('lastUpdatedWib').innerText = data.last_updated_wib || '—';
      document.getElementById('kpiTotalSistem').innerHTML = `${kpi.total_sistem} <span style="font-size:14px; font-weight:600;">Sistem</span>`;
      document.getElementById('kpiDmp').innerHTML = `${formatNum(kpi.total_dmp_mw)} <span style="font-size:14px; font-weight:600;">MW</span>`;
      document.getElementById('kpiBp').innerHTML = `${formatNum(kpi.total_bp_mw)} <span style="font-size:14px; font-weight:600;">MW</span>`;
      document.getElementById('kpiCad').innerHTML = `${kpi.total_cad_mw >= 0 ? '+' : ''}${formatNum(kpi.total_cad_mw)} <span style="font-size:14px; font-weight:600;">MW</span>`;
      document.getElementById('kpiCadSub').innerHTML = `Reserve Margin: <strong>${kpi.overall_reserve_margin_pct}%</strong>`;
      document.getElementById('kpiDefisitVal').innerHTML = `${kpi.status_counts.defisit} <span style="font-size:14px; font-weight:600;">Sistem</span>`;

      // Status Counts
      document.getElementById('countDefisit').innerText = `${kpi.status_counts.defisit} Sistem`;
      document.getElementById('countSiaga').innerText = `${kpi.status_counts.siaga} Sistem`;
      document.getElementById('countNormal').innerText = `${kpi.status_counts.normal} Sistem`;
      document.getElementById('countUnfilled').innerText = `${kpi.status_counts.unfilled} Sistem`;

      // Badge Counts
      document.getElementById('badgeCountInter').innerText = kpi.jenis_counts.interkoneksi || 49;
      document.getElementById('badgeCountIso').innerText = kpi.jenis_counts.isolated || 645;
      document.getElementById('badgeCountUld').innerText = kpi.jenis_counts.uld || 216;

      document.getElementById('badgeCount24h').innerText = kpi.jam_operasi_counts['24h'] || 537;
      document.getElementById('badgeCount12h').innerText = kpi.jam_operasi_counts['12h'] || 305;
      document.getElementById('badgeCount6h').innerText = kpi.jam_operasi_counts['6h'] || 68;

      // Deficit Spotlight
      renderDeficitSpotlight(data.systems.filter(s => s.status_code === 'defisit'));

      // Modal Metadata
      document.getElementById('modalWbTitle').innerText = src.workbook_title;
      document.getElementById('modalWbAuthor').innerText = src.author;

      // Views
      renderRegionalCards(data.regions);
      renderIsolatedTable(data.systems.filter(s => s.jenis_code === 'isolated'));
      renderPembangkitTable(data.systems);
      renderGarduIndukTable(data.systems);
      renderTransmisiTable(data.systems.filter(s => s.jenis_code === 'interkoneksi'));
      renderDistribusiTable(data.systems, kpi.total_bp_mw);
      renderDetailTable();
      initOrUpdateMap();
      updateFilterBarUI();
    }

    function renderDeficitSpotlight(deficits) {
      const container = document.getElementById('deficitSpotlightContainer');
      const sorted = [...deficits].sort((a, b) => a.cad_mw - b.cad_mw);

      container.innerHTML = sorted.map(s => `
        <div class="status-count-row" style="margin-bottom:0;" onclick="focusSpecificSystem('${s.name}')">
          <div>
            <div style="font-weight:700;">${s.name}</div>
            <div style="color:var(--text-dim); font-size:10px;">${s.region} • ${s.jenis} (${s.jam_operasi})</div>
          </div>
          <strong style="color:#EF4444; font-size:12px;">${formatNum(s.cad_mw)} MW</strong>
        </div>
      `).join('');
    }

    function renderRegionalCards(regions) {
      const container = document.getElementById('regionalCardsContainer');
      container.innerHTML = regions.map(r => `
        <div class="regional-card" onclick="filterByRegion('${r.region}')" onmouseenter="showRegionalCardTooltip(event, '${r.region}')" onmouseleave="hideGlobalTooltip()">
          <div class="regional-header">
            <span class="regional-title">${r.region}</span>
            <span style="font-size:10px; color:var(--text-dim);">${r.count} Sistem</span>
          </div>
          <div class="metric-row">
            <span>DMP vs Beban Puncak:</span>
            <strong>${formatNum(r.dmp)} / ${formatNum(r.bp)} MW</strong>
          </div>
          <div class="metric-row">
            <span>Cadangan Daya:</span>
            <strong style="color:${r.cad_mw < 0 ? '#EF4444' : (r.cad_mw < 100 ? '#F59E0B' : '#10B981')};">
              ${r.cad_mw >= 0 ? '+' : ''}${formatNum(r.cad_mw)} MW (${r.reserve_margin_pct}%)
            </strong>
          </div>
          <div class="metric-row">
            <span>Status Sistem:</span>
            <div>
              ${r.defisit > 0 ? `<span class="status-badge defisit">${r.defisit} Defisit</span> ` : ''}
              ${r.siaga > 0 ? `<span class="status-badge siaga">${r.siaga} Siaga</span> ` : ''}
              ${r.normal > 0 ? `<span class="status-badge normal">${r.normal} Normal</span>` : ''}
            </div>
          </div>
          <div class="metric-row" style="margin-top:6px; font-size:10.5px; color:var(--text-dim);">
            <span>Pola Nyala: <strong>${r.count_24h} (24j)</strong> • <strong>${r.count_12h} (12j)</strong> • <strong>${r.count_6h} (6j)</strong></span>
          </div>
        </div>
      `).join('');
    }

    function showRegionalCardTooltip(e, regName) {
      if (!appData) return;
      const r = appData.regions.find(item => item.region === regName);
      if (!r) return;
      const html = `
        <div class="tooltip-header">
          <span class="tooltip-title">🌐 Wilayah ${r.region}</span>
          <span style="font-size:10.5px; font-weight:700;">${r.count} Sistem</span>
        </div>
        <div class="tooltip-grid">
          <div>• DMP: <strong>${formatNum(r.dmp)} MW</strong></div>
          <div>• Beban: <strong>${formatNum(r.bp)} MW</strong></div>
          <div>• Cadangan: <strong>${r.cad_mw >= 0 ? '+' : ''}${formatNum(r.cad_mw)} MW</strong></div>
          <div>• Margin: <strong>${r.reserve_margin_pct}%</strong></div>
        </div>
        <div style="font-size:10.5px; margin-top:4px;">
          Pola operasi: 24 Jam (${r.count_24h}), 12 Jam (${r.count_12h}), 6 Jam (${r.count_6h})
        </div>
        <div class="tooltip-hint">💡 Klik untuk menyaring tabel & memfokuskan peta ke wilayah ini</div>
      `;
      showGlobalTooltip(e, html);
    }

    // Isolated Table View
    function renderIsolatedTable(isolatedSystems) {
      const tbody = document.getElementById('isolatedTableBody');
      const previewList = isolatedSystems.slice(0, 30);
      tbody.innerHTML = previewList.map(s => `
        <tr onclick="openSystemModal(${s.no})" style="cursor:pointer;">
          <td>${s.no}</td>
          <td><strong>${s.name}</strong></td>
          <td>${s.unit}</td>
          <td>${s.region}</td>
          <td><span class="tag-badge ${s.jam_code === '24h' ? 'tag-jam-24' : (s.jam_code === '12h' ? 'tag-jam-12' : 'tag-jam-6')}">${s.jam_operasi}</span></td>
          <td>${formatNum(s.dmp)}</td>
          <td>${formatNum(s.bp)}</td>
          <td style="color:${s.cad_mw < 0 ? '#EF4444' : '#10B981'}; font-weight:700;">${s.cad_mw >= 0 ? '+' : ''}${formatNum(s.cad_mw)}</td>
          <td><span class="status-badge ${s.status_code}">${s.status}</span></td>
          <td style="max-width:280px; white-space:normal; font-size:11px; color:var(--text-muted);">${s.keterangan}</td>
          <td><button class="btn" style="padding:2px 7px; font-size:10px;" onclick="event.stopPropagation(); openSystemModal(${s.no})">Detail</button></td>
        </tr>
      `).join('');
    }

    function filterIsolatedByJam(jamCode) {
      switchTab('detail');
      setFilterJenis('isolated');
      if (jamCode !== 'all') {
        setFilterJam(jamCode);
      }
    }

    // Pembangkit Table
    function renderPembangkitTable(systems) {
      const tbody = document.getElementById('pembangkitTableBody');
      tbody.innerHTML = systems.slice(0, 50).map(s => `
        <tr onclick="openSystemModal(${s.no})" style="cursor:pointer;">
          <td>${s.no}</td>
          <td><strong>${s.name}</strong></td>
          <td>${s.unit}</td>
          <td><span class="tag-badge ${s.jenis_code === 'isolated' ? 'tag-isolated' : 'tag-interkoneksi'}">${s.jenis}</span></td>
          <td>${s.jam_operasi}</td>
          <td><strong style="color:#00A3E0;">${formatNum(s.dmp)}</strong></td>
          <td><strong style="color:#FDB913;">${formatNum(s.bp)}</strong></td>
          <td style="color:${s.cad_mw < 0 ? '#EF4444' : '#10B981'}; font-weight:700;">${s.cad_mw >= 0 ? '+' : ''}${formatNum(s.cad_mw)}</td>
          <td><span class="status-badge ${s.status_code}">${s.status}</span></td>
          <td><button class="btn" style="padding:2px 7px; font-size:10px;" onclick="event.stopPropagation(); openSystemModal(${s.no})">Detail</button></td>
        </tr>
      `).join('');
    }

    // Gardu Induk Table
    function renderGarduIndukTable(systems) {
      const tbody = document.getElementById('garduIndukTableBody');
      tbody.innerHTML = systems.slice(0, 50).map(s => `
        <tr onclick="openSystemModal(${s.no})" style="cursor:pointer;">
          <td>${s.no}</td>
          <td><strong>${s.name}</strong></td>
          <td>${s.region}</td>
          <td><span class="tag-badge ${s.jenis_code === 'isolated' ? 'tag-isolated' : 'tag-interkoneksi'}">${s.jenis}</span></td>
          <td>${s.jam_operasi}</td>
          <td>${formatNum(s.dmp)}</td>
          <td><strong style="color:#FDB913;">${formatNum(s.bp)}</strong></td>
          <td style="color:${s.cad_mw < 0 ? '#EF4444' : '#10B981'}; font-weight:700;">${s.cad_mw >= 0 ? '+' : ''}${formatNum(s.cad_mw)}</td>
          <td><span class="status-badge ${s.status_code}">${s.status}</span></td>
          <td><button class="btn" style="padding:2px 7px; font-size:10px;" onclick="event.stopPropagation(); openSystemModal(${s.no})">Detail</button></td>
        </tr>
      `).join('');
    }

    // Transmisi Table
    function renderTransmisiTable(interSystems) {
      const tbody = document.getElementById('transmisiTableBody');
      tbody.innerHTML = interSystems.map(s => `
        <tr onclick="openSystemModal(${s.no})" style="cursor:pointer;">
          <td>${s.no}</td>
          <td><strong>${s.name}</strong></td>
          <td>${s.unit}</td>
          <td>${s.region}</td>
          <td><strong style="color:#00A3E0;">${formatNum(s.dmp)}</strong></td>
          <td><strong style="color:#FDB913;">${formatNum(s.bp)}</strong></td>
          <td style="color:${s.cad_mw < 0 ? '#EF4444' : '#10B981'}; font-weight:700;">${s.cad_mw >= 0 ? '+' : ''}${formatNum(s.cad_mw)}</td>
          <td><span class="status-badge ${s.status_code}">${s.status}</span></td>
          <td><button class="btn" style="padding:2px 7px; font-size:10px;" onclick="event.stopPropagation(); openSystemModal(${s.no})">Detail</button></td>
        </tr>
      `).join('');
    }

    // Distribusi Table
    function renderDistribusiTable(systems, totalBp) {
      const tbody = document.getElementById('distribusiTableBody');
      tbody.innerHTML = systems.slice(0, 50).map(s => {
        const share = totalBp ? (s.bp / totalBp * 100).toFixed(2) : '0';
        return `
          <tr onclick="openSystemModal(${s.no})" style="cursor:pointer;">
            <td>${s.no}</td>
            <td><strong>${s.name}</strong></td>
            <td>${s.region}</td>
            <td>${s.jenis}</td>
            <td>${s.jam_operasi}</td>
            <td><strong>${formatNum(s.bp)}</strong></td>
            <td>${share}%</td>
            <td>${formatNum(s.dmp)}</td>
            <td style="color:${s.cad_mw < 0 ? '#EF4444' : '#10B981'}; font-weight:700;">${s.cad_mw >= 0 ? '+' : ''}${formatNum(s.cad_mw)}</td>
            <td><span class="status-badge ${s.status_code}">${s.status}</span></td>
            <td><button class="btn" style="padding:2px 7px; font-size:10px;" onclick="event.stopPropagation(); openSystemModal(${s.no})">Detail</button></td>
          </tr>
        `;
      }).join('');
    }

    // Detail Table with Multi-filtering, Search, Sorting, and Pagination
    function getFilteredList() {
      if (!appData) return [];
      let list = [...appData.systems];

      if (currentFilterStatus !== 'all') {
        list = list.filter(s => s.status_code === currentFilterStatus);
      }
      if (currentFilterJenis !== 'all') {
        list = list.filter(s => s.jenis_code === currentFilterJenis);
      }
      if (currentFilterJam !== 'all') {
        list = list.filter(s => s.jam_code === currentFilterJam);
      }
      if (currentFilterRegion) {
        list = list.filter(s => s.region.toLowerCase() === currentFilterRegion.toLowerCase());
      }
      if (currentSearchQuery) {
        const q = currentSearchQuery.toLowerCase();
        list = list.filter(s => 
          s.name.toLowerCase().includes(q) ||
          s.unit.toLowerCase().includes(q) ||
          s.region.toLowerCase().includes(q) ||
          s.jenis.toLowerCase().includes(q) ||
          s.jam_operasi.toLowerCase().includes(q) ||
          s.keterangan.toLowerCase().includes(q) ||
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

      document.getElementById('tableRowCountDisplay').innerText = `Menampilkan ${totalItems} dari ${appData ? appData.systems.length : 0} sistem`;
      document.getElementById('paginationInfo').innerText = totalItems > 0 ? `Menampilkan ${startIndex + 1} - ${endIndex} dari ${totalItems} sistem` : 'Tidak ada sistem yang cocok';
      document.getElementById('currentPageLabel').innerText = currentPage;
      document.getElementById('totalPageLabel').innerText = totalPages;

      document.getElementById('btnFirstPage').disabled = (currentPage === 1);
      document.getElementById('btnPrevPage').disabled = (currentPage === 1);
      document.getElementById('btnNextPage').disabled = (currentPage === totalPages);
      document.getElementById('btnLastPage').disabled = (currentPage === totalPages);

      ['no', 'name', 'unit', 'region', 'jenis', 'jam_operasi', 'dmp', 'bp', 'cad_mw', 'cad_pct', 'status'].forEach(col => {
        const el = document.getElementById('sort-' + col);
        if (el) el.innerText = (sortColumn === col) ? (sortAsc ? '▲' : '▼') : '↕';
      });

      const tbody = document.getElementById('detailTableBody');
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
            ${s.keterangan.length > 70 ? s.keterangan.substring(0, 70) + '…' : s.keterangan}
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

    function changePageSize(val) {
      pageSize = parseInt(val, 10);
      currentPage = 1;
      renderDetailTable();
    }

    function onTableRowHover(sysNo, evt) {
      if (!appData) return;
      const s = appData.systems.find(item => item.no === sysNo);
      if (!s) return;
      showGlobalTooltip(evt, generateSystemTooltip(s));

      const marker = systemMarkersMap[sysNo];
      if (marker && marker._icon) {
        marker._icon.classList.add('radar-marker-pulse-active');
      }
    }

    function onTableRowLeave(sysNo) {
      hideGlobalTooltip();
      const marker = systemMarkersMap[sysNo];
      if (marker && marker._icon) {
        marker._icon.classList.remove('radar-marker-pulse-active');
      }
    }

    function onSearchChange(val) {
      currentSearchQuery = val;
      currentPage = 1;
      updateFilterBarUI();
      renderDetailTable();
      initOrUpdateMap();
    }

    function setFilterStatus(status) {
      currentFilterStatus = status;
      currentPage = 1;
      ['All', 'Defisit', 'Siaga', 'Normal', 'Unfilled'].forEach(k => {
        const btn = document.getElementById('btnFilter' + k);
        if (btn) btn.classList.toggle('active', k.toLowerCase() === status || (k === 'All' && status === 'all'));
      });
      updateFilterBarUI();
      renderDetailTable();
      initOrUpdateMap();
    }

    function setFilterJenis(jenis) {
      currentFilterJenis = jenis;
      currentPage = 1;
      ['All', 'Interkoneksi', 'Isolated', 'Uld'].forEach(k => {
        const btn = document.getElementById('btnPillJenis' + k);
        if (btn) btn.classList.toggle('active', k.toLowerCase() === jenis || (k === 'All' && jenis === 'all'));
      });
      updateFilterBarUI();
      renderDetailTable();
      initOrUpdateMap();
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

      if (currentFilterStatus !== 'all') {
        chips.push({
          label: `Status: ${currentFilterStatus.toUpperCase()}`,
          remove: () => setFilterStatus('all')
        });
      }
      if (currentFilterJenis !== 'all') {
        chips.push({
          label: `Jenis: ${currentFilterJenis.toUpperCase()}`,
          remove: () => setFilterJenis('all')
        });
      }
      if (currentFilterJam !== 'all') {
        chips.push({
          label: `Jam Nyala: ${currentFilterJam.toUpperCase()}`,
          remove: () => setFilterJam('all')
        });
      }
      if (currentFilterRegion) {
        chips.push({
          label: `Wilayah: ${currentFilterRegion}`,
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

      if (chips.length > 0) {
        bar.classList.add('active');
        container.innerHTML = chips.map((c, i) => `
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
      currentFilterJenis = 'all';
      currentFilterJam = 'all';
      currentFilterRegion = null;
      currentSearchQuery = '';
      currentPage = 1;
      document.getElementById('searchInput').value = '';
      setFilterStatus('all');
      setFilterJenis('all');
      setFilterJam('all');
      showToast("Semua filter telah direset");
    }

    // Map Island Navigation
    function zoomToIsland(islandKey) {
      if (!leafletMap) return;
      document.querySelectorAll('.island-btn').forEach(b => b.classList.remove('active'));
      const activeBtn = document.getElementById('btnMap' + islandKey.charAt(0).toUpperCase() + islandKey.slice(1));
      if (activeBtn) activeBtn.classList.add('active');

      const target = ISLAND_COORDINATES[islandKey] || ISLAND_COORDINATES.all;
      leafletMap.flyTo(target.center, target.zoom, { duration: 1.2 });
    }

    function zoomToDeficitSystems() {
      if (!leafletMap || !appData) return;
      const defs = appData.systems.filter(s => s.status_code === 'defisit');
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
      if (leafletMap && s.geo) {
        leafletMap.flyTo([s.geo.lat, s.geo.lng], 8, { duration: 1.2 });
        const marker = systemMarkersMap[s.no];
        if (marker) {
          setTimeout(() => marker.openPopup(), 1200);
        }
      }
    }

    function openSystemModal(no) {
      if (!appData) return;
      const s = appData.systems.find(item => item.no === no);
      if (!s) return;

      document.getElementById('modalSystemName').innerText = `${s.no}. Sistem ${s.name} (${s.region})`;
      const content = `
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px; background:var(--bg-card-alt); padding:10px 14px; border-radius:8px;">
          <div>
            <div style="font-size:10px; color:var(--text-dim);">STATUS OPERASI</div>
            <div style="margin-top:4px;"><span class="status-badge ${s.status_code}">${s.status}</span></div>
          </div>
          <div style="text-align:right;">
            <div style="font-size:10px; color:var(--text-dim);">CADANGAN DAYA</div>
            <div style="font-size:18px; font-weight:800; color:${s.cad_mw < 0 ? '#EF4444' : '#10B981'};">
              ${s.cad_mw >= 0 ? '+' : ''}${formatNum(s.cad_mw)} MW (${s.cad_pct}%)
            </div>
          </div>
        </div>

        <div style="display:grid; grid-template-columns:repeat(3, 1fr); gap:10px; margin-bottom:14px;">
          <div style="background:var(--bg-card-alt); padding:10px; border-radius:6px;">
            <div style="font-size:10px; color:var(--text-dim);">Jenis Sistem</div>
            <div style="font-size:13px; font-weight:700; color:#A78BFA;">${s.jenis}</div>
          </div>
          <div style="background:var(--bg-card-alt); padding:10px; border-radius:6px;">
            <div style="font-size:10px; color:var(--text-dim);">Pola Jam Operasi</div>
            <div style="font-size:13px; font-weight:700; color:#38BDF8;">${s.jam_operasi}</div>
          </div>
          <div style="background:var(--bg-card-alt); padding:10px; border-radius:6px;">
            <div style="font-size:10px; color:var(--text-dim);">Unit / Wilayah</div>
            <div style="font-size:11px; font-weight:600;">${s.unit}</div>
          </div>
        </div>

        <div style="display:grid; grid-template-columns:repeat(3, 1fr); gap:10px; margin-bottom:14px;">
          <div style="background:var(--bg-card-alt); padding:10px; border-radius:6px;">
            <div style="font-size:10px; color:var(--text-dim);">Daya Terpasang</div>
            <div style="font-size:15px; font-weight:800;">${formatNum(s.daya_terpasang)} MW</div>
          </div>
          <div style="background:var(--bg-card-alt); padding:10px; border-radius:6px;">
            <div style="font-size:10px; color:var(--text-dim);">DMP (Pasok)</div>
            <div style="font-size:15px; font-weight:800; color:#00A3E0;">${formatNum(s.dmp)} MW</div>
          </div>
          <div style="background:var(--bg-card-alt); padding:10px; border-radius:6px;">
            <div style="font-size:10px; color:var(--text-dim);">Beban Puncak (BP)</div>
            <div style="font-size:15px; font-weight:800; color:#FDB913;">${formatNum(s.bp)} MW</div>
          </div>
        </div>

        <div style="background:var(--bg-card-alt); border-radius:8px; padding:12px;">
          <div style="font-weight:700; color:var(--text-main); margin-bottom:4px;">📝 Catatan Operasional & Validasi:</div>
          <div style="white-space:pre-line; font-size:11.5px; color:var(--text-muted);">${s.keterangan}</div>
        </div>
      `;

      document.getElementById('modalSystemContent').innerHTML = content;
      document.getElementById('systemDetailModal').classList.add('active');
    }

    function closeSystemModal() {
      document.getElementById('systemDetailModal').classList.remove('active');
    }

    function openSyncModal() {
      document.getElementById('syncModal').classList.add('active');
    }

    function closeSyncModal() {
      document.getElementById('syncModal').classList.remove('active');
    }

    async function uploadNewExcel(event) {
      const file = event.target.files[0];
      if (!file) return;

      const formData = new FormData();
      formData.append('file', file);

      try {
        const res = await fetch('/api/upload', { method: 'POST', body: formData });
        const result = await res.json();
        if (result.status === 'success') {
          appData = result.data;
          renderDashboard(appData);
          closeSyncModal();
          showToast("File Excel baru 910 sistem berhasil disinkronkan!");
        } else {
          showToast("Gagal unggah: " + result.message, true);
        }
      } catch (err) {
        showToast("Error upload: " + err.message, true);
      }
    }

    // Clean Watermark-Free Map Layer Settings
    let currentMapLayerMode = 'vector';
    let rawGeojsonData = null;

    function getProvinceStyle(isDark, layerMode) {
      if (layerMode === 'vector') {
        return {
          fillColor: isDark ? '#0D233F' : '#CBD5E1',
          fillOpacity: 0.92,
          color: isDark ? '#00A3E0' : '#0284C7',
          weight: 1.2,
          opacity: 0.9
        };
      } else {
        return {
          fillColor: isDark ? '#002E62' : '#CBD5E1',
          fillOpacity: 0.15,
          color: isDark ? '#00A3E0' : '#0284C7',
          weight: 1.0,
          opacity: 0.7
        };
      }
    }

    function setMapBaseLayer(mode) {
      currentMapLayerMode = mode;
      ['Vector', 'Esri', 'Osm'].forEach(m => {
        const btn = document.getElementById('btnLayer' + m);
        if (btn) btn.classList.toggle('active', m.toLowerCase() === mode);
      });

      if (!leafletMap) return;

      if (mapTileLayer) {
        leafletMap.removeLayer(mapTileLayer);
        mapTileLayer = null;
      }

      const isDark = document.documentElement.getAttribute('data-theme') !== 'light';

      if (mode === 'esri') {
        const esriUrl = isDark ? 
          'https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Dark_Gray_Base/MapServer/tile/{z}/{y}/{x}' : 
          'https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer/tile/{z}/{y}/{x}';
        mapTileLayer = L.tileLayer(esriUrl, { maxZoom: 16 }).addTo(leafletMap);
      } else if (mode === 'osm') {
        mapTileLayer = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', { maxZoom: 19 }).addTo(leafletMap);
      }

      if (geojsonLayer) {
        geojsonLayer.setStyle(getProvinceStyle(isDark, mode));
        geojsonLayer.bringToBack();
      }
      if (markersLayerGroup) markersLayerGroup.bringToFront();

      showToast(`Tampilan peta diubah ke: ${mode === 'vector' ? 'Vektor GIS (Bersih/Offline)' : mode.toUpperCase()}`);
    }

    function initOrUpdateMap() {
      if (!leafletMap) {
        leafletMap = L.map('leafletMap', {
          center: [-2.5, 118.0],
          zoom: 5,
          minZoom: 4,
          maxZoom: 10,
          attributionControl: false
        });

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
                    geojsonLayer.resetStyle(e.target);
                    hideGlobalTooltip();
                  }
                });
              }
            }).addTo(leafletMap);

            if (markersLayerGroup) markersLayerGroup.bringToFront();
          })
          .catch(() => {});

        markersLayerGroup = L.layerGroup().addTo(leafletMap);
      }

      if (!appData) return;

      // Filtered markers to display on map
      const systemsToRender = getFilteredList();

      markersLayerGroup.clearLayers();
      systemMarkersMap = {};

      systemsToRender.forEach(s => {
        const lat = s.geo ? s.geo.lat : -2.0;
        const lng = s.geo ? s.geo.lng : 118.0;
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
              <div style="width:11px; height:11px; background:${color}; border:1.5px solid #FFF; border-radius:50%; box-shadow:0 0 6px ${color};"></div>
            `,
            iconSize: [11, 11],
            iconAnchor: [5.5, 5.5]
          });
        }

        const marker = L.marker([lat, lng], { icon });
        systemMarkersMap[s.no] = marker;

        marker.on('mouseover', (e) => {
          showGlobalTooltip(e.originalEvent, generateSystemTooltip(s));
          const row = document.getElementById('row-detail-' + s.no);
          if (row) row.classList.add('highlighted');
        });

        marker.on('mousemove', (e) => {
          positionGlobalTooltip(e.originalEvent);
        });

        marker.on('mouseout', () => {
          hideGlobalTooltip();
          const row = document.getElementById('row-detail-' + s.no);
          if (row) row.classList.remove('highlighted');
        });

        marker.on('click', () => {
          openSystemModal(s.no);
        });

        const popupContent = `
          <div style="font-family:sans-serif; min-width:220px; color:#0F172A; font-size:11.5px;">
            <div style="font-weight:800; font-size:13px; margin-bottom:4px; color:#002E62;">${s.name}</div>
            <div style="margin-bottom:6px; display:flex; gap:4px;">
              <span class="status-badge ${s.status_code}">${s.status}</span>
              <span class="tag-badge ${s.jenis_code === 'isolated' ? 'tag-isolated' : 'tag-interkoneksi'}">${s.jenis}</span>
            </div>
            <div style="font-size:10.5px; color:#64748B; margin-bottom:4px;">${s.unit} • Pola: <strong>${s.jam_operasi}</strong></div>
            <div>• DMP: <strong>${formatNum(s.dmp)} MW</strong></div>
            <div>• Beban Puncak: <strong>${formatNum(s.bp)} MW</strong></div>
            <div style="margin-top:4px; font-weight:700; color:${s.cad_mw < 0 ? '#EF4444' : '#10B981'};">
              Cadangan: ${s.cad_mw >= 0 ? '+' : ''}${formatNum(s.cad_mw)} MW (${s.cad_pct}%)
            </div>
            <div style="margin-top:8px;">
              <button style="background:#002E62; color:#FFF; border:none; padding:4px 8px; border-radius:4px; font-size:10px; cursor:pointer;" onclick="openSystemModal(${s.no})">Buka Detail Lengkap</button>
            </div>
          </div>
        `;

        marker.bindPopup(popupContent);
        markersLayerGroup.addLayer(marker);
      });
    }

    function resetMapZoom() {
      zoomToIsland('all');
    }

    function switchTab(tabId) {
      document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
      document.querySelectorAll('.nav-tab').forEach(el => el.classList.remove('active'));

      const target = document.getElementById('tab-' + tabId);
      if (target) target.classList.add('active');

      const tabs = Array.from(document.querySelectorAll('.nav-tab'));
      const tabKeys = ['overview', 'isolated', 'pembangkit', 'gardu_induk', 'transmisi', 'distribusi', 'detail'];
      const activeIdx = tabKeys.indexOf(tabId);
      if (activeIdx >= 0 && tabs[activeIdx]) tabs[activeIdx].classList.add('active');

      if (tabId === 'overview' && leafletMap) {
        setTimeout(() => leafletMap.invalidateSize(), 150);
      }
    }

    function toggleTheme() {
      const current = document.documentElement.getAttribute('data-theme') || 'dark';
      const next = current === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', next);
      document.getElementById('btnTheme').innerText = next === 'dark' ? '🌙' : '☀️';

      if (leafletMap) {
        setMapBaseLayer(currentMapLayerMode);
      }

      showToast(`Tema diubah ke ${next === 'dark' ? 'Dark Mode' : 'Light Mode'}`);
    }

    function toggleFullscreen() {
      if (!document.fullscreenElement) {
        document.documentElement.requestFullscreen().catch(() => {});
        showToast("Mode Layar Penuh Aktif");
      } else {
        document.exitFullscreen().catch(() => {});
        showToast("Keluar Layar Penuh");
      }
    }

    function changeAutoRefresh(val) {
      if (autoRefreshTimer) clearInterval(autoRefreshTimer);
      if (countdownTicker) clearInterval(countdownTicker);

      autoRefreshSeconds = parseInt(val, 10);
      countdownRemaining = autoRefreshSeconds;

      const label = document.getElementById('countdownLabel');

      if (autoRefreshSeconds > 0) {
        label.innerText = `Auto: ${countdownRemaining}d`;
        countdownTicker = setInterval(() => {
          countdownRemaining--;
          if (countdownRemaining <= 0) {
            countdownRemaining = autoRefreshSeconds;
            loadData(true);
          }
          label.innerText = `Auto: ${countdownRemaining}d`;
        }, 1000);
      } else {
        label.innerText = `Auto: Nonaktif`;
      }
    }

    function exportCSV() {
      window.location.href = '/api/export/csv';
    }

    function exportJSON() {
      if (!appData) return;
      const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(appData, null, 2));
      const downloadAnchor = document.createElement('a');
      downloadAnchor.setAttribute("href", dataStr);
      downloadAnchor.setAttribute("download", "PLN_Monitoring_910_Sistem_Nasional.json");
      document.body.appendChild(downloadAnchor);
      downloadAnchor.click();
      downloadAnchor.remove();
      showToast("Data JSON 910 sistem berhasil diekspor!");
    }

    // Chatbot AI
    function toggleChatbot() {
      const drawer = document.getElementById('chatbotDrawer');
      isChatOpen = !isChatOpen;

      if (isChatOpen) {
        drawer.classList.add('open');
        setTimeout(() => {
          const input = document.getElementById('chatInput');
          if (input) input.focus();
        }, 150);
      } else {
        drawer.classList.remove('open');
      }
    }

    function clearChatHistory() {
      const body = document.getElementById('chatbotBody');
      const typing = document.getElementById('chatTyping');
      body.innerHTML = `
        <div class="chat-bubble bot">
          <div style="font-weight:700; color:var(--pln-cyan); margin-bottom:4px;">✨ Percakapan telah dibersihkan.</div>
          <div>Silakan tanyakan informasi teknis atau non-teknis mengenai 910 Sistem Kelistrikan PLN.</div>
          <div class="chat-meta">⚡ Asisten AI PLN • Sekarang</div>
        </div>
      `;
      body.appendChild(typing);
      showToast("Riwayat chat dibersihkan.");
    }

    function askQuickPrompt(text) {
      if (!isChatOpen) toggleChatbot();
      const input = document.getElementById('chatInput');
      input.value = text;
      sendChatMessage();
    }

    function formatChatMarkdown(text) {
      if (!text) return '';
      let safe = text
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;");

      safe = safe.replace(/^### (.*$)/gim, '<div style="font-weight:700; color:var(--pln-cyan); margin:6px 0 3px; font-size:12.5px;">$1</div>');
      safe = safe.replace(/^## (.*$)/gim, '<div style="font-weight:700; color:var(--pln-cyan); margin:8px 0 4px; font-size:13px;">$1</div>');
      safe = safe.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
      safe = safe.replace(/\*(.*?)\*/g, '<em>$1</em>');
      safe = safe.replace(/`(.*?)`/g, '<code>$1</code>');
      safe = safe.replace(/^> (.*$)/gim, '<blockquote>$1</blockquote>');
      safe = safe.replace(/^\s*-\s+(.*$)/gim, '<div style="margin-left:14px; margin-bottom:3px;">• $1</div>');
      safe = safe.replace(/\n/g, '<br>');

      return safe;
    }

    async function sendChatMessage() {
      const input = document.getElementById('chatInput');
      const text = input.value.trim();
      if (!text) return;

      input.value = '';
      const body = document.getElementById('chatbotBody');
      const typing = document.getElementById('chatTyping');

      const now = new Date();
      const timeStr = `${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')} WIB`;
      
      const userBubble = document.createElement('div');
      userBubble.className = 'chat-bubble user';
      userBubble.innerHTML = `
        <div>${text.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')}</div>
        <div class="chat-meta">Anda • ${timeStr}</div>
      `;
      body.insertBefore(userBubble, typing);

      typing.style.display = 'flex';
      body.scrollTop = body.scrollHeight;

      try {
        const response = await fetch('/api/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ message: text })
        });

        const data = await response.json();
        typing.style.display = 'none';

        const botReply = (data && data.reply) ? data.reply : 'Maaf, terjadi kendala saat memproses respons chatbot.';
        const botBubble = document.createElement('div');
        botBubble.className = 'chat-bubble bot';
        botBubble.innerHTML = `
          <div>${formatChatMarkdown(botReply)}</div>
          <div class="chat-meta">⚡ Asisten AI PLN • ${data.timestamp_wib || timeStr}</div>
        `;
        body.insertBefore(botBubble, typing);
      } catch (err) {
        typing.style.display = 'none';
        const errBubble = document.createElement('div');
        errBubble.className = 'chat-bubble bot';
        errBubble.innerHTML = `
          <div style="color:#EF4444;">⚠️ Gagal terhubung ke chatbot API: ${err.message}</div>
          <div class="chat-meta">⚡ Error • ${timeStr}</div>
        `;
        body.insertBefore(errBubble, typing);
      }

      body.scrollTop = body.scrollHeight;
    }

    // App Startup
    window.addEventListener('DOMContentLoaded', () => {
      loadData(false);
      checkServerStatus();
      changeAutoRefresh(30);
    });
  </script>
</body>
</html>
'''

output_path = os.path.join(os.path.dirname(__file__), 'public', 'index.html')
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(HTML_CONTENT)
print("Updated public/index.html successfully!")
