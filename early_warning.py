import pandas as pd
from pathlib import Path

# -------------------------------------------------
# STEP 19: FLOOD EARLY WARNING LOGIC
# -------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

DISCHARGE_FILE = (
    BASE_DIR / "data" / "krishna_discharge_daily.csv"
)

OUTPUT_FILE = (
    BASE_DIR / "data" / "flood_early_warning.csv"
)

print("\nFLOOD EARLY WARNING SYSTEM")
print("----------------------------")

# -------------------------------------------------
# FLOOD THRESHOLD
# -------------------------------------------------

FLOOD_THRESHOLD = 736.23

print("Flood threshold:", FLOOD_THRESHOLD)

# -------------------------------------------------
# LOAD REAL DISCHARGE DATA
# -------------------------------------------------

df = pd.read_csv(DISCHARGE_FILE)

df["Date"] = pd.to_datetime(
    df["Date"],
    errors="coerce"
)

df = df.dropna(subset=["Date"])

print("Discharge records:", len(df))

# -------------------------------------------------
# USE REAL DAILY MAXIMUM DISCHARGE
# -------------------------------------------------

df["Discharge"] = pd.to_numeric(
    df["Discharge_Max"],
    errors="coerce"
)

df = df.dropna(subset=["Discharge"])

# -------------------------------------------------
# CALCULATE RISK RATIO
# -------------------------------------------------

df["Risk_Ratio"] = (
    df["Discharge"] / FLOOD_THRESHOLD
)

# -------------------------------------------------
# EARLY WARNING LEVEL
# -------------------------------------------------

def classify_warning(ratio):

    if ratio < 0.75:
        return "NORMAL"

    elif ratio < 1.00:
        return "WATCH"

    elif ratio < 1.25:
        return "WARNING"

    else:
        return "CRITICAL"


df["Warning_Level"] = (
    df["Risk_Ratio"]
    .apply(classify_warning)
)

# -------------------------------------------------
# FLOOD RISK
# -------------------------------------------------

df["Flood_Risk"] = (
    df["Discharge"] >= FLOOD_THRESHOLD
).astype(int)

# -------------------------------------------------
# DISPLAY RESULTS
# -------------------------------------------------

print("\nEarly warning results:")

print(
    df[
        [
            "Date",
            "Discharge",
            "Risk_Ratio",
            "Warning_Level",
            "Flood_Risk"
        ]
    ].tail(20).to_string(index=False)
)

# -------------------------------------------------
# SUMMARY
# -------------------------------------------------

print("\nWARNING SUMMARY")
print("----------------")

print(
    df["Warning_Level"]
    .value_counts()
)

# -------------------------------------------------
# SAVE RESULTS
# -------------------------------------------------

df[
    [
        "Date",
        "Discharge",
        "Risk_Ratio",
        "Warning_Level",
        "Flood_Risk"
    ]
].to_csv(
    OUTPUT_FILE,
    index=False
)

print("\nResults saved to:")
print(OUTPUT_FILE)

print("\nSTEP 19 COMPLETED")