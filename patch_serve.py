content = open('web/serve.py').read()
new_endpoint = """
        elif parsed_url.path == "/api/note":
            import json
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
"""
# Insert after /api/flag logic
flag_end = "self.wfile.write(json.dumps({\"status\": \"ok\"}).encode('utf-8'))\n"
parts = content.split(flag_end)
if len(parts) >= 2:
    parts[0] += flag_end + new_endpoint
    with open('web/serve.py', 'w') as f:
        f.write("".join(parts))
    print("Patched serve.py")
else:
    print("Could not find insertion point")
