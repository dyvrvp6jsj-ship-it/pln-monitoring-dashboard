#!/bin/bash
# ==============================================================================
# SCRIPT 3: PUSH REPOSITORI KE GITHUB
# Cukup klik 2x (double-click) file ini di macOS Finder
# ==============================================================================
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

echo "=================================================================="
echo "⚡ PUSH REPOSITORI DASHBOARD PLN KE GITHUB"
echo "=================================================================="
echo "Direktori Kerja: $DIR"
echo "Target Remote:   https://github.com/dyvrvp6jsj-ship-it/pln-monitoring-dashboard.git"
echo "Target Branch:   main"
echo "=================================================================="
echo ""
echo "Catatan Penting Autentikasi GitHub:"
echo "1. Masukkan Username: dyvrvp6jsj-ship-it"
echo "2. Masukkan Password: Gunakan GitHub Personal Access Token (PAT)"
echo "   (Token diawali 'ghp_...'. Teks tidak akan terlihat saat diketik/paste)"
echo ""
echo "Sedang melakukan git push..."
echo ""

git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "=================================================================="
    echo "✅ BERHASIL! Seluruh berkas telah ter-upload ke repositori GitHub:"
    echo "   https://github.com/dyvrvp6jsj-ship-it/pln-monitoring-dashboard"
    echo "=================================================================="
else
    echo ""
    echo "=================================================================="
    echo "❌ Push gagal atau dibatalkan."
    echo "Tips jika autentikasi ditolak:"
    echo "Buat token di: https://github.com/settings/tokens"
    echo "Pilih 'Generate new token (classic)' dan centang izin 'repo'."
    echo "=================================================================="
fi

echo ""
read -p "Tekan [Enter] untuk menutup jendela ini..."
