import http.server
import socketserver
import os
import urllib.parse
import json
import subprocess

PORT = 8000
WEB_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = "/Users/markoates/Assets"

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Force the browser to NEVER cache local development files
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

    def translate_path(self, path):
        parsed_path = urllib.parse.unquote(urllib.parse.urlparse(path).path)
        if parsed_path.startswith("/Assets/"):
            return os.path.join(ASSETS_DIR, parsed_path[len("/Assets/"):])
        return os.path.join(WEB_DIR, parsed_path.lstrip('/'))

    def do_POST(self):
        parsed_url = urllib.parse.urlparse(self.path)
        
        if parsed_url.path == "/api/open-finder":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)
            target = data.get('target', '')
            
            if target.startswith('/Assets/'):
                target = os.path.join(ASSETS_DIR, target[len('/Assets/'):])
            elif target and not target.startswith('/'):
                target = os.path.join(ASSETS_DIR, target)
                
            if os.path.exists(target):
                subprocess.Popen(['open', '-R', target])
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "ok"}).encode('utf-8'))
            else:
                self.send_response(404)
                self.end_headers()
            return
            
        elif parsed_url.path == "/api/sync":
            try:
                pipeline_script = os.path.join(os.path.dirname(WEB_DIR), "scripts", "rebuild_ui_data.sh")
                subprocess.run([pipeline_script], check=True)
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "ok"}).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
            return
            
        elif parsed_url.path == "/api/flag":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)
            
            identifier = data.get('identifier')
            flag_type = data.get('flag_type') # 'favorite', 'error', 'none'
            
            flags_path = os.path.join(WEB_DIR, 'flags.json')
            flags = {}
            if os.path.exists(flags_path):
                with open(flags_path, 'r', encoding='utf-8') as f:
                    try: flags = json.load(f)
                    except: pass
            
            if flag_type == 'none':
                if identifier in flags:
                    del flags[identifier]
            else:
                flags[identifier] = flag_type
                
            with open(flags_path, 'w', encoding='utf-8') as f:
                json.dump(flags, f)
                
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ok"}).encode('utf-8'))
            return
            
        elif parsed_url.path == "/api/note":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)
            
            identifier = data.get('identifier')
            note = data.get('note', '')
            
            notes_path = os.path.join(WEB_DIR, 'notes.json')
            notes = {}
            if os.path.exists(notes_path):
                with open(notes_path, 'r', encoding='utf-8') as f:
                    try: notes = json.load(f)
                    except: pass
            
            if note:
                notes[identifier] = note
            else:
                if identifier in notes:
                    del notes[identifier]
                
            with open(notes_path, 'w', encoding='utf-8') as f:
                json.dump(notes, f)
                
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ok"}).encode('utf-8'))
            return

        self.send_response(404)
        self.end_headers()

socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
    print(f"Serving UI at http://localhost:{PORT}")
    print(f"Serving /Assets/ endpoint directly from {ASSETS_DIR}")
    print("Caching is DISABLED for local development.")
    httpd.serve_forever()
