import pandas as pd
from pathlib import Path

# --------------------------------------------------
# 1. File paths
# --------------------------------------------------

rainfall_path = Path(r"data\krishna_rainfall_daily.csv")
discharge_path = Path(r"data\krishna_discharge_daily.csv")

output_path = Path(r"data\krishna_rainfall_discharge.csv")


# --------------------------------------------------
# 2. Load datasets
# --------------------------------------------------

rainfall = pd.read_csv(rainfall_path)
discharge = pd.read_csv(discharge_path)

print("Rainfall rows:", len(rainfall))
print("Discharge rows:", len(discharge))


# --------------------------------------------------
# 3. Convert Date columns
# --------------------------------------------------

rainfall["Date"] = pd.to_datetime(
    rainfall["Date"],
    errors="coerce"
)

discharge["Date"] = pd.to_datetime(
    discharge["Date"],
    errors="coerce"
)


# --------------------------------------------------
# 4. Merge using common dates
# --------------------------------------------------

merged = pd.merge(
    rainfall,
    discharge,
    on="Date",
    how="inner"
)


# --------------------------------------------------
# 5. Sort by date
# --------------------------------------------------

merged = merged.sort_values("Date").reset_index(drop=True)


# --------------------------------------------------
# 6. Save merged dataset
# --------------------------------------------------

merged.to_csv(
    output_path,
    index=False
)


# --------------------------------------------------
# 7. Display results
# --------------------------------------------------

print("\n-----------------------------------")
print("MERGE COMPLETED")
print("-----------------------------------")

print("Merged rows:", len(merged))
print("Merged columns:", len(merged.columns))

print("\nColumns:")
print(merged.columns.tolist())

print("\nFirst 5 rows:")
print(merged.head())

print("\nOutput file:")
print(output_path)