import pandas as pd
from pathlib import Path

# --------------------------------------------------
# 1. File paths
# --------------------------------------------------

input_path = Path(r"data\river_water_level.csv")
output_path = Path(r"data\krishna_water_level_daily.csv")


# --------------------------------------------------
# 2. Load dataset
# --------------------------------------------------

df = pd.read_csv(input_path)

print("Original rows:", len(df))


# --------------------------------------------------
# 3. Keep only Krishna Basin
# --------------------------------------------------

df["Basin"] = df["Basin"].astype(str).str.strip()

df = df[
    df["Basin"].str.lower() == "krishna"
].copy()

print("Krishna Basin rows:", len(df))


# --------------------------------------------------
# 4. Keep only required columns
# --------------------------------------------------

df = df[
    [
        "Station",
        "River",
        "Basin",
        "Latitude",
        "Longitude",
        "Data Acquisition Time",
        "River Water Level Manual Hourly (meter)"
    ]
].copy()


# --------------------------------------------------
# 5. Convert date correctly
# --------------------------------------------------

df["Date"] = pd.to_datetime(
    df["Data Acquisition Time"],
    format="%d-%m-%Y %H:%M",
    errors="coerce"
)

invalid_dates = df["Date"].isna().sum()

print("Invalid dates:", invalid_dates)


# --------------------------------------------------
# 6. Convert water level to numeric
# --------------------------------------------------

water_col = "River Water Level Manual Hourly (meter)"

df["Water_Level"] = pd.to_numeric(
    df[water_col],
    errors="coerce"
)

invalid_water = df["Water_Level"].isna().sum()

print("Invalid water-level values:", invalid_water)


# --------------------------------------------------
# 7. Remove invalid records
# --------------------------------------------------

df = df.dropna(
    subset=["Date", "Water_Level"]
).copy()


# --------------------------------------------------
# 8. Remove duplicate records
# --------------------------------------------------

before_duplicates = len(df)

df = df.drop_duplicates(
    subset=[
        "Station",
        "Date"
    ]
)

duplicates_removed = (
    before_duplicates - len(df)
)

print("Duplicate rows removed:", duplicates_removed)


# --------------------------------------------------
# 9. Remove impossible negative water levels
# --------------------------------------------------

negative_values = (
    df["Water_Level"] < 0
).sum()

print(
    "Negative water-level values:",
    negative_values
)

df = df[
    df["Water_Level"] >= 0
].copy()


# --------------------------------------------------
# 10. Create date-only column
# --------------------------------------------------

df["Date"] = df["Date"].dt.date

df["Date"] = pd.to_datetime(
    df["Date"]
)


# --------------------------------------------------
# 11. Create daily water-level dataset
# --------------------------------------------------

daily_water = (
    df.groupby("Date")
    .agg(
        Water_Level_Mean=("Water_Level", "mean"),
        Water_Level_Max=("Water_Level", "max"),
        Water_Level_Min=("Water_Level", "min"),
        Water_Level_Station_Count=("Station", "nunique")
    )
    .reset_index()
)


# --------------------------------------------------
# 12. Sort by date
# --------------------------------------------------

daily_water = daily_water.sort_values(
    "Date"
).reset_index(drop=True)


# --------------------------------------------------
# 13. Save cleaned dataset
# --------------------------------------------------

daily_water.to_csv(
    output_path,
    index=False
)


# --------------------------------------------------
# 14. Display results
# --------------------------------------------------

print("\n-----------------------------------")
print("WATER LEVEL PROCESSING COMPLETED!")
print("-----------------------------------")

print("Final rows:", len(daily_water))

print("Output file:")
print(output_path)

print("\nFirst 10 rows:")
print(
    daily_water.head(10).to_string(index=False)
)