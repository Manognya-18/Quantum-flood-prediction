import pandas as pd
import numpy as np
from pathlib import Path

# -------------------------------------------------
# STEP 14: REAL DATA-BASED SENSOR CANDIDATE GENERATION
# -------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR.parent / "data"

RAINFALL_FILE = DATA_DIR / "krishna_rainfall_daily.csv"
DISCHARGE_FILE = DATA_DIR / "krishna_discharge_daily.csv"

OUTPUT_FILE = BASE_DIR / "sensor_locations.csv"

print("\nREAL KRISHNA BASIN SENSOR CANDIDATE GENERATION")
print("------------------------------------------------")

# -------------------------------------------------
# LOAD REAL CLEANED DATA
# -------------------------------------------------

rainfall = pd.read_csv(RAINFALL_FILE)
discharge = pd.read_csv(DISCHARGE_FILE)

print("Rainfall rows:", len(rainfall))
print("Discharge rows:", len(discharge))

# Convert dates
rainfall["Date"] = pd.to_datetime(rainfall["Date"], errors="coerce")
discharge["Date"] = pd.to_datetime(discharge["Date"], errors="coerce")

rainfall = rainfall.dropna(subset=["Date"])
discharge = discharge.dropna(subset=["Date"])

# -------------------------------------------------
# MERGE RAINFALL + DISCHARGE BY DATE
# -------------------------------------------------

df = pd.merge(
    rainfall,
    discharge,
    on="Date",
    how="inner"
)

print("Common dates:", len(df))

if len(df) == 0:
    raise ValueError("No common dates found between rainfall and discharge data.")

# -------------------------------------------------
# CALCULATE RISK COMPONENTS
# -------------------------------------------------

def normalize(series):
    minimum = series.min()
    maximum = series.max()

    if maximum == minimum:
        return pd.Series(0.5, index=series.index)

    return (series - minimum) / (maximum - minimum)


df["Rainfall_Risk"] = normalize(df["Rainfall_Total"])

df["Discharge_Risk"] = normalize(df["Discharge_Max"])

# Flood risk combines rainfall and discharge conditions
df["Flood_Risk"] = (
    0.5 * df["Rainfall_Risk"]
    + 0.5 * df["Discharge_Risk"]
)

# -------------------------------------------------
# CREATE REAL DATA-BASED CANDIDATE STATIONS
# -------------------------------------------------
#
# Your cleaned daily files are basin-level aggregates.
# Therefore, they do NOT contain station coordinates.
#
# We create candidate monitoring zones from the
# available station-count information instead of
# inventing geographical coordinates.
#
# Candidate zones are selected from the highest-risk
# observations in the real dataset.
# -------------------------------------------------

# Use the six highest-risk dates as candidate
# monitoring scenarios.
candidate_count = min(6, len(df))

candidates = df.nlargest(candidate_count, "Flood_Risk").copy()

# -------------------------------------------------
# COVERAGE
# -------------------------------------------------
#
# Coverage is based on the number of monitoring
# stations represented in the actual daily data.
# This is normalized across the selected candidates.
# -------------------------------------------------

coverage_raw = (
    candidates["Rainfall_Station_Count"]
    + candidates["Discharge_Station_Count"]
)

candidates["Coverage"] = normalize(coverage_raw)

# -------------------------------------------------
# COST
# -------------------------------------------------
#
# Equal deployment cost assumption.
# This is an optimization constraint, not a measured
# physical sensor price.
# -------------------------------------------------

candidates["Cost"] = 1

# -------------------------------------------------
# STATION IDs
# -------------------------------------------------

candidates = candidates.reset_index(drop=True)

candidates["Station_ID"] = [
    f"KR-{i+1:02d}" for i in range(len(candidates))
]

# -------------------------------------------------
# FINAL TABLE
# -------------------------------------------------

output = candidates[
    [
        "Station_ID",
        "Rainfall_Risk",
        "Discharge_Risk",
        "Flood_Risk",
        "Coverage",
        "Cost"
    ]
].copy()

# Round values
for column in [
    "Rainfall_Risk",
    "Discharge_Risk",
    "Flood_Risk",
    "Coverage"
]:
    output[column] = output[column].round(4)

# Save
output.to_csv(OUTPUT_FILE, index=False)

# -------------------------------------------------
# DISPLAY RESULT
# -------------------------------------------------

print("\nGenerated candidate stations:")
print(output.to_string(index=False))

print("\nSaved to:")
print(OUTPUT_FILE)

print("\nSTEP 14 COMPLETED")