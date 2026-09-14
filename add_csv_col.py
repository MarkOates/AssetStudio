import csv
import os

CSV_PATH = '/Users/markoates/Assets/assets_db.csv'
TMP_PATH = '/Users/markoates/Assets/assets_db.csv.tmp'

with open(CSV_PATH, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)
    
    if 'blacklisted_type' not in header:
        header.append('blacklisted_type')
        
        with open(TMP_PATH, 'w', encoding='utf-8', newline='') as out:
            writer = csv.writer(out)
            writer.writerow(header)
            
            for row in reader:
                # Add an empty column for blacklisted_type since these are all valid
                row.append('')
                writer.writerow(row)
                
        os.rename(TMP_PATH, CSV_PATH)
        print("Added 'blacklisted_type' column to CSV.")
    else:
        print("Column already exists.")
