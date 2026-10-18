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

print("-----------------------------------")
print("DATASET DATE RANGES")
print("-----------------------------------")

print(
    "Rainfall:",
    rainfall["Date"].min().date(),
    "to",
    rainfall["Date"].max().date()
)

print(
    "Discharge:",
    discharge["Date"].min().date(),
    "to",
    discharge["Date"].max().date()
)

print(
    "Water Level:",
    water["Date"].min().date(),
    "to",
    water["Date"].max().date()
)