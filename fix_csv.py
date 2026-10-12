import os
import csv

filepath = 'F:/Project-F/Assets/Resources/Localization/game_text.csv'
rows = []
modified = False
with open(filepath, 'r', encoding='utf-8-sig', newline='') as f:
    reader = csv.reader(f)
    for row in reader:
        if len(row) > 5 and '특별히 머물러' in row[5]:
            row[5] = row[5].replace('크큭', '크흠')
            modified = True
        rows.append(row)

if modified:
    with open(filepath, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)
    print("CSV updated.")
else:
    print("Not found in CSV.")
