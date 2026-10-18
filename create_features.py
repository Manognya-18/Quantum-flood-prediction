import pandas as pd

# -----------------------------------
# 1. Load flood training dataset
# -----------------------------------

input_path = r"data\krishna_flood_training.csv"

df = pd.read_csv(input_path)

# Convert Date
df["Date"] = pd.to_datetime(df["Date"])

# Sort by date
df = df.sort_values("Date").reset_index(drop=True)

print("-----------------------------------")
print("FEATURE ENGINEERING")
print("-----------------------------------")

print("Original rows:", len(df))


# -----------------------------------
# 2. Rainfall features
# -----------------------------------

# Today's rainfall
df["Rainfall_Today"] = df["Rainfall_Total"]

# Previous day's rainfall
df["Rainfall_Previous_Day"] = (
    df["Rainfall_Total"].shift(1)
)

# 3-day accumulated rainfall
df["Rainfall_3Day"] = (
    df["Rainfall_Total"]
    .rolling(window=3)
    .sum()
)

# 7-day accumulated rainfall
df["Rainfall_7Day"] = (
    df["Rainfall_Total"]
    .rolling(window=7)
    .sum()
)


# -----------------------------------
# 3. Discharge features
# -----------------------------------

# Today's discharge
df["Discharge_Today"] = df["Discharge_Mean"]

# Previous day's discharge
df["Discharge_Previous_Day"] = (
    df["Discharge_Mean"].shift(1)
)

# 3-day average discharge
df["Discharge_3Day_Average"] = (
    df["Discharge_Mean"]
    .rolling(window=3)
    .mean()
)

# Discharge change from previous day
df["Discharge_Change"] = (
    df["Discharge_Mean"]
    - df["Discharge_Mean"].shift(1)
)


# -----------------------------------
# 4. Remove rows with insufficient history
# -----------------------------------

# The first 6 rows cannot have a complete
# 7-day rainfall history.

df = df.dropna().reset_index(drop=True)


# -----------------------------------
# 5. Select final features
# -----------------------------------

feature_columns = [
    "Date",

    "Rainfall_Today",
    "Rainfall_Previous_Day",
    "Rainfall_3Day",
    "Rainfall_7Day",

    "Discharge_Today",
    "Discharge_Previous_Day",
    "Discharge_3Day_Average",
    "Discharge_Change",

    "Flood_Risk_Next_Day"
]

final_df = df[feature_columns]


# -----------------------------------
# 6. Save feature dataset
# -----------------------------------

output_path = r"data\krishna_flood_features.csv"

final_df.to_csv(
    output_path,
    index=False
)


# -----------------------------------
# 7. Display results
# -----------------------------------

print("\n-----------------------------------")
print("FEATURE ENGINEERING COMPLETED")
print("-----------------------------------")

print("Final rows:", len(final_df))
print("Final columns:", len(final_df.columns))

print("\nColumns:")
print(final_df.columns.tolist())

print("\nFirst 10 rows:")
print(
    final_df.head(10).to_string(index=False)
)

print("\nTarget distribution:")
print(
    final_df["Flood_Risk_Next_Day"]
    .value_counts()
    .sort_index()
)

print("\nOutput file:")
print(output_path)