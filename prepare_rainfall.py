import pandas as pd
from pathlib import Path

# --------------------------------------------------
# 1. File paths
# --------------------------------------------------

input_path = Path(r"data\Rainfall dataset 1.csv")
output_path = Path(r"data\krishna_rainfall_daily.csv")


# --------------------------------------------------
# 2. Load rainfall dataset
# --------------------------------------------------

df = pd.read_csv(input_path)

print("Original rows:", len(df))


# --------------------------------------------------
# 3. Make sure we only use Krishna Basin
# --------------------------------------------------

df["Basin"] = df["Basin"].astype(str).str.strip()

df = df[df["Basin"].str.lower() == "krishna"].copy()

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
    errors="coerce"
)

# Remove rows where timestamp could not be converted
df = df.dropna(
    subset=["Data Acquisition Time"]
)


# --------------------------------------------------
# 6. Convert rainfall column to numeric
# --------------------------------------------------

rainfall_column = "Telemetry Hourly Rainfall (mm)"

df[rainfall_column] = pd.to_numeric(
    df[rainfall_column],
    errors="coerce"
)

# Remove missing rainfall values
df = df.dropna(
    subset=[rainfall_column]
)


# --------------------------------------------------
# 7. Remove invalid negative rainfall
# --------------------------------------------------
negative_count = (df[rainfall_column] < 0).sum()

print("Negative rainfall values:", negative_count)

df = df[df[rainfall_column] >= 0].copy()

print("Rows after removing negative values:", len(df))
# --------------------------------------------------
# 8. Create Date column
# --------------------------------------------------

df["Date"] = df["Data Acquisition Time"].dt.date

# --------------------------------------------------
# 9. Calculate daily rainfall for each station
# --------------------------------------------------

daily_station = (
    df.groupby(
        ["Date", "Station"]
    )[rainfall_column]
    .agg(
        Rainfall_Mean="mean",
        Rainfall_Max="max",
        Rainfall_Total="sum"
    )
    .reset_index()
)
print("\nDaily rainfall by station:")
print(daily_station.head())


# --------------------------------------------------
# 10. Calculate Krishna Basin daily rainfall
# --------------------------------------------------

daily_rainfall = (
    daily_station
    .groupby("Date")
    .agg(
        Rainfall_Mean=("Rainfall_Mean", "mean"),
        Rainfall_Max=("Rainfall_Max", "max"),
        Rainfall_Total=("Rainfall_Total", "sum"),
        Rainfall_Station_Count=("Station", "nunique")
    )
    .reset_index()
)
print("\nKrishna Basin daily rainfall:")
print(daily_rainfall.head())


# --------------------------------------------------
# 11. Save the processed dataset
# --------------------------------------------------

output_path = Path(r"data\krishna_rainfall_daily.csv")

daily_rainfall.to_csv(
    output_path,
    index=False
)

print("\nDaily rainfall dataset saved!")
print("File:", output_path)
print("Rows:", len(daily_rainfall))


# --------------------------------------------------
# 12. Display results
# --------------------------------------------------

print("\n-----------------------------------")
print("Rainfall processing completed!")
print("-----------------------------------")
print("Final rows:", len(daily_rainfall))
print("Output file:", output_path)

print("\nFirst 5 rows:")
print(daily_rainfall.head())