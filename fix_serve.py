content = open('web/serve.py').read()
# Find the exact string we want to replace
target = """            if flag_type == 'none':
                if identifier in flags:
                    del flags[identifier]
            else:
                flags[identifier] = flag_type
                
            with open(flags_path, 'w', encoding='utf-8') as f:
                json.dump(flags, f)
                
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ok"}).encode('utf-8'))"""

replacement = target + """
            
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

# I need to restore the original file first, since my split messed it up.
# I'll just remove the bad note endpoint.
import re
# The bad endpoint was inserted inside /api/sync
# Let's just find the first occurrence of `/api/note` and remove it down to `encode('utf-8'))\n`
bad_match = re.search(r'elif parsed_url\.path == "/api/note":.*?self\.wfile\.write\(json\.dumps\(\{"status": "ok"\}\)\.encode\(\'utf-8\'\)\)\n', content, re.DOTALL)
if bad_match:
    content = content.replace(bad_match.group(0), '')

# Wait, `"".join(parts)` removed ALL occurrences of `flag_end` !!!
# That means `/api/sync` and `/api/flag` both lost their `self.wfile.write(...)`!
# Let me reconstruct it.
