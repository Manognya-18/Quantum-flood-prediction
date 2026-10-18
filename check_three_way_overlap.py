import pandas as pd
from pathlib import Path

# File paths
rainfall_path = Path(r"data\krishna_rainfall_daily.csv")
discharge_path = Path(r"data\krishna_discharge_daily.csv")
water_path = Path(r"data\krishna_water_level_daily.csv")

# Load datasets
rainfall = pd.read_csv(rainfall_path)
discharge = pd.read_csv(discharge_path)
water = pd.read_csv(water_path)

# Convert dates
rainfall["Date"] = pd.to_datetime(rainfall["Date"])
discharge["Date"] = pd.to_datetime(discharge["Date"])
water["Date"] = pd.to_datetime(water["Date"])

# Get unique dates
rainfall_dates = set(rainfall["Date"])
discharge_dates = set(discharge["Date"])
water_dates = set(water["Date"])

# Find common dates
common_dates = (
    rainfall_dates
    & discharge_dates
    & water_dates
)

print("-----------------------------------")
print("3-DATASET DATE OVERLAP")
print("-----------------------------------")

print("Rainfall dates:", len(rainfall_dates))
print("Discharge dates:", len(discharge_dates))
print("Water-level dates:", len(water_dates))

print("Common dates in ALL THREE:", len(common_dates))

print("\nFirst 20 common dates:")

for date in sorted(common_dates)[:20]:
    print(date.date())