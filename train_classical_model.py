import pandas as pd
import os
import joblib

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)

# -----------------------------------
# 1. Load feature dataset
# -----------------------------------

input_path = r"data\krishna_flood_features.csv"

df = pd.read_csv(input_path)

df["Date"] = pd.to_datetime(df["Date"])

# Sort chronologically
df = df.sort_values("Date").reset_index(drop=True)

print("-----------------------------------")
print("CLASSICAL ML FLOOD PREDICTION")
print("-----------------------------------")

print("Total rows:", len(df))


# -----------------------------------
# 2. Define features
# -----------------------------------

features = [
    "Rainfall_Today",
    "Rainfall_Previous_Day",
    "Rainfall_3Day",
    "Rainfall_7Day",

    "Discharge_Today",
    "Discharge_Previous_Day",
    "Discharge_3Day_Average",
    "Discharge_Change"
]

target = "Flood_Risk_Next_Day"


# -----------------------------------
# 3. Create X and y
# -----------------------------------

X = df[features]
y = df[target]


# -----------------------------------
# 4. Time-based train/test split
# -----------------------------------

split_index = int(len(df) * 0.80)

X_train = X.iloc[:split_index]
X_test = X.iloc[split_index:]

y_train = y.iloc[:split_index]
y_test = y.iloc[split_index:]

print("\nTraining rows:", len(X_train))
print("Testing rows:", len(X_test))


# -----------------------------------
# 5. Train Random Forest
# -----------------------------------

model = RandomForestClassifier(
    n_estimators=100,
    max_depth=5,
    random_state=42,
    class_weight="balanced"
)

model.fit(X_train, y_train)

# Save trained model
os.makedirs("models", exist_ok=True)

model_path = r"models\random_forest_model.pkl"
joblib.dump(model, model_path)

print("\nTrained model saved to:")
print(model_path)


# -----------------------------------
# 6. Make predictions
# -----------------------------------

y_pred = model.predict(X_test)


# -----------------------------------
# 7. Calculate performance
# -----------------------------------

accuracy = accuracy_score(y_test, y_pred)

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
# 8. Display results
# -----------------------------------

print("\n-----------------------------------")
print("MODEL RESULTS")
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
# 9. Feature importance
# -----------------------------------

importance = pd.DataFrame({
    "Feature": features,
    "Importance": model.feature_importances_
})

importance = importance.sort_values(
    "Importance",
    ascending=False
)

print("\nFeature Importance:")
print(
    importance.to_string(index=False)
)


# -----------------------------------
# 10. Save predictions
# -----------------------------------

results = df.iloc[split_index:].copy()

results["Predicted_Flood_Risk"] = y_pred

output_path = r"results\classical_model_predictions.csv"

results.to_csv(
    output_path,
    index=False
)

print("\nPredictions saved to:")
print(output_path)

print("\n-----------------------------------")
print("CLASSICAL MODEL TRAINING COMPLETED")
print("-----------------------------------")