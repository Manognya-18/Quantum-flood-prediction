import pandas as pd

rainfall = pd.read_csv(
    r"data\krishna_rainfall_daily.csv"
)

discharge = pd.read_csv(
    r"data\krishna_discharge_daily.csv"
)

water = pd.read_csv(
    r"data\krishna_water_level_daily.csv"
)

rainfall["Date"] = pd.to_datetime(rainfall["Date"])
discharge["Date"] = pd.to_datetime(discharge["Date"])
water["Date"] = pd.to_datetime(water["Date"])

common = (
    set(rainfall["Date"])
    & set(discharge["Date"])
    & set(water["Date"])
)

result = water[
    water["Date"].isin(common)
].sort_values("Date")

print("-----------------------------------")
print("COMMON WATER-LEVEL RECORDS")
print("-----------------------------------")

print("Number of common dates:", len(result))

print("\nAll common dates:")
print(result.to_string(index=False))