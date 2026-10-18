import pandas as pd

from sklearn.preprocessing import MinMaxScaler


# -----------------------------------
# 1. Load feature dataset
# -----------------------------------

input_path = r"data\krishna_flood_features.csv"

df = pd.read_csv(input_path)

df["Date"] = pd.to_datetime(df["Date"])

df = df.sort_values("Date").reset_index(drop=True)


print("-----------------------------------")
print("QUANTUM DATA PREPARATION")
print("-----------------------------------")

print("Total rows:", len(df))


# -----------------------------------
# 2. Select 4 quantum features
# -----------------------------------

quantum_features = [
    "Rainfall_Today",
    "Rainfall_7Day",
    "Discharge_Today",
    "Discharge_Change"
]

target = "Flood_Risk_Next_Day"


# -----------------------------------
# 3. Extract X and y
# -----------------------------------

X = df[quantum_features]

y = df[target]


# -----------------------------------
# 4. Time-based train/test split
# -----------------------------------

split_index = int(len(df) * 0.80)

X_train = X.iloc[:split_index].copy()
X_test = X.iloc[split_index:].copy()

y_train = y.iloc[:split_index].copy()
y_test = y.iloc[split_index:].copy()


print("\nTraining rows:", len(X_train))
print("Testing rows:", len(X_test))


# -----------------------------------
# 5. Scale the features
# -----------------------------------

scaler = MinMaxScaler(
    feature_range=(0, 3.14159)
)

X_train_scaled = scaler.fit_transform(X_train)

X_test_scaled = scaler.transform(X_test)


# -----------------------------------
# 6. Convert back to DataFrames
# -----------------------------------

X_train_scaled = pd.DataFrame(
    X_train_scaled,
    columns=quantum_features
)

X_test_scaled = pd.DataFrame(
    X_test_scaled,
    columns=quantum_features
)


# -----------------------------------
# 7. Save prepared quantum data
# -----------------------------------

train_data = X_train_scaled.copy()

train_data["Flood_Risk_Next_Day"] = (
    y_train.values
)

test_data = X_test_scaled.copy()

test_data["Flood_Risk_Next_Day"] = (
    y_test.values
)


train_path = r"data\quantum_train.csv"

test_path = r"data\quantum_test.csv"


train_data.to_csv(
    train_path,
    index=False
)

test_data.to_csv(
    test_path,
    index=False
)


# -----------------------------------
# 8. Display results
# -----------------------------------

print("\n-----------------------------------")
print("QUANTUM DATA PREPARATION COMPLETED")
print("-----------------------------------")

print("\nQuantum features:")
print(quantum_features)

print("\nTraining data:")
print(train_data.head().to_string(index=False))

print("\nTesting data:")
print(test_data.head().to_string(index=False))

print("\nTraining target distribution:")
print(
    train_data[
        "Flood_Risk_Next_Day"
    ].value_counts().sort_index()
)

print("\nTesting target distribution:")
print(
    test_data[
        "Flood_Risk_Next_Day"
    ].value_counts().sort_index()
)

print("\nFiles created:")
print(train_path)
print(test_path)