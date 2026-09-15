import re
import subprocess
import sys

html = open('web/pack.html').read()
scripts = re.findall(r'<script>(.*?)</script>', html, re.DOTALL)
for i, script in enumerate(scripts):
    with open(f'tmp_script_{i}.js', 'w') as f:
        f.write(script)
    res = subprocess.run(['node', '-c', f'tmp_script_{i}.js'], capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Error in script {i}: {res.stderr}")
        sys.exit(1)
print("All good!")
