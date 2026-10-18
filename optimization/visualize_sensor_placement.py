import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# -------------------------------------------------
# STEP 18: SENSOR PLACEMENT VISUALIZATION
# -------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

SENSOR_FILE = BASE_DIR / "sensor_locations.csv"
QAOA_FILE = BASE_DIR / "quantum_selected_sensors.csv"

print("\nSENSOR PLACEMENT VISUALIZATION")
print("--------------------------------")

# -------------------------------------------------
# LOAD DATA
# -------------------------------------------------

df = pd.read_csv(SENSOR_FILE)
qaoa = pd.read_csv(QAOA_FILE)

# -------------------------------------------------
# CALCULATE IMPORTANCE SCORE
# -------------------------------------------------

df["Importance_Score"] = (
    0.40 * df["Flood_Risk"]
    + 0.30 * df["Coverage"]
    + 0.20 * df["Rainfall_Risk"]
    + 0.10 * df["Discharge_Risk"]
)

# -------------------------------------------------
# GET QAOA SELECTED STATIONS
# -------------------------------------------------

selected_stations = (
    qaoa["Selected_Station"]
    .astype(str)
    .tolist()
)

print("\nAll candidate stations:")
print(df["Station_ID"].tolist())

print("\nQAOA selected stations:")
print(selected_stations)

# -------------------------------------------------
# MARK SELECTED STATIONS
# -------------------------------------------------

df["Selected"] = (
    df["Station_ID"]
    .astype(str)
    .isin(selected_stations)
)

# -------------------------------------------------
# DISPLAY RESULTS
# -------------------------------------------------

print("\nSensor placement results:")

print(
    df[
        [
            "Station_ID",
            "Rainfall_Risk",
            "Discharge_Risk",
            "Flood_Risk",
            "Coverage",
            "Importance_Score",
            "Selected"
        ]
    ].to_string(index=False)
)

# -------------------------------------------------
# CREATE VISUALIZATION
# -------------------------------------------------

plt.figure(figsize=(10, 6))

bars = plt.bar(
    df["Station_ID"],
    df["Importance_Score"]
)

# Highlight QAOA-selected stations
for bar, selected in zip(bars, df["Selected"]):

    if selected:
        bar.set_hatch("//")

# Labels
plt.xlabel("Candidate Station")
plt.ylabel("Importance Score")

plt.title(
    "Quantum Sensor Placement - Candidate Station Analysis"
)

# Add score values
for bar, score in zip(
    bars,
    df["Importance_Score"]
):

    plt.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.01,
        f"{score:.3f}",
        ha="center"
    )

plt.ylim(0, 1.1)

plt.tight_layout()

# -------------------------------------------------
# SAVE IMAGE
# -------------------------------------------------

OUTPUT_FILE = (
    BASE_DIR /
    "sensor_placement_visualization.png"
)

plt.savefig(
    OUTPUT_FILE,
    dpi=300,
    bbox_inches="tight"
)

plt.show()

print("\nVisualization saved to:")
print(OUTPUT_FILE)

print("\nSTEP 18 COMPLETED")