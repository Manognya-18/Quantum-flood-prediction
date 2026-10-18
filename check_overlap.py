import pandas as pd
from pathlib import Path

# --------------------------------------------------
# 1. File paths
# --------------------------------------------------

rainfall_path = Path(r"data\krishna_rainfall_daily.csv")
discharge_path = Path(r"data\krishna_discharge_daily.csv")


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
# 4. Find common dates
# --------------------------------------------------

common_dates = sorted(
    set(rainfall["Date"].dropna())
    &
    set(discharge["Date"].dropna())
)


# --------------------------------------------------
# 5. Display results
# --------------------------------------------------

print("\n-----------------------------------")
print("DATE OVERLAP RESULTS")
print("-----------------------------------")

print("Rainfall dates:", rainfall["Date"].nunique())
print("Discharge dates:", discharge["Date"].nunique())
print("Common dates:", len(common_dates))

if common_dates:
    print("\nFirst 10 common dates:")

    for date in common_dates[:10]:
        print(date.strftime("%Y-%m-%d"))

    print("\nLast 10 common dates:")

    for date in common_dates[-10:]:
        print(date.strftime("%Y-%m-%d"))


# --------------------------------------------------
# 6. Calculate overlap percentage
# --------------------------------------------------

if rainfall["Date"].nunique() > 0:

    overlap_percentage = (
        len(common_dates)
        / rainfall["Date"].nunique()
    ) * 100

    print(
        f"\nRainfall dates having discharge data: "
        f"{overlap_percentage:.2f}%"
    )