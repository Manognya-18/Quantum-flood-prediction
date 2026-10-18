import pandas as pd
import numpy as np
from pathlib import Path
from itertools import combinations

from scipy.optimize import minimize

from qiskit import QuantumCircuit
from qiskit.circuit.library import QAOAAnsatz
from qiskit.quantum_info import Statevector

from qiskit_optimization import QuadraticProgram


# ============================================================
# STEP 16
# QUANTUM SENSOR PLACEMENT USING QAOA
# ============================================================

print("\n")
print("QUANTUM SENSOR PLACEMENT USING QAOA")
print("-----------------------------------")


# ------------------------------------------------------------
# 1. LOAD SENSOR DATA
# ------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "sensor_locations.csv"

df = pd.read_csv(INPUT_FILE)

print(f"Candidate stations: {len(df)}")

print("\nStation importance scores:")
print(df[["Station_ID", "Flood_Risk", "Coverage"]])


# ------------------------------------------------------------
# 2. CALCULATE IMPORTANCE SCORE
# ------------------------------------------------------------

# Same weighting used in Step 15
df["Importance_Score"] = (
    0.40 * df["Flood_Risk"]
    + 0.30 * df["Coverage"]
    + 0.20 * df["Rainfall_Risk"]
    + 0.10 * df["Discharge_Risk"]
)

stations = df["Station_ID"].tolist()
weights = df["Importance_Score"].tolist()

n = len(stations)

print("\nCalculated importance scores:")

for station, score in zip(stations, weights):
    print(f"{station}: {score:.4f}")


# ------------------------------------------------------------
# 3. SENSOR BUDGET
# ------------------------------------------------------------

SENSOR_BUDGET = 3

print(f"\nSensor budget: {SENSOR_BUDGET}")


# ------------------------------------------------------------
# 4. CREATE QUBO
# ------------------------------------------------------------

# We want to MAXIMIZE:
#
#     sum(weight_i * x_i)
#
# where:
#
#     x_i = 1 -> select station
#     x_i = 0 -> don't select station
#
# We also require:
#
#     sum(x_i) = 3
#
# QAOA works naturally with unconstrained QUBO problems.
# Therefore we add a penalty:
#
#     P * (sum(x_i) - 3)^2
#
# to force the solution to contain exactly 3 stations.

PENALTY = 2.0

qp = QuadraticProgram("Quantum_Flood_Sensor_Placement")


# Create binary variables
for station in stations:
    qp.binary_var(name=station)


# ------------------------------------------------------------
# 5. BUILD PENALIZED OBJECTIVE
# ------------------------------------------------------------

# Minimize:
#
# -Importance + Penalty * (number_selected - 3)^2

linear = {}
quadratic = {}

for i, station in enumerate(stations):

    # Expansion of:
    # P * (sum(x_i) - K)^2
    #
    # Linear contribution:
    # P * (1 - 2K)

    linear[station] = (
        -weights[i]
        + PENALTY * (1 - 2 * SENSOR_BUDGET)
    )


# Quadratic contribution:
#
# 2P * x_i*x_j

for i in range(n):

    for j in range(i + 1, n):

        quadratic[(stations[i], stations[j])] = 2 * PENALTY


# Constant P*K^2 does not affect optimization,
# so it does not need to be included.

qp.minimize(
    linear=linear,
    quadratic=quadratic
)


print("\nQUBO created successfully.")

print(f"Number of variables: {n}")
print(f"Penalty value: {PENALTY}")


# ------------------------------------------------------------
# 6. CONVERT QUBO TO ISING HAMILTONIAN
# ------------------------------------------------------------

ising_operator, offset = qp.to_ising()

print("\nIsing Hamiltonian created.")

print(f"Number of qubits: {ising_operator.num_qubits}")


# ------------------------------------------------------------
# 7. CREATE QAOA CIRCUIT
# ------------------------------------------------------------

REPS = 2

qaoa_circuit = QAOAAnsatz(
    cost_operator=ising_operator,
    reps=REPS
)

print("\nQAOA circuit created.")

print(f"QAOA layers (p): {REPS}")
print(f"Qubits: {qaoa_circuit.num_qubits}")
print(f"Parameters: {len(qaoa_circuit.parameters)}")


# ------------------------------------------------------------
# 8. EXPECTATION VALUE FUNCTION
# ------------------------------------------------------------

def calculate_energy(params):

    """
    Calculates the expected QUBO energy
    using a quantum statevector.
    """

    bound_circuit = qaoa_circuit.assign_parameters(
        params
    )

    state = Statevector.from_instruction(
        bound_circuit
    )

    probabilities = state.probabilities_dict()

    total_energy = 0.0

    for bitstring, probability in probabilities.items():

        # Qiskit displays qubit states in reverse order.
        bits = bitstring[::-1]

        selected = [
            int(bit)
            for bit in bits
        ]

        number_selected = sum(selected)

        importance = sum(
            weights[i] * selected[i]
            for i in range(n)
        )

        # Penalized objective
        energy = (
            -importance
            + PENALTY *
            (number_selected - SENSOR_BUDGET) ** 2
        )

        total_energy += probability.real * energy

    return float(total_energy)


# ------------------------------------------------------------
# 9. INITIAL PARAMETERS
# ------------------------------------------------------------

num_parameters = len(qaoa_circuit.parameters)

initial_parameters = np.zeros(
    num_parameters
)

# Small deterministic initialization
initial_parameters[:] = 0.1


print("\nStarting QAOA optimization...")


# ------------------------------------------------------------
# 10. CLASSICAL OPTIMIZER
# ------------------------------------------------------------

result = minimize(
    calculate_energy,
    initial_parameters,
    method="COBYLA",
    options={
        "maxiter": 100,
        "rhobeg": 0.5
    }
)


print("\nQAOA optimization completed.")

print(f"Optimizer success: {result.success}")
print(f"Iterations: {result.nfev}")
print(f"Final expectation value: {result.fun:.6f}")


# ------------------------------------------------------------
# 11. GET FINAL QUANTUM STATE
# ------------------------------------------------------------

final_circuit = qaoa_circuit.assign_parameters(
    result.x
)

final_state = Statevector.from_instruction(
    final_circuit
)

probabilities = final_state.probabilities_dict()


# ------------------------------------------------------------
# 12. FIND BEST FEASIBLE QUANTUM SOLUTION
# ------------------------------------------------------------

feasible_states = []

for bitstring, probability in probabilities.items():

    bits = bitstring[::-1]

    selected = [
        int(bit)
        for bit in bits
    ]

    number_selected = sum(selected)

    if number_selected == SENSOR_BUDGET:

        importance = sum(
            weights[i] * selected[i]
            for i in range(n)
        )

        feasible_states.append(
            (
                probability.real,
                importance,
                bitstring,
                selected
            )
        )


# Sort by quantum probability
feasible_states.sort(
    key=lambda x: x[0],
    reverse=True
)


# ------------------------------------------------------------
# 13. DISPLAY QUANTUM RESULT
# ------------------------------------------------------------

print("\n")
print("QUANTUM SENSOR PLACEMENT RESULT")
print("--------------------------------")

if feasible_states:

    best_probability = feasible_states[0][0]
    best_importance = feasible_states[0][1]
    best_bits = feasible_states[0][2]
    best_selection = feasible_states[0][3]

    selected_stations = [
        stations[i]
        for i in range(n)
        if best_selection[i] == 1
    ]

    print(f"Selected stations: {selected_stations}")

    print(
        f"Quantum probability: "
        f"{best_probability:.4f}"
    )

    print(
        f"Total importance score: "
        f"{best_importance:.4f}"
    )

    print("\nSelected sensor locations:")

    for station in selected_stations:
        score = df.loc[
            df["Station_ID"] == station,
            "Importance_Score"
        ].iloc[0]

        print(
            f"  {station} "
            f"-> Importance = {score:.4f}"
        )

else:

    print("No feasible 3-station solution found.")


# ------------------------------------------------------------
# 14. CLASSICAL EXHAUSTIVE CHECK
# ------------------------------------------------------------

print("\n")
print("CLASSICAL VALIDATION")
print("--------------------")

best_classical = None

for combination in combinations(
    range(n),
    SENSOR_BUDGET
):

    score = sum(
        weights[i]
        for i in combination
    )

    if (
        best_classical is None
        or score > best_classical[0]
    ):

        best_classical = (
            score,
            combination
        )


classical_score = best_classical[0]
classical_stations = [
    stations[i]
    for i in best_classical[1]
]

print(
    f"Best classical combination: "
    f"{classical_stations}"
)

print(
    f"Classical importance score: "
    f"{classical_score:.4f}"
)


# ------------------------------------------------------------
# 15. SAVE QUANTUM RESULT
# ------------------------------------------------------------

if feasible_states:

    output = pd.DataFrame({
        "Selected_Station": selected_stations,
        "Importance_Score": [
            df.loc[
                df["Station_ID"] == station,
                "Importance_Score"
            ].iloc[0]
            for station in selected_stations
        ]
    })

    output_file = BASE_DIR / "quantum_selected_sensors.csv"

    output.to_csv(
        output_file,
        index=False
    )

    print("\nResult saved to:")

    print(output_file)


print("\n")
print("STEP 16 COMPLETED")
print("--------------------------------")