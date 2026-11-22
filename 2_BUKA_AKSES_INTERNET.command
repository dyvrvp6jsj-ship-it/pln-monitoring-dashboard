#!/bin/bash
# ==============================================================================
# SCRIPT 2: BUKA AKSES INTERNET PUBLIK (Cloudflare Ultra Fast Tunnel)
# Cukup klik 2x (double-click) file ini di macOS Finder
# ==============================================================================
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

echo "=================================================================="
echo "🌐 MEMBUKA JALUR AKSES INTERNET PUBLIK (CLOUDFLARE TUNNEL)"
echo "   Server Regional: Jakarta & Singapura (Ultra Fast, Anti-Lag)"
echo "=================================================================="
echo ""
echo "Sedang menghubungkan ke Cloudflare Edge Network..."
echo "Tautan (Link) publik HTTPS akan segera muncul di dalam kotak di bawah."
echo "Salin link tersebut untuk dibuka di HP atau dibagikan ke rekan kerja/atasan."
echo ""
echo "Tekan [Ctrl + C] untuk menghentikan akses internet."
echo "=================================================================="
echo ""

if [ -f "$DIR/bin/cloudflared" ]; then
    "$DIR/bin/cloudflared" tunnel --protocol http2 --url http://localhost:8080
else
    echo "❌ Binary cloudflared tidak ditemukan di folder bin/."
    read -p "Tekan [Enter] untuk keluar..."
fi
