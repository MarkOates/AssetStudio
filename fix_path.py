import os
BASE_DIR = os.path.dirname(os.path.abspath('scripts/auto_catalog_ai.py'))
# The correct path to Assets is /Users/markoates/Assets, which is os.path.join(BASE_DIR, '..', '..', 'Assets')
print(os.path.abspath(os.path.join(BASE_DIR, '..', '..', 'Assets')))
