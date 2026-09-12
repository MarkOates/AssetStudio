import http.server
import socketserver
import os
import urllib.parse

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
        # Parse and UNQUOTE the URL path (vital for spaces in folder names)
        parsed_path = urllib.parse.unquote(urllib.parse.urlparse(path).path)
        
        # If the path starts with /Assets/, route it to the actual Assets directory on disk
        if parsed_path.startswith("/Assets/"):
            return os.path.join(ASSETS_DIR, parsed_path[len("/Assets/"):])
            
        # Otherwise, serve from the current web/ directory
        return os.path.join(WEB_DIR, parsed_path.lstrip('/'))

    def do_POST(self):
        parsed_url = urllib.parse.urlparse(self.path)
        if parsed_url.path == "/api/open-finder":
            import json
            import subprocess
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)
            target = data.get('target', '')
            
            # Map /Assets/ URL to physical path
            if target.startswith('/Assets/'):
                target = os.path.join(ASSETS_DIR, target[len('/Assets/'):])
            elif target and not target.startswith('/'):
                # Handle relative pack IDs (e.g. "provider/pack")
                target = os.path.join(ASSETS_DIR, target)
                
            if os.path.exists(target):
                # Use macOS 'open -R' to reveal the file/folder in Finder
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
            import subprocess
            import json
            try:
                # Delegate the multi-step CI pipeline to a dedicated shell script
                pipeline_script = os.path.join(os.path.dirname(WEB_DIR), "scripts", "rebuild_viewer.sh")
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

        self.send_response(404)
        self.end_headers()

socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
    print(f"Serving UI at http://localhost:{PORT}")
    print(f"Serving /Assets/ endpoint directly from {ASSETS_DIR}")
    print("Caching is DISABLED for local development.")
    httpd.serve_forever()
