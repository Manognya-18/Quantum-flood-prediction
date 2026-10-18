import pandas as pd

# Load cleaned discharge dataset
discharge = pd.read_csv(
    r"data\krishna_discharge_daily.csv"
)

# Convert date
discharge["Date"] = pd.to_datetime(
    discharge["Date"]
)

# Display columns
print("-----------------------------------")
print("DISCHARGE DATA")
print("-----------------------------------")

print("Rows:", len(discharge))
print("Columns:")
print(discharge.columns.tolist())

# Find the discharge column automatically
print("\nFirst 5 rows:")
print(discharge.head().to_string(index=False))

# Show numerical statistics
print("\nDischarge statistics:")

print(
    discharge.describe().to_string()
)