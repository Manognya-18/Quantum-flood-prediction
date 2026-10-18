import pandas as pd
from pathlib import Path

# -------------------------------------------------
# STEP 21: AUTOMATIC FLOOD ALERT GENERATION
# -------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

INPUT_FILE = BASE_DIR / "data" / "flood_early_warning.csv"
OUTPUT_FILE = BASE_DIR / "data" / "latest_flood_alert.txt"

print("\nAUTOMATIC FLOOD ALERT GENERATION")
print("---------------------------------")

# -------------------------------------------------
# LOAD EARLY WARNING DATA
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
# GET LATEST RECORD
# -------------------------------------------------

latest = df.sort_values("Date").iloc[-1]

latest_date = latest["Date"]
latest_discharge = latest["Discharge"]
latest_ratio = latest["Risk_Ratio"]
warning_level = latest["Warning_Level"]

# -------------------------------------------------
# ALERT MESSAGE
# -------------------------------------------------

if warning_level == "NORMAL":

    action = (
        "Continue routine monitoring. "
        "No immediate flood-response action is indicated "
        "by this threshold-based alert."
    )

elif warning_level == "WATCH":

    action = (
        "Increase monitoring frequency and observe "
        "rainfall and discharge trends."
    )

elif warning_level == "WARNING":

    action = (
        "Prepare for possible flood conditions and "
        "increase disaster-response readiness."
    )

elif warning_level == "CRITICAL":

    action = (
        "Initiate high-priority monitoring and "
        "follow applicable local flood-response procedures."
    )

else:

    action = "Review the latest data and warning classification."

# -------------------------------------------------
# CREATE ALERT
# -------------------------------------------------

alert = f"""
==================================================
       KRISHNA BASIN FLOOD EARLY WARNING
==================================================

Latest Data Date : {latest_date.strftime('%Y-%m-%d')}

Maximum Discharge: {latest_discharge:.3f}

Risk Ratio       : {latest_ratio:.3f}

Alert Level      : {warning_level}

Recommended Action:
{action}

==================================================
Note:
This is a project-level analytical alert generated
from the available discharge dataset and the
project-defined threshold of 736.23.
It is not an official government flood warning.
==================================================
"""

# -------------------------------------------------
# DISPLAY ALERT
# -------------------------------------------------

print(alert)

# -------------------------------------------------
# SAVE ALERT
# -------------------------------------------------

with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
    file.write(alert)

print("Alert saved to:")
print(OUTPUT_FILE)

print("\nSTEP 21 COMPLETED")