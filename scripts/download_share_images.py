import os
import json
import time
import glob
import urllib.request
from urllib.error import HTTPError, URLError
import re

DATA_FILE = os.path.join(os.path.dirname(__file__), '../web/viewer_data.json')
OUT_DIR = os.path.join(os.path.dirname(__file__), '../web/images/packs')

USER_AGENT = 'AssetStudio/1.0 (Local Archive Tool)'

def setup():
    if not os.path.exists(OUT_DIR):
        os.makedirs(OUT_DIR)

from html.parser import HTMLParser

class MetaImageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.image_url = None

    def handle_starttag(self, tag, attrs):
        if self.image_url:
            return # Already found
        if tag == "meta":
            attrs_dict = dict(attrs)
            if attrs_dict.get("property") == "og:image" or attrs_dict.get("name") == "twitter:image":
                if "content" in attrs_dict:
                    self.image_url = attrs_dict["content"].replace('&amp;', '&')

def get_image_url(html):
    parser = MetaImageParser()
    try:
        parser.feed(html)
        return parser.image_url
    except Exception as e:
        print(f"  [!] Parser error: {e}")
        return None

def fetch_with_retry(url, is_binary=False):
    req = urllib.request.Request(url, headers={'User-Agent': USER_AGENT})
    while True:
        try:
            with urllib.request.urlopen(req, timeout=10) as response:
                return response.read() if is_binary else response.read().decode('utf-8', errors='ignore')
        except HTTPError as e:
            if e.code == 429:
                print(f"  [!] 429 Too Many Requests hit for {url}. Sleeping for 130 seconds...")
                time.sleep(130)
            else:
                print(f"  [!] HTTP Error {e.code} for {url}")
                return "ERROR_404" if e.code == 404 else None
        except Exception as e:
            print(f"  [!] Error fetching {url}: {e}")
            return None

def main():
    setup()
    
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    packs = data.get('asset_packs', {})
    total = len(packs)
    
    print(f"Found {total} packs. Starting download process...")
    
    for i, (pack_id, pack_info) in enumerate(packs.items(), 1):
        source_url = pack_info.get('source_url')
        if not source_url:
            print(f"[{i}/{total}] Skipping {pack_id} - No source URL")
            continue
            
        if '/download/' in source_url:
            public_url = source_url.split('/download/')[0]
        else:
            public_url = source_url
            
        safe_id = pack_id.replace('/', '_')
        
        # Check if already downloaded or explicitly marked as not having one
        existing = glob.glob(os.path.join(OUT_DIR, f"{safe_id}.social-share-image.*"))
        no_image = os.path.join(OUT_DIR, f"{safe_id}.no-share-image")
        
        if existing:
            print(f"[{i}/{total}] Skipping {pack_id} - Image already exists")
            continue
        if os.path.exists(no_image):
            print(f"[{i}/{total}] Skipping {pack_id} - Marked as no share image")
            continue
            
        print(f"[{i}/{total}] Processing {pack_id}...")
        
        # 1. Fetch HTML
        html = fetch_with_retry(public_url)
        if not html:
            continue
        elif html == "ERROR_404":
            print(f"  [-] 404 Not Found for {pack_id}. Marking as no image.")
            open(no_image, 'w').close()
            time.sleep(3.0)
            continue
            
        img_url = get_image_url(html)
        if not img_url:
            print(f"  [-] No og:image found for {pack_id}. Marking as no image.")
            open(no_image, 'w').close()
            time.sleep(3.0)
            continue
            
        # 2. Delay before fetching image
        time.sleep(3.0)
        
        # 3. Determine extension
        ext = '.jpg' # default
        if '.gif' in img_url.lower(): ext = '.gif'
        elif '.png' in img_url.lower(): ext = '.png'
        elif '.webp' in img_url.lower(): ext = '.webp'
            
        # 4. Fetch Image
        img_data = fetch_with_retry(img_url, is_binary=True)
        if img_data:
            out_path = os.path.join(OUT_DIR, f"{safe_id}.social-share-image{ext}")
            with open(out_path, 'wb') as f:
                f.write(img_data)
            print(f"  [+] Saved {os.path.basename(out_path)}")
            
        # 5. Delay before next pack
        time.sleep(3.0)

if __name__ == '__main__':
    main()
