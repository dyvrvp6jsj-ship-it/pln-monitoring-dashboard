#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

echo "=================================================================="
echo "⚡ MEMULAI DASHBOARD REALTIME MONITORING 910 SISTEM KELISTRIKAN PLN"
echo "=================================================================="
echo "Direktori Kerja: $DIR"
echo ""

# Bersihkan sisa proses lama di port 8080 agar tidak bentrok
OLD_PID=$(lsof -t -i :8080 2>/dev/null)
if [ -n "$OLD_PID" ]; then
    echo "Membersihkan proses lama di port 8080 (PID: $OLD_PID)..."
    kill -9 $OLD_PID 2>/dev/null
    sleep 0.5
fi

echo "Membuka browser otomatis ke http://localhost:8080 ..."
echo ""

(
    sleep 1.2
    if command -v open &> /dev/null; then
        open "http://localhost:8080"
    fi
) &

python3 server.py

EXIT_CODE=$?
if [ $EXIT_CODE -ne 0 ]; then
    echo ""
    echo "=================================================================="
    echo "❌ Server berhenti dengan kode error: $EXIT_CODE"
    echo "=================================================================="
    echo ""
    read -p "Tekan [Enter] untuk menutup jendela ini..."
fi
