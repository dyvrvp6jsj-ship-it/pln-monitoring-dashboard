#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"
echo "Menjalankan PLN Realtime Monitoring Dashboard..."
(sleep 1.2 && open "http://localhost:8080" 2>/dev/null) &
python3 server.py
