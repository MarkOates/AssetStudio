content = open('scripts/build_viewer_data.py').read()
content = content.replace(
    '''                asset = {
                    "identifier": identifier,
                    "name": intra_pack_id,
                    "blacklisted_type": row.get('blacklisted_type') or None,''',
    '''                asset = {
                    "identifier": identifier,
                    "name": intra_pack_id,
                    "blacklisted_type": None,'''
)
with open('scripts/build_viewer_data.py', 'w') as f:
    f.write(content)
