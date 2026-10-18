import pandas as pd
from pathlib import Path

# -------------------------------------------------
# STEP 22: DISASTER RESPONSE RECOMMENDATIONS
# -------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

INPUT_FILE = BASE_DIR / "data" / "flood_early_warning.csv"
OUTPUT_FILE = BASE_DIR / "data" / "disaster_response_plan.csv"

print("\nDISASTER RESPONSE RECOMMENDATION SYSTEM")
print("----------------------------------------")

# -------------------------------------------------
# LOAD WARNING DATA
# -------------------------------------------------

df = pd.read_csv(INPUT_FILE)

df["Date"] = pd.to_datetime(
    df["Date"],
    errors="coerce"
)

df["Discharge"] = pd.to_numeric(
    df["Discharge"],
    errors="coerce"
)

df["Risk_Ratio"] = pd.to_numeric(
    df["Risk_Ratio"],
    errors="coerce"
)

df = df.dropna(
    subset=["Date", "Discharge", "Risk_Ratio"]
)

# -------------------------------------------------
# RESPONSE LOGIC
# -------------------------------------------------

def get_response(level):

    if level == "NORMAL":
        return (
            "Routine monitoring",
            "Continue normal monitoring of rainfall and river discharge."
        )

    elif level == "WATCH":
        return (
            "Increase monitoring",
            "Increase monitoring frequency and check vulnerable areas."
        )

    elif level == "WARNING":
        return (
            "Prepare response",
            "Prepare emergency teams, communication channels and evacuation resources."
        )

    elif level == "CRITICAL":
        return (
            "High-priority response",
            "Activate high-priority monitoring and follow applicable local emergency procedures."
        )

    else:
        return (
            "Review data",
            "Check the latest measurements and warning classification."
        )


# -------------------------------------------------
# GENERATE RESPONSE PLAN
# -------------------------------------------------

responses = df["Warning_Level"].apply(get_response)

df["Response_Level"] = responses.apply(
    lambda x: x[0]
)

df["Recommended_Action"] = responses.apply(
    lambda x: x[1]
)

# -------------------------------------------------
# DISPLAY LATEST RESPONSE
# -------------------------------------------------

latest = df.sort_values("Date").iloc[-1]

print("\nLATEST FLOOD RESPONSE STATUS")
print("----------------------------")

print("Date:", latest["Date"].strftime("%Y-%m-%d"))
print("Discharge:", latest["Discharge"])
print("Warning Level:", latest["Warning_Level"])
print("Response Level:", latest["Response_Level"])
print("Recommended Action:")
print(latest["Recommended_Action"])

# -------------------------------------------------
# SAVE
# -------------------------------------------------

df[
    [
        "Date",
        "Discharge",
        "Risk_Ratio",
        "Warning_Level",
        "Response_Level",
        "Recommended_Action"
    ]
].to_csv(
    OUTPUT_FILE,
    index=False
)

print("\nResponse plan saved to:")
print(OUTPUT_FILE)

print("\nSTEP 22 COMPLETED")