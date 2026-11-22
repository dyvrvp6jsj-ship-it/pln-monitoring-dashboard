#!/bin/bash
# ==============================================================================
# SCRIPT 1: JALANKAN DASHBOARD MONITORING PLN (Localhost & Wi-Fi)
# Cukup klik 2x (double-click) file ini di macOS Finder
# ==============================================================================
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

echo "=================================================================="
echo "⚡ MEMULAI DASHBOARD REALTIME MONITORING 910 SISTEM KELISTRIKAN PLN"
echo "=================================================================="
echo "Direktori Kerja: $DIR"
echo "Membuka browser otomatis ke http://localhost:8080 ..."
echo ""

# Buka browser otomatis setelah 1 detik di latar belakang
(
    sleep 1.2
    if command -v open &> /dev/null; then
        open "http://localhost:8080"
    fi
) &

# Jalankan backend server Python
python3 server.py
