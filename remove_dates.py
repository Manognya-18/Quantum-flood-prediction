import csv
from pathlib import Path

path = Path(r'data\river water level 20021-2025 krishna basin.csv')
with path.open('r', encoding='utf-8-sig', newline='') as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    rows = list(reader)

removed_dates = {'01-11-2021 08:00', '09-12-2021 08:00'}
filtered = [row for row in rows if str(row.get('Data Acquisition Time', '')).strip() not in removed_dates]

with path.open('w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(filtered)

print(f'Removed {len(rows) - len(filtered)} rows; kept {len(filtered)} rows')
