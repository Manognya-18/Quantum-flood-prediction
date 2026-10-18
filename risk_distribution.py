import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# -------------------------------------------------
# STEP 24: FLOOD RISK DISTRIBUTION VISUALIZATION
# -------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

INPUT_FILE = BASE_DIR / "data" / "flood_early_warning.csv"
OUTPUT_FILE = BASE_DIR / "data" / "risk_distribution.png"

print("\nFLOOD RISK DISTRIBUTION VISUALIZATION")
print("--------------------------------------")

# -------------------------------------------------
# LOAD DATA
# -------------------------------------------------

df = pd.read_csv(INPUT_FILE)

# -------------------------------------------------
# COUNT WARNING LEVELS
# -------------------------------------------------

risk_counts = (
    df["Warning_Level"]
    .value_counts()
    .reindex(
        ["NORMAL", "WATCH", "WARNING", "CRITICAL"],
        fill_value=0
    )
)

print("\nRisk distribution:")
print(risk_counts)

# -------------------------------------------------
# CREATE BAR CHART
# -------------------------------------------------

plt.figure(figsize=(9, 6))

bars = plt.bar(
    risk_counts.index,
    risk_counts.values
)

plt.xlabel("Warning Level")
plt.ylabel("Number of Records")

plt.title(
    "Krishna Basin Flood Risk Distribution"
)

# Add values above bars
for bar, value in zip(
    bars,
    risk_counts.values
):
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height(),
        str(value),
        ha="center",
        va="bottom"
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

print("\nChart saved to:")
print(OUTPUT_FILE)

print("\nSTEP 24 COMPLETED")