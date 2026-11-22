#!/bin/bash
# ==============================================================================
# SCRIPT PELUNCUR OTOMATIS: DASHBOARD REALTIME MONITORING PLN
# Cukup klik 2x (double-click) file ini di macOS Finder untuk menjalankan aplikasi
# ==============================================================================

# Pindah ke direktori tempat script ini berada
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

echo "=================================================================="
echo "⚡ MEMULAI DASHBOARD REALTIME MONITORING 910 SISTEM KELISTRIKAN PLN"
echo "   (Konsolidasi Sistem Interkoneksi, Isolated 24j/12j/6j, & ULD)"
echo "=================================================================="
echo "Direktori Kerja: $DIR"
echo ""

# Periksa instalasi Python 3
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 tidak ditemukan. Pastikan Python 3 sudah terinstal."
    read -p "Tekan [Enter] untuk keluar..."
    exit 1
fi

# Buka browser otomatis ke localhost setelah 1.2 detik di background
(
    sleep 1.2
    if command -v open &> /dev/null; then
        open "http://localhost:8080"
    fi
) &

# Jalankan backend server
python3 server.py
