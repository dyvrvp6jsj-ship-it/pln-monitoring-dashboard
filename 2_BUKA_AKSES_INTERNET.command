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

# Pastikan server lokal 8080 sedang aktif
if ! lsof -i :8080 >/dev/null 2>&1; then
    echo "⚠️  Server dashboard di port 8080 belum menyala!"
    echo "   Menyalakan server dashboard di latar belakang terlebih dahulu..."
    python3 server.py &
    sleep 2
fi

CF_BIN=""
if [ -x "$DIR/bin/cloudflared" ]; then
    CF_BIN="$DIR/bin/cloudflared"
elif command -v cloudflared >/dev/null 2>&1; then
    CF_BIN="$(command -v cloudflared)"
fi

if [ -z "$CF_BIN" ]; then
    echo "❌ Binary cloudflared belum ditemukan di bin/."
    echo "   Mengunduh binary cloudflared resmi untuk macOS..."
    mkdir -p "$DIR/bin"
    curl -L --progress-bar "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-darwin-amd64.tgz" -o /tmp/cf.tgz
    tar -xzf /tmp/cf.tgz -C "$DIR/bin/"
    chmod +x "$DIR/bin/cloudflared"
    CF_BIN="$DIR/bin/cloudflared"
    rm -f /tmp/cf.tgz
fi

echo "Sedang menghubungkan ke Cloudflare Edge Network (Data Center Jakarta)..."
echo "Tautan (Link) publik HTTPS yang berakhiran '.trycloudflare.com' akan muncul di bawah."
echo "Salin link tersebut untuk dibuka di HP luar rumah atau dibagikan ke WhatsApp."
echo ""
echo "Tekan [Ctrl + C] pada keyboard jika ingin menghentikan akses internet."
echo "=================================================================="
echo ""

"$CF_BIN" tunnel --protocol http2 --edge-ip-version 4 --url http://localhost:8080
