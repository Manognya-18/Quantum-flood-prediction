import pandas as pd
from qiskit_optimization import QuadraticProgram
from pathlib import Path

# -------------------------------------------------
# STEP 15: SENSOR PLACEMENT OPTIMIZATION
# -------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "sensor_locations.csv"

df = pd.read_csv(INPUT_FILE)

print("\nSENSOR PLACEMENT OPTIMIZATION")
print("--------------------------------")

print("Candidate stations:", len(df))

# Number of sensors we are allowed to select
SENSOR_BUDGET = 3

# Create a score from the REAL station data
df["Importance_Score"] = (
    0.25 * df["Rainfall_Risk"]
    + 0.25 * df["Discharge_Risk"]
    + 0.30 * df["Flood_Risk"]
    + 0.20 * df["Coverage"]
)

print("\nStation scores:")
print(df[["Station_ID", "Importance_Score"]])

# -------------------------------------------------
# CREATE QUADRATIC PROGRAM
# -------------------------------------------------

problem = QuadraticProgram("Flood_Sensor_Placement")

station_ids = df["Station_ID"].tolist()

# Binary variable for every candidate station
for station in station_ids:
    problem.binary_var(name=str(station))

# -------------------------------------------------
# OBJECTIVE
# -------------------------------------------------

linear = {}

for _, row in df.iterrows():
    station = str(row["Station_ID"])
    score = float(row["Importance_Score"])

    # Maximize importance
    linear[station] = score

problem.maximize(linear=linear)

# -------------------------------------------------
# SENSOR BUDGET CONSTRAINT
# -------------------------------------------------

constraint = {
    str(station): 1
    for station in station_ids
}

problem.linear_constraint(
    linear=constraint,
    sense="==",
    rhs=SENSOR_BUDGET,
    name="sensor_budget"
)

# -------------------------------------------------
# DISPLAY PROBLEM
# -------------------------------------------------

print("\nOptimization problem created.")
print(problem)

print("\nSensor budget:", SENSOR_BUDGET)
print("Number of variables:", len(station_ids))

print("\nSTEP 15 COMPLETED")