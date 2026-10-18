import pandas as pd
from pathlib import Path

# -------------------------------------------------
# STEP 23: FLOOD RISK SUMMARY & STATISTICS
# -------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

INPUT_FILE = BASE_DIR / "data" / "flood_early_warning.csv"
OUTPUT_FILE = BASE_DIR / "data" / "flood_risk_summary.csv"

print("\nFLOOD RISK SUMMARY & STATISTICS")
print("--------------------------------")

# -------------------------------------------------
# LOAD DATA
# -------------------------------------------------

df = pd.read_csv(INPUT_FILE)

df["Date"] = pd.to_datetime(
    df["Date"],
    errors="coerce"
)

df["Discharge"] = pd.to_numeric(
    df["Discharge"],
    errors="coerce"
)

df = df.dropna(
    subset=["Date", "Discharge"]
)

# -------------------------------------------------
# BASIC STATISTICS
# -------------------------------------------------

total_records = len(df)

normal_count = (
    df["Warning_Level"] == "NORMAL"
).sum()

watch_count = (
    df["Warning_Level"] == "WATCH"
).sum()

warning_count = (
    df["Warning_Level"] == "WARNING"
).sum()

critical_count = (
    df["Warning_Level"] == "CRITICAL"
).sum()

# -------------------------------------------------
# PERCENTAGES
# -------------------------------------------------

normal_percent = (
    normal_count / total_records * 100
)

watch_percent = (
    watch_count / total_records * 100
)

warning_percent = (
    warning_count / total_records * 100
)

critical_percent = (
    critical_count / total_records * 100
)

# -------------------------------------------------
# MAXIMUM DISCHARGE
# -------------------------------------------------

max_row = df.loc[
    df["Discharge"].idxmax()
]

max_discharge = max_row["Discharge"]
max_date = max_row["Date"]
max_level = max_row["Warning_Level"]

# -------------------------------------------------
# PRINT SUMMARY
# -------------------------------------------------

print("\nRISK SUMMARY")
print("------------")

print("Total records:", total_records)

print(
    f"NORMAL   : {normal_count} "
    f"({normal_percent:.2f}%)"
)

print(
    f"WATCH    : {watch_count} "
    f"({watch_percent:.2f}%)"
)

print(
    f"WARNING  : {warning_count} "
    f"({warning_percent:.2f}%)"
)

print(
    f"CRITICAL : {critical_count} "
    f"({critical_percent:.2f}%)"
)

print("\nHIGHEST RECORDED DISCHARGE")
print("---------------------------")

print(
    f"Date      : {max_date.strftime('%Y-%m-%d')}"
)

print(
    f"Discharge : {max_discharge:.3f}"
)

print(
    f"Risk Level: {max_level}"
)

# -------------------------------------------------
# CREATE SUMMARY DATAFRAME
# -------------------------------------------------

summary = pd.DataFrame({
    "Metric": [
        "Total Records",
        "Normal Records",
        "Watch Records",
        "Warning Records",
        "Critical Records",
        "Normal Percentage",
        "Watch Percentage",
        "Warning Percentage",
        "Critical Percentage",
        "Maximum Discharge",
        "Maximum Discharge Date",
        "Maximum Discharge Risk Level"
    ],

    "Value": [
        total_records,
        normal_count,
        watch_count,
        warning_count,
        critical_count,
        round(normal_percent, 2),
        round(watch_percent, 2),
        round(warning_percent, 2),
        round(critical_percent, 2),
        round(max_discharge, 3),
        max_date.strftime("%Y-%m-%d"),
        max_level
    ]
})

# -------------------------------------------------
# SAVE SUMMARY
# -------------------------------------------------

summary.to_csv(
    OUTPUT_FILE,
    index=False
)

print("\nSummary saved to:")
print(OUTPUT_FILE)

print("\nSTEP 23 COMPLETED")