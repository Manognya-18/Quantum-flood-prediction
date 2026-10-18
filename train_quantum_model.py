import pandas as pd

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)

from qiskit.circuit.library import ZZFeatureMap
from qiskit_machine_learning.kernels import FidelityQuantumKernel
from qiskit_machine_learning.algorithms import QSVC


# -----------------------------------
# 1. Load quantum datasets
# -----------------------------------

train_path = r"data\quantum_train.csv"
test_path = r"data\quantum_test.csv"

train = pd.read_csv(train_path)
test = pd.read_csv(test_path)

print("-----------------------------------")
print("QUANTUM FLOOD PREDICTION")
print("-----------------------------------")

print("Training rows:", len(train))
print("Testing rows:", len(test))


# -----------------------------------
# 2. Select quantum features
# -----------------------------------

features = [
    "Rainfall_Today",
    "Rainfall_7Day",
    "Discharge_Today",
    "Discharge_Change"
]

target = "Flood_Risk_Next_Day"


# -----------------------------------
# 3. Create X and y
# -----------------------------------

X_train = train[features]
y_train = train[target]

X_test = test[features]
y_test = test[target]


print("\nNumber of quantum features:", len(features))
print("Number of qubits:", len(features))


# -----------------------------------
# 4. Create quantum feature map
# -----------------------------------

feature_map = ZZFeatureMap(
    feature_dimension=len(features),
    reps=2,
    entanglement="linear"
)

print("\nQuantum feature map created.")
print("Feature map:")
print(feature_map)


# -----------------------------------
# 5. Create quantum kernel
# -----------------------------------

quantum_kernel = FidelityQuantumKernel(
    feature_map=feature_map
)

print("\nQuantum kernel created.")


# -----------------------------------
# 6. Create QSVC
# -----------------------------------

model = QSVC(
    quantum_kernel=quantum_kernel,
    class_weight="balanced"
)

print("\nQSVC model created.")


# -----------------------------------
# 7. Train quantum model
# -----------------------------------

print("\nTraining quantum model...")

model.fit(
    X_train,
    y_train
)

print("Quantum model training completed.")


# -----------------------------------
# 8. Make predictions
# -----------------------------------

print("\nMaking predictions...")

y_pred = model.predict(X_test)


# -----------------------------------
# 9. Calculate metrics
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
# 10. Display results
# -----------------------------------

print("\n-----------------------------------")
print("QUANTUM MODEL RESULTS")
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
# 11. Save predictions
# -----------------------------------

results = test.copy()

results["Predicted_Flood_Risk"] = y_pred

output_path = (
    r"results\quantum_model_predictions.csv"
)

results.to_csv(
    output_path,
    index=False
)

print("\nPredictions saved to:")
print(output_path)

print("\n-----------------------------------")
print("QUANTUM MODEL COMPLETED")
print("-----------------------------------")