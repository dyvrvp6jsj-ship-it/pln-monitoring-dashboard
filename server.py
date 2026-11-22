"""
PLN Realtime Monitoring Backend Server (server.py)
Menyajikan REST API, modul static Leaflet GIS, endpoint Chatbot AI, dan auto-sinkronisasi data.
Bound to 0.0.0.0:8080 untuk Open Akses Jaringan Lokal (LAN / Wi-Fi).
"""

import http.server
import socketserver
import json
import os
import io
import csv
import gzip
import subprocess
from urllib.parse import urlparse, parse_qs
from datetime import datetime
from parser import parse_excel_monitoring, WIB

PORT = 8080
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, 'data', 'sumber_data_pln.xlsx')
HTML_FILE = os.path.join(BASE_DIR, 'public', 'index.html')
SHAREPOINT_URL = "https://ptpln365-my.sharepoint.com/:x:/g/personal/mohammad_anang_ptpln365_onmicrosoft_com/IQAP_S2PC7-nTYf6tBRkQH84AVwSj7Q2cMy0F3SeSkPgDho?download=1"

cached_data = None
last_parsed_time = None

_cached_lan_ip = None

def sync_from_sharepoint():
    """Mengunduh pembaruan file Excel terbaru langsung dari cloud SharePoint PT PLN."""
    try:
        cmd = f'curl -s -L -c /tmp/sp_c.txt -b /tmp/sp_c.txt "{SHAREPOINT_URL}" -o /tmp/sp_temp.xlsx'
        subprocess.run(cmd, shell=True, timeout=14)
        if os.path.exists('/tmp/sp_temp.xlsx') and os.path.getsize('/tmp/sp_temp.xlsx') > 50000:
            import shutil
            shutil.copyfile('/tmp/sp_temp.xlsx', DATA_FILE)
            return True, "Berhasil mengunduh pembaruan data langsung dari SharePoint PT PLN 365"
    except Exception:
        pass
    return False, "Data dimuat ulang dari penyimpanan lokal"

def get_lan_ip():
    """Mendeteksi IP LAN aktif secara dinamis, cepat dan non-blocking."""
    global _cached_lan_ip
    if _cached_lan_ip:
        return _cached_lan_ip
    try:
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0.3)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        if ip and not ip.startswith("127."):
            _cached_lan_ip = ip
            return _cached_lan_ip
    except Exception:
        pass
    try:
        out = subprocess.check_output(
            "ifconfig | awk '/inet / && !/127.0.0.1/ {print $2}'",
            shell=True,
            timeout=0.5,
            stderr=subprocess.DEVNULL,
        ).decode().strip()
        if out:
            for ip in out.split():
                if not ip.startswith("127."):
                    _cached_lan_ip = ip
                    return _cached_lan_ip
    except Exception:
        pass
    _cached_lan_ip = "127.0.0.1"
    return _cached_lan_ip

def get_data(force_reload=False):
    global cached_data, last_parsed_time
    if force_reload or cached_data is None:
        cached_data = parse_excel_monitoring(DATA_FILE)
        last_parsed_time = datetime.now(WIB)
    return cached_data

class ThreadingServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    daemon_threads = True
    allow_reuse_address = True

class DashboardHandler(http.server.BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def handle(self):
        try:
            super().handle()
        except (ConnectionResetError, BrokenPipeError):
            pass

    def _send_bytes(self, content_bytes, content_type='text/html; charset=utf-8', status_code=200, extra_headers=None):
        try:
            accept_encoding = self.headers.get('Accept-Encoding', '') if self.headers else ''
            if 'gzip' in accept_encoding and len(content_bytes) > 256:
                compressed = gzip.compress(content_bytes, compresslevel=5)
                self.send_response(status_code)
                self.send_header('Content-Type', content_type)
                self.send_header('Content-Encoding', 'gzip')
                self.send_header('Content-Length', str(len(compressed)))
                if extra_headers:
                    for k, v in extra_headers.items():
                        self.send_header(k, v)
                self.end_headers()
                self.wfile.write(compressed)
            else:
                self.send_response(status_code)
                self.send_header('Content-Type', content_type)
                self.send_header('Content-Length', str(len(content_bytes)))
                if extra_headers:
                    for k, v in extra_headers.items():
                        self.send_header(k, v)
                self.end_headers()
                self.wfile.write(content_bytes)
        except (ConnectionResetError, BrokenPipeError):
            pass

    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path in ['/', '/index.html']:
            if os.path.exists(HTML_FILE):
                with open(HTML_FILE, 'rb') as f:
                    content = f.read()
                self._send_bytes(content, 'text/html; charset=utf-8')
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"Frontend not found")
        
        elif 'apple-touch-icon' in path or path == '/favicon.ico':
            fav_path = os.path.join(BASE_DIR, 'public', 'logo_pln.png')
            if os.path.exists(fav_path):
                with open(fav_path, 'rb') as f:
                    content = f.read()
                self._send_bytes(content, 'image/png')
            else:
                self.send_response(204)
                self.end_headers()
            return
        
        elif path.startswith('/leaflet/') or path.startswith('/public/') or path.endswith(('.html', '.geojson', '.js', '.css', '.png', '.jpg', '.jpeg', '.svg', '.ico', '.webp')):
            rel_path = path.lstrip('/')
            file_path = os.path.join(BASE_DIR, 'public', rel_path.replace('public/', ''))
            if os.path.exists(file_path) and os.path.isfile(file_path):
                import mimetypes
                mime_type, _ = mimetypes.guess_type(file_path)
                if file_path.endswith('.html'):
                    mime_type = 'text/html; charset=utf-8'
                elif file_path.endswith('.geojson'):
                    mime_type = 'application/json'
                elif file_path.endswith('.js'):
                    mime_type = 'application/javascript'
                elif file_path.endswith('.css'):
                    mime_type = 'text/css'
                elif file_path.endswith('.png'):
                    mime_type = 'image/png'
                elif file_path.endswith(('.jpg', '.jpeg')):
                    mime_type = 'image/jpeg'
                elif file_path.endswith('.svg'):
                    mime_type = 'image/svg+xml'
                elif file_path.endswith('.ico'):
                    mime_type = 'image/x-icon'
                
                with open(file_path, 'rb') as f:
                    content = f.read()
                self._send_bytes(content, mime_type or 'application/octet-stream')
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"Static file not found")

        elif path == '/report_preview.html':
            try:
                preview_path = os.path.join(BASE_DIR, 'public', 'report_preview.html')
                with open(preview_path, 'rb') as f:
                    content = f.read()
                self._send_bytes(content, 'text/html; charset=utf-8')
            except Exception as e:
                self.send_error_json(str(e))

        elif path == '/api/data':
            try:
                data = get_data(force_reload=False)
                payload = json.dumps(data).encode('utf-8')
                self._send_bytes(payload, 'application/json; charset=utf-8')
            except Exception as e:
                self.send_error_json(str(e))

        elif path == '/api/status':
            lan_ip = get_lan_ip()
            st = {
                "status": "online",
                "lan_ip": lan_ip,
                "port": PORT,
                "local_url": f"http://localhost:{PORT}",
                "network_url": f"http://{lan_ip}:{PORT}",
                "last_parsed": last_parsed_time.strftime("%d %B %Y, %H:%M:%S WIB") if last_parsed_time else "Belum sinkron"
            }
            payload = json.dumps(st).encode('utf-8')
            self._send_bytes(payload, 'application/json; charset=utf-8')

        elif path == '/api/export/csv':
            try:
                data = get_data(force_reload=False)
                output = io.StringIO()
                writer = csv.writer(output)
                writer.writerow([
                    'No', 'ID', 'Sistem', 'Unit/Wilayah', 'Regional', 'Jenis Sistem', 'Jam Operasi',
                    'Daya Terpasang (MW)', 'Unit Terbesar (MW)', 'DMN (MW)', 'DMP (MW)', 'BPM (MW)', 
                    'Cadangan (MW)', 'Cadangan (%)', 'Status Neraca Daya', 'Keterangan Validasi'
                ])
                for s in data['systems']:
                    writer.writerow([
                        s['no'], s['id'], s['name'], s['unit'], s['region'], s['jenis'], s['jam_operasi'],
                        s.get('daya_terpasang', 0), s.get('unit_terbesar', 0), s['dmn'], s['dmp'], s['bp'],
                        s['cad_mw'], s['cad_pct'], s['status'], s['keterangan'].replace('\n', ' ')
                    ])
                
                payload = output.getvalue().encode('utf-8-sig')
                self._send_bytes(payload, 'text/csv; charset=utf-8', extra_headers={'Content-Disposition': 'attachment; filename="PLN_Monitoring_910_Sistem_Nasional.csv"'})
            except Exception as e:
                self.send_error_json(str(e))

        elif path == '/api/config/sistem-besar':
            try:
                cfg_file = os.path.join(BASE_DIR, 'config', 'sistem_besar.json')
                curr = {}
                if os.path.exists(cfg_file):
                    with open(cfg_file, 'r', encoding='utf-8') as f:
                        curr = json.load(f)
                resp = json.dumps({
                    "status": "success",
                    "config": curr
                }).encode('utf-8')
                self._send_bytes(resp, 'application/json; charset=utf-8')
            except Exception as e:
                self.send_error_json(str(e))

        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == '/api/refresh':
            try:
                synced, sync_msg = sync_from_sharepoint()
                data = get_data(force_reload=True)
                payload = json.dumps({
                    "status": "success",
                    "message": sync_msg,
                    "synced_from_sharepoint": synced,
                    "data": data
                }).encode('utf-8')
                self._send_bytes(payload, 'application/json; charset=utf-8')
            except Exception as e:
                self.send_error_json(str(e))

        elif path == '/api/chat':
            try:
                content_length = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(content_length).decode('utf-8')
                req_json = json.loads(body) if body else {}
                user_msg = req_json.get('message', '')
                
                import importlib
                import chatbot
                importlib.reload(chatbot)
                data = get_data(force_reload=False)
                answer = chatbot.process_chat_query(user_msg, data)
                
                resp = json.dumps({
                    "status": "success",
                    "reply": answer,
                    "timestamp_wib": datetime.now(WIB).strftime("%H:%M:%S WIB")
                }).encode('utf-8')
                self._send_bytes(resp, 'application/json; charset=utf-8')
            except Exception as e:
                self.send_error_json(str(e))

        elif path == '/api/upload':
            try:
                content_length = int(self.headers.get('Content-Length', 0))
                file_bytes = self.rfile.read(content_length)
                
                if self.headers.get('Content-Type', '').startswith('multipart/form-data'):
                    boundary = self.headers.get('Content-Type').split('boundary=')[1].encode()
                    parts = file_bytes.split(b'--' + boundary)
                    for part in parts:
                        if b'filename="' in part:
                            head, body = part.split(b'\r\n\r\n', 1)
                            file_data = body.rsplit(b'\r\n', 1)[0]
                            with open(DATA_FILE, 'wb') as f:
                                f.write(file_data)
                            break
                else:
                    with open(DATA_FILE, 'wb') as f:
                        f.write(file_bytes)

                data = get_data(force_reload=True)
                res = json.dumps({
                    "status": "success",
                    "message": "File Excel baru berhasil diunggah dan disinkronkan!",
                    "data": data
                }).encode('utf-8')
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Content-Length', str(len(res)))
                self.end_headers()
                self.wfile.write(res)
            except Exception as e:
                self.send_error_json(str(e))

        elif path == '/api/config/sistem-besar':
            try:
                content_length = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(content_length).decode('utf-8')
                req_json = json.loads(body) if body else {}
                new_ids = req_json.get('sistem_besar_ids', [])
                
                cfg_file = os.path.join(BASE_DIR, 'config', 'sistem_besar.json')
                curr = {}
                if os.path.exists(cfg_file):
                    with open(cfg_file, 'r', encoding='utf-8') as f:
                        curr = json.load(f)
                curr['sistem_besar_ids'] = new_ids
                curr['status'] = 'configured' if len(new_ids) == 24 else ('partial' if len(new_ids) > 0 else 'unconfigured')
                curr['status_message'] = '24 sistem besar resmi terkonfigurasi' if len(new_ids) == 24 else f'{len(new_ids)} sistem besar terkonfigurasi'
                with open(cfg_file, 'w', encoding='utf-8') as f:
                    json.dump(curr, f, indent=2)
                
                data = get_data(force_reload=True)
                resp = json.dumps({
                    "status": "success",
                    "message": "Konfigurasi sistem besar diperbarui",
                    "config": curr,
                    "data": data
                }).encode('utf-8')
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Content-Length', str(len(resp)))
                self.end_headers()
                self.wfile.write(resp)
            except Exception as e:
                self.send_error_json(str(e))

        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")

    def send_error_json(self, message):
        payload = json.dumps({"status": "error", "message": message}).encode('utf-8')
        self.send_response(500)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

def run():
    # Preload data
    get_data(force_reload=True)
    lan_ip = get_lan_ip()

    with ThreadingServer(("0.0.0.0", PORT), DashboardHandler) as httpd:
        print("=" * 64)
        print("PLN REALTIME MONITORING DASHBOARD IS READY & OPEN FOR ACCESS:")
        print(f"  • Localhost: http://localhost:{PORT}")
        print(f"  • Open Network (LAN/Wi-Fi): http://{lan_ip}:{PORT}")
        print("=" * 64)
        httpd.serve_forever()

if __name__ == '__main__':
    run()
