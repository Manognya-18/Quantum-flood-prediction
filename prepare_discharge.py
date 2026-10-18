import pandas as pd
from pathlib import Path

# --------------------------------------------------
# 1. File paths
# --------------------------------------------------

input_path = Path(r"data\river water discharge dataset 3 2001-2025.csv")
output_path = Path(r"data\krishna_discharge_daily.csv")


# --------------------------------------------------
# 2. Load discharge dataset
# --------------------------------------------------

df = pd.read_csv(input_path)

print("Original rows:", len(df))


# --------------------------------------------------
# 3. Filter Krishna Basin
# --------------------------------------------------

df["Basin"] = df["Basin"].astype(str).str.strip()

df = df[
    df["Basin"].str.lower() == "krishna"
].copy()

print("Krishna Basin rows:", len(df))


# --------------------------------------------------
# 4. Remove duplicate Station + Timestamp records
# --------------------------------------------------

before = len(df)

df = df.drop_duplicates(
    subset=["Station", "Data Acquisition Time"]
)

after = len(df)

print("Duplicate rows removed:", before - after)


# --------------------------------------------------
# 5. Convert timestamp
# --------------------------------------------------

df["Data Acquisition Time"] = pd.to_datetime(
    df["Data Acquisition Time"],
    format="%d-%m-%Y %H:%M",
    errors="coerce"
)

invalid_dates = df["Data Acquisition Time"].isna().sum()

print("Invalid dates:", invalid_dates)

df = df.dropna(
    subset=["Data Acquisition Time"]
)


# --------------------------------------------------
# 6. Convert discharge to numeric
# --------------------------------------------------

discharge_column = (
    "Manual Daily River Water Discharge (m3/sec)"
)

df[discharge_column] = pd.to_numeric(
    df[discharge_column],
    errors="coerce"
)

invalid_discharge = df[discharge_column].isna().sum()

print("Invalid discharge values:", invalid_discharge)

df = df.dropna(
    subset=[discharge_column]
)


# --------------------------------------------------
# 7. Remove negative discharge
# --------------------------------------------------

negative_count = (
    df[discharge_column] < 0
).sum()

print("Negative discharge values:", negative_count)

df = df[
    df[discharge_column] >= 0
].copy()

print(
    "Rows after removing negative discharge:",
    len(df)
)


# --------------------------------------------------
# 8. Create Date column
# --------------------------------------------------

df["Date"] = (
    df["Data Acquisition Time"].dt.date
)


# --------------------------------------------------
# 9. Create daily discharge features
# --------------------------------------------------

daily_discharge = (
    df.groupby("Date")
      .agg(
          Discharge_Mean=(
              discharge_column,
              "mean"
          ),
          Discharge_Max=(
              discharge_column,
              "max"
          ),
          Discharge_Station_Count=(
              "Station",
              "nunique"
          )
      )
      .reset_index()
)


# --------------------------------------------------
# 10. Save cleaned discharge dataset
# --------------------------------------------------

daily_discharge.to_csv(
    output_path,
    index=False
)


# --------------------------------------------------
# 11. Display results
# --------------------------------------------------

print("\n-----------------------------------")
print("Discharge processing completed!")
print("-----------------------------------")

print("Final rows:", len(daily_discharge))
print("Output file:", output_path)

print("\nFirst 5 rows:")
print(daily_discharge.head())