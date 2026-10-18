import pandas as pd

rainfall = pd.read_csv(
    r"data\krishna_rainfall_daily.csv"
)

water = pd.read_csv(
    r"data\krishna_water_level_daily.csv"
)

rainfall["Date"] = pd.to_datetime(rainfall["Date"])
water["Date"] = pd.to_datetime(water["Date"])

water_dates = set(water["Date"])

rainfall["Has_Water_Level"] = rainfall["Date"].isin(water_dates)

print("-----------------------------------")
print("WATER LEVEL COVERAGE")
print("-----------------------------------")

print("Total rainfall dates:", len(rainfall))
print(
    "Dates with water level:",
    rainfall["Has_Water_Level"].sum()
)
print(
    "Dates without water level:",
    (~rainfall["Has_Water_Level"]).sum()
)

print("\nWater-level date range:")
print("First:", water["Date"].min().date())
print("Last :", water["Date"].max().date())

print("\nWater-level dates:")
print(
    water["Date"]
    .sort_values()
    .dt.strftime("%Y-%m-%d")
    .to_string(index=False)
)