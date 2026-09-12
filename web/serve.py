import http.server
import socketserver
import os
import urllib.parse

PORT = 8000
WEB_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = "/Users/markoates/Assets"

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        # Parse and UNQUOTE the URL path (vital for spaces in folder names like "Explosions Pack 8")
        parsed_path = urllib.parse.unquote(urllib.parse.urlparse(path).path)
        
        # If the path starts with /Assets/, route it to the actual Assets directory on disk
        if parsed_path.startswith("/Assets/"):
            return os.path.join(ASSETS_DIR, parsed_path[len("/Assets/"):])
            
        # Otherwise, serve from the current web/ directory
        return os.path.join(WEB_DIR, parsed_path.lstrip('/'))

with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
    print(f"Serving UI at http://localhost:{PORT}")
    print(f"Serving /Assets/ endpoint directly from {ASSETS_DIR}")
    httpd.serve_forever()
