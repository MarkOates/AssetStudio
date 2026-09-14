content = open('scripts/build_viewer_data.py').read()
content = content.replace(
    '''            asset = {
                "identifier": row['identifier'],
                "name": row['name'],''',
    '''            asset = {
                "identifier": row['identifier'],
                "name": row['name'],
                "blacklisted_type": None,'''
)
with open('scripts/build_viewer_data.py', 'w') as f:
    f.write(content)
print("Patched build_viewer_data.py")
