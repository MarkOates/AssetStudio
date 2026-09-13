import json

with open('scripts/ai_catalog_proposals.json', 'r', encoding='utf-8', errors='replace') as f:
    text = f.read()

# We know the garbage starts around char 7147989
# Let's just slice it before the corrupted object starts.
# We can find the previous '{' that represents the start of an object at the top level array.

bad_index = text.find('roboid-hurt')
print("Bad index:", bad_index)

# Find the start of the object containing this bad index.
# The objects in the array start with '  {\n    "identifier":'
last_valid_obj = text.rfind('  {\n    "identifier":', 0, bad_index)
print("Last valid object starts at:", last_valid_obj)

# Cut the string there and append closing brackets
clean_text = text[:last_valid_obj]
clean_text = clean_text.rstrip()
if clean_text.endswith(','):
    clean_text = clean_text[:-1]

clean_text += '\n]'

try:
    data = json.loads(clean_text)
    print("Successfully parsed! Count:", len(data))
    with open('scripts/ai_catalog_proposals.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
except Exception as e:
    print("Failed to parse:", e)
