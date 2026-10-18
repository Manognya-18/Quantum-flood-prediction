import csv
from pathlib import Path

path = Path(r'data\river water discharge dataset 3 2001-2025.csv')
with path.open('r', encoding='utf-8-sig', newline='') as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    rows = list(reader)

filtered = [row for row in rows if str(row.get('Basin', '')).strip().lower() == 'krishna']

with path.open('w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(filtered)

print(f'Kept {len(filtered)} rows')
