import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# -------------------------------------------------
# STEP 20: FLOOD RISK VISUALIZATION
# -------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

INPUT_FILE = BASE_DIR / "data" / "flood_early_warning.csv"

OUTPUT_FILE = BASE_DIR / "data" / "flood_risk_visualization.png"

print("\nFLOOD RISK VISUALIZATION")
print("-------------------------")

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

print("Records loaded:", len(df))

# -------------------------------------------------
# FLOOD THRESHOLD
# -------------------------------------------------

FLOOD_THRESHOLD = 736.23

# -------------------------------------------------
# CREATE PLOT
# -------------------------------------------------

plt.figure(figsize=(14, 6))

plt.plot(
    df["Date"],
    df["Discharge"],
    linewidth=1
)

# Flood threshold
plt.axhline(
    y=FLOOD_THRESHOLD,
    linestyle="--",
    linewidth=2
)

plt.xlabel("Date")
plt.ylabel("Maximum Daily Discharge")
plt.title(
    "Krishna Basin Flood Risk Monitoring"
)

plt.tight_layout()

# -------------------------------------------------
# SAVE
# -------------------------------------------------

plt.savefig(
    OUTPUT_FILE,
    dpi=300,
    bbox_inches="tight"
)

plt.show()

print("\nVisualization saved to:")
print(OUTPUT_FILE)

print("\nSTEP 20 COMPLETED")