import json
import time
import subprocess
import concurrent.futures

def main():
    with open('web/packs.json', 'r') as f:
        packs = json.load(f)

    targets = []
    for pid, pdata in packs.items():
        if pdata.get('can_be_extracted_by_automation') is True and not pdata.get('extracted_at'):
            targets.append(pid)
            if len(targets) == 500:
                break

    print(f"Found {len(targets)} targets matching criteria.")

    start_time = time.time()
    
    def extract(pid):
        res = subprocess.run(['python3', 'scripts/extract_pack.py', pid], capture_output=True, text=True, errors='replace')
        if res.returncode != 0:
            return pid, False, res.stderr
        return pid, True, res.stdout

    success_count = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        for pid, success, out in executor.map(extract, targets):
            if success:
                success_count += 1
                print(f"[OK] {pid}")
            else:
                print(f"[FAIL] {pid}: {out.strip()}")

    duration = time.time() - start_time
    print(f"Extracted {success_count}/{len(targets)} packs in {duration:.2f} seconds.")

if __name__ == '__main__':
    main()
