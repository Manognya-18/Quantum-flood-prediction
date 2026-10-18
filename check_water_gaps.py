import pandas as pd

water = pd.read_csv(
    r"data\krishna_water_level_daily.csv"
)

water["Date"] = pd.to_datetime(water["Date"])

water = water.sort_values("Date")

water["Gap_Days"] = (
    water["Date"].diff().dt.days
)

print("-----------------------------------")
print("WATER LEVEL DATE GAPS")
print("-----------------------------------")

print("Total records:", len(water))

print("\nGap statistics:")
print(water["Gap_Days"].describe())

print("\nLargest gaps:")

print(
    water[
        ["Date", "Gap_Days"]
    ]
    .sort_values("Gap_Days", ascending=False)
    .head(20)
    .to_string(index=False)
)