with open('public/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace mobile header CSS rules
old_mobile_header_css = """      /* Header Mobile Compact */
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
      }"""

new_mobile_header_css = """      /* Header Mobile Clean & Compact (Anti-Collision) */
      header {
        padding: 8px 12px !important;
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        justify-content: space-between !important;
        align-items: center !important;
        gap: 10px !important;
        height: 52px !important;
        box-sizing: border-box !important;
      }

      .brand-section {
        display: flex !important;
        align-items: center !important;
        gap: 8px !important;
        min-width: 0 !important;
        flex: 1 !important;
        overflow: hidden !important;
      }

      .pln-logo-box {
        width: 26px !important;
        height: 32px !important;
        flex-shrink: 0 !important;
      }

      .brand-text {
        min-width: 0 !important;
        flex: 1 !important;
        overflow: hidden !important;
      }

      .brand-text h1 {
        font-size: 12.5px !important;
        font-weight: 800 !important;
        white-space: nowrap !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
        margin: 0 !important;
        color: var(--pln-blue) !important;
      }

      [data-theme="dark"] .brand-text h1 {
        color: var(--pln-cyan) !important;
      }

      .brand-text p, .badge-total, .print-opt-label {
        display: none !important;
      }

      /* In Header Controls on Mobile, strictly show only the hamburger button */
      .header-controls {
        display: flex !important;
        align-items: center !important;
        flex-shrink: 0 !important;
      }

      .header-controls > *:not(.mobile-hamburger-btn) {
        display: none !important;
      }

      .mobile-hamburger-btn {
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        background: #002E62 !important;
        color: #FFFFFF !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 6px !important;
        padding: 6px 12px !important;
        font-size: 16px !important;
        cursor: pointer !important;
        box-shadow: 0 1px 4px rgba(0,0,0,0.1) !important;
      }"""

if old_mobile_header_css in html:
    html = html.replace(old_mobile_header_css, new_mobile_header_css)
    print("Replaced mobile header CSS successfully")
else:
    print("old_mobile_header_css not found")

with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Finished fix_mobile_header.py")
