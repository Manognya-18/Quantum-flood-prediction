import pandas as pd

# Load the merged rainfall + discharge dataset
input_path = r"data\krishna_rainfall_discharge.csv"

df = pd.read_csv(input_path)

# Convert Date
df["Date"] = pd.to_datetime(df["Date"])

print("-----------------------------------")
print("FLOOD TARGET CREATION")
print("-----------------------------------")

print("Rows:", len(df))
print("Columns:")
print(df.columns.tolist())

# -----------------------------------
# Calculate 90th percentile
# -----------------------------------

threshold = df["Discharge_Mean"].quantile(0.90)

print("\n90th Percentile Discharge:")
print(threshold)

# -----------------------------------
# Create current high-flow label
# -----------------------------------

df["Flood_Risk"] = (
    df["Discharge_Mean"] >= threshold
).astype(int)

# -----------------------------------
# Create NEXT-DAY target
# -----------------------------------

df["Flood_Risk_Next_Day"] = (
    df["Flood_Risk"].shift(-1)
)

# Remove final row because it has no next-day target
df = df.dropna(
    subset=["Flood_Risk_Next_Day"]
)

df["Flood_Risk_Next_Day"] = (
    df["Flood_Risk_Next_Day"].astype(int)
)

# -----------------------------------
# Save dataset
# -----------------------------------

output_path = r"data\krishna_flood_training.csv"

df.to_csv(
    output_path,
    index=False
)

# -----------------------------------
# Results
# -----------------------------------

print("\n-----------------------------------")
print("FLOOD TARGET CREATED")
print("-----------------------------------")

print("Flood threshold:", threshold)

print(
    "High-flow days:",
    df["Flood_Risk"].sum()
)

print(
    "Normal-flow days:",
    (df["Flood_Risk"] == 0).sum()
)

print("\nNext-day target distribution:")

print(
    df["Flood_Risk_Next_Day"]
    .value_counts()
    .sort_index()
)

print("\nFinal rows:", len(df))

print("\nOutput file:")
print(output_path)

print("\nFirst 10 rows:")
print(
    df.head(10).to_string(index=False)
)