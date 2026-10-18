import pandas as pd
from pathlib import Path
from itertools import combinations


# ============================================================
# STEP 17
# QUANTUM VS CLASSICAL SENSOR PLACEMENT
# ============================================================

print("\n")
print("QUANTUM VS CLASSICAL SENSOR PLACEMENT")
print("--------------------------------------")


# ------------------------------------------------------------
# 1. FILE PATHS
# ------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

INPUT_FILE = BASE_DIR / "sensor_locations.csv"
QUANTUM_FILE = BASE_DIR / "quantum_selected_sensors.csv"


# ------------------------------------------------------------
# 2. LOAD DATA
# ------------------------------------------------------------

df = pd.read_csv(INPUT_FILE)

quantum_df = pd.read_csv(QUANTUM_FILE)

print(f"Candidate stations: {len(df)}")


# ------------------------------------------------------------
# 3. CALCULATE IMPORTANCE SCORE
# ------------------------------------------------------------

df["Importance_Score"] = (
    0.40 * df["Flood_Risk"]
    + 0.30 * df["Coverage"]
    + 0.20 * df["Rainfall_Risk"]
    + 0.10 * df["Discharge_Risk"]
)


# ------------------------------------------------------------
# 4. SENSOR BUDGET
# ------------------------------------------------------------

SENSOR_BUDGET = 3


# ------------------------------------------------------------
# 5. QUANTUM SOLUTION
# ------------------------------------------------------------

quantum_stations = quantum_df["Selected_Station"].tolist()

quantum_score = quantum_df["Importance_Score"].sum()


# ------------------------------------------------------------
# 6. CLASSICAL OPTIMIZATION
# ------------------------------------------------------------

stations = df["Station_ID"].tolist()

weights = df["Importance_Score"].tolist()

best_classical_score = -1
best_classical_combination = None


for combination in combinations(
    range(len(stations)),
    SENSOR_BUDGET
):

    score = sum(
        weights[i]
        for i in combination
    )

    if score > best_classical_score:

        best_classical_score = score

        best_classical_combination = combination


classical_stations = [
    stations[i]
    for i in best_classical_combination
]


# ------------------------------------------------------------
# 7. COMPARE RESULTS
# ------------------------------------------------------------

same_solution = (
    set(quantum_stations)
    == set(classical_stations)
)


score_difference = (
    quantum_score
    - best_classical_score
)


if best_classical_score != 0:

    score_difference_percent = (
        score_difference
        / best_classical_score
    ) * 100

else:

    score_difference_percent = 0


# ------------------------------------------------------------
# 8. DISPLAY RESULTS
# ------------------------------------------------------------

print("\n")
print("QUANTUM RESULT")
print("--------------")

print(
    "Selected stations:",
    quantum_stations
)

print(
    f"Importance score: {quantum_score:.4f}"
)


print("\n")
print("CLASSICAL RESULT")
print("----------------")

print(
    "Selected stations:",
    classical_stations
)

print(
    f"Importance score: "
    f"{best_classical_score:.4f}"
)


print("\n")
print("COMPARISON")
print("----------")

print(
    f"Same station selection: "
    f"{'YES' if same_solution else 'NO'}"
)

print(
    f"Score difference: "
    f"{score_difference:.4f}"
)

print(
    f"Score difference (%): "
    f"{score_difference_percent:.2f}%"
)


# ------------------------------------------------------------
# 9. CREATE COMPARISON TABLE
# ------------------------------------------------------------

comparison = pd.DataFrame({

    "Method": [
        "QAOA Quantum",
        "Classical Exhaustive"
    ],

    "Selected_Stations": [
        ", ".join(quantum_stations),
        ", ".join(classical_stations)
    ],

    "Number_of_Sensors": [
        len(quantum_stations),
        len(classical_stations)
    ],

    "Total_Importance_Score": [
        quantum_score,
        best_classical_score
    ]

})


# ------------------------------------------------------------
# 10. SAVE COMPARISON
# ------------------------------------------------------------

OUTPUT_FILE = (
    BASE_DIR /
    "quantum_vs_classical_sensor_placement.csv"
)

comparison.to_csv(
    OUTPUT_FILE,
    index=False
)


# ------------------------------------------------------------
# 11. FINAL SUMMARY
# ------------------------------------------------------------

print("\n")
print("COMPARISON TABLE")
print("----------------")

print(comparison.to_string(index=False))


print("\n")
print("Result saved to:")

print(OUTPUT_FILE)


print("\n")
print("STEP 17 COMPLETED")
print("--------------------------------")