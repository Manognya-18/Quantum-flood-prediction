import pandas as pd

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)

from qiskit.circuit.library import ZZFeatureMap, RealAmplitudes
from qiskit.primitives import StatevectorSampler

from qiskit_machine_learning.algorithms import VQC
from qiskit_machine_learning.optimizers import COBYLA
from qiskit_machine_learning.utils import algorithm_globals


# -----------------------------------
# 1. Set random seed
# -----------------------------------

algorithm_globals.random_seed = 42


# -----------------------------------
# 2. Load quantum datasets
# -----------------------------------

train_path = r"data\quantum_train.csv"
test_path = r"data\quantum_test.csv"

train = pd.read_csv(train_path)
test = pd.read_csv(test_path)

print("-----------------------------------")
print("VQC FLOOD PREDICTION")
print("-----------------------------------")

print("Training rows:", len(train))
print("Testing rows:", len(test))


# -----------------------------------
# 3. Select quantum features
# -----------------------------------

features = [
    "Rainfall_Today",
    "Rainfall_7Day",
    "Discharge_Today",
    "Discharge_Change"
]

target = "Flood_Risk_Next_Day"


# -----------------------------------
# 4. Create X and y
# -----------------------------------

X_train = train[features].values
y_train = train[target].values

X_test = test[features].values
y_test = test[target].values


print("\nNumber of features:", len(features))
print("Number of qubits:", len(features))


# -----------------------------------
# 5. Create quantum feature map
# -----------------------------------

feature_map = ZZFeatureMap(
    feature_dimension=len(features),
    reps=1,
    entanglement="linear"
)

print("\nQuantum feature map created.")


# -----------------------------------
# 6. Create variational ansatz
# -----------------------------------

ansatz = RealAmplitudes(
    num_qubits=len(features),
    reps=1,
    entanglement="linear"
)

print("Variational ansatz created.")


# -----------------------------------
# 7. Create optimizer
# -----------------------------------

optimizer = COBYLA(
    maxiter=50
)

print("COBYLA optimizer created.")


# -----------------------------------
# 8. Create sampler
# -----------------------------------

sampler = StatevectorSampler(
    default_shots=1024,
    seed=42
)

print("Statevector sampler created.")


# -----------------------------------
# 9. Create VQC
# -----------------------------------

vqc = VQC(
    sampler=sampler,
    feature_map=feature_map,
    ansatz=ansatz,
    optimizer=optimizer
)

print("VQC model created.")


# -----------------------------------
# 10. Train VQC
# -----------------------------------

print("\nTraining VQC...")
print("This may take some time...")

vqc.fit(
    X_train,
    y_train
)

print("VQC training completed.")


# -----------------------------------
# 11. Make predictions
# -----------------------------------

print("\nMaking predictions...")

y_pred = vqc.predict(X_test)


# -----------------------------------
# 12. Calculate metrics
# -----------------------------------

accuracy = accuracy_score(
    y_test,
    y_pred
)

precision = precision_score(
    y_test,
    y_pred,
    zero_division=0
)

recall = recall_score(
    y_test,
    y_pred,
    zero_division=0
)

f1 = f1_score(
    y_test,
    y_pred,
    zero_division=0
)

cm = confusion_matrix(
    y_test,
    y_pred
)


# -----------------------------------
# 13. Display results
# -----------------------------------

print("\n-----------------------------------")
print("VQC MODEL RESULTS")
print("-----------------------------------")

print(f"Accuracy  : {accuracy:.4f}")
print(f"Precision : {precision:.4f}")
print(f"Recall    : {recall:.4f}")
print(f"F1 Score  : {f1:.4f}")

print("\nConfusion Matrix:")
print(cm)

print("\nClassification Report:")

print(
    classification_report(
        y_test,
        y_pred,
        zero_division=0
    )
)


# -----------------------------------
# 14. Save predictions
# -----------------------------------

results = test.copy()

results["Predicted_Flood_Risk"] = y_pred

output_path = r"results\vqc_model_predictions.csv"

results.to_csv(
    output_path,
    index=False
)

print("\nPredictions saved to:")
print(output_path)

print("\n-----------------------------------")
print("VQC MODEL COMPLETED")
print("-----------------------------------")