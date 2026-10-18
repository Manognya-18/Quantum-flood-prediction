import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
import joblib

# -----------------------------------------
# PAGE CONFIGURATION
# -----------------------------------------

st.set_page_config(
    page_title="Quantum Flood Prediction",
    page_icon="🌊",
    layout="wide"
)

# -----------------------------------------
# TITLE
# -----------------------------------------

st.title("🌊 Quantum Flood Prediction & Disaster Response System")

st.subheader("Krishna Basin Flood-Risk Monitoring")

st.write(
    "A data-driven flood forecasting system using "
    "classical and quantum machine learning."
)

st.divider()

# -----------------------------------------
# SIDEBAR
# -----------------------------------------

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Go to",
    [
        "🏠 Overview",
        "🌧️ Data Analysis",
        "🤖 Flood Prediction",
        "⚛️ Quantum ML",
        "📊 Model Comparison",
        "🚨 Early Warning",
        "⚛️ Sensor Optimization",
        "🛟 Disaster Response",
        "🚀 Future Scope"
    ]
)

# -----------------------------------------
# OVERVIEW
# -----------------------------------------

if page == "🏠 Overview":

    st.header("Project Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Training Samples",
            "207"
        )

    with col2:
        st.metric(
            "Testing Samples",
            "52"
        )

    with col3:
        st.metric(
            "Quantum Features",
            "4"
        )

    with col4:
        st.metric(
            "Qubits",
            "4"
        )

    st.divider()

    st.subheader("Project Pipeline")

    st.write("""
    Historical Data
    ↓
    Data Cleaning
    ↓
    Daily Aggregation
    ↓
    Feature Engineering
    ↓
    Flood-Risk Classification
    ↓
    Classical + Quantum ML
    ↓
    Model Comparison
    """)

    st.subheader("Completed Components")

    st.success("✅ Rainfall data cleaning")
    st.success("✅ Discharge data cleaning")
    st.success("✅ Dataset processing")
    st.success("✅ Feature engineering")
    st.success("✅ Flood-risk target creation")
    st.success("✅ Random Forest model")
    st.success("✅ QSVC quantum model")
    st.success("✅ VQC quantum model")
    st.success("✅ Model comparison")

    st.subheader("Recently Completed")

    st.success("✅ QAOA sensor-placement optimization")
    st.success("✅ Flood early-warning classification")
    st.success("✅ Risk visualization")
    st.success("✅ Disaster-response recommendations")
    st.success("✅ Risk distribution analysis")

    st.info(
        "The project has progressed from the 40% prototype "
        "to an integrated flood-risk monitoring prototype."
    )

# -----------------------------------------
# DATA ANALYSIS
# -----------------------------------------

elif page == "🌧️ Data Analysis":

    st.header("🌧️ Environmental Data Analysis")

    # Load rainfall data
    rainfall_path = r"data\krishna_rainfall_daily.csv"

    try:
        rainfall = pd.read_csv(rainfall_path)

        st.subheader("Rainfall Data")

        st.write(
            f"Total rainfall records: {len(rainfall)}"
        )

        st.dataframe(
            rainfall.head(10),
            use_container_width=True
        )

        # Detect rainfall column
        rainfall_columns = [
            col for col in rainfall.columns
            if "rainfall" in col.lower()
        ]

        if rainfall_columns:

            rainfall_col = rainfall_columns[0]

            st.subheader("Daily Rainfall")

            fig, ax = plt.subplots()

            ax.plot(
                rainfall[rainfall_col]
            )

            ax.set_xlabel("Day")
            ax.set_ylabel("Rainfall")
            ax.set_title("Daily Rainfall")

            st.pyplot(fig)

    except FileNotFoundError:

        st.error(
            "Rainfall dataset not found."
        )

    st.divider()

    # -------------------------------------
    # DISCHARGE
    # -------------------------------------

    discharge_path = (
        r"data\krishna_discharge_daily.csv"
    )

    try:

        discharge = pd.read_csv(
            discharge_path
        )

        st.subheader("💧 Discharge Data")

        st.write(
            f"Total discharge records: {len(discharge)}"
        )

        st.dataframe(
            discharge.head(10),
            use_container_width=True
        )

    except FileNotFoundError:

        st.error(
            "Discharge dataset not found."
        )

# -----------------------------------------
# FLOOD PREDICTION
# -----------------------------------------

elif page == "🤖 Flood Prediction":

    st.header("🤖 Flood Risk Prediction")

    st.write(
        "Enter the environmental conditions to generate "
        "a next-day flood-risk prediction using the trained "
        "Random Forest model."
    )

    # Load trained model
    model_path = r"models\random_forest_model.pkl"

    try:

        model = joblib.load(model_path)

        st.success("✅ Trained Random Forest model loaded successfully.")

        st.divider()

        st.subheader("🌧️ Rainfall Features")

        col1, col2 = st.columns(2)

        with col1:

            rainfall_today = st.number_input(
                "Rainfall Today",
                min_value=0.0,
                value=10.0,
                help="Rainfall recorded today."
            )

            rainfall_previous_day = st.number_input(
                "Rainfall Previous Day",
                min_value=0.0,
                value=10.0,
                help="Rainfall recorded on the previous day."
            )

        with col2:

            rainfall_3day = st.number_input(
                "Rainfall 3-Day",
                min_value=0.0,
                value=30.0,
                help="Recent 3-day rainfall measure."
            )

            rainfall_7day = st.number_input(
                "Rainfall 7-Day",
                min_value=0.0,
                value=50.0,
                help="Recent 7-day rainfall measure."
            )

        st.divider()

        st.subheader("💧 River Discharge Features")

        col1, col2 = st.columns(2)

        with col1:

            discharge_today = st.number_input(
                "Discharge Today",
                min_value=0.0,
                value=500.0,
                help="Current river discharge."
            )

            discharge_previous_day = st.number_input(
                "Discharge Previous Day",
                min_value=0.0,
                value=500.0,
                help="Previous day's river discharge."
            )

        with col2:

            discharge_3day_average = st.number_input(
                "Discharge 3-Day Average",
                min_value=0.0,
                value=500.0,
                help="Average discharge over the recent 3-day period."
            )

            discharge_change = st.number_input(
                "Discharge Change",
                value=0.0,
                help="Change in discharge compared with the previous day."
            )

        st.divider()

        if st.button(
            "🔍 Analyze Flood Risk",
            use_container_width=True
        ):

            # Create input DataFrame
            input_data = pd.DataFrame({
                "Rainfall_Today": [rainfall_today],
                "Rainfall_Previous_Day": [rainfall_previous_day],
                "Rainfall_3Day": [rainfall_3day],
                "Rainfall_7Day": [rainfall_7day],
                "Discharge_Today": [discharge_today],
                "Discharge_Previous_Day": [discharge_previous_day],
                "Discharge_3Day_Average": [discharge_3day_average],
                "Discharge_Change": [discharge_change]
            })

            # Make prediction
            prediction = model.predict(input_data)[0]

            # Get prediction probability
            probabilities = model.predict_proba(input_data)[0]

            st.divider()

            st.subheader("🚨 Flood Risk Prediction")

            if prediction == 1:

                st.error(
                    "🔴 HIGH FLOOD RISK — Next-day flood risk detected."
                )

                st.write(
                    f"Probability of High Flood Risk: "
                    f"{probabilities[1] * 100:.2f}%"
                )

            else:

                st.success(
                    "🟢 NORMAL — No high flood risk predicted "
                    "for the next day."
                )

                st.write(
                    f"Probability of High Flood Risk: "
                    f"{probabilities[1] * 100:.2f}%"
                )

            st.divider()

            st.subheader("📋 Input Features Used for Prediction")

            st.dataframe(
                input_data,
                use_container_width=True,
                hide_index=True
            )

    except FileNotFoundError:

        st.error(
            "❌ Trained Random Forest model not found."
        )

        st.write(
            "Please run train_classical_model.py first "
            "to create models\\random_forest_model.pkl."
        )


# -----------------------------------------
# QUANTUM ML
# -----------------------------------------

elif page == "⚛️ Quantum ML":

    st.header("⚛️ Quantum Machine Learning")

    st.write(
        "Our quantum models use four environmental "
        "features encoded into a four-qubit system."
    )

    st.subheader("Quantum Features")

    features = [
        "Rainfall_Today",
        "Rainfall_7Day",
        "Discharge_Today",
        "Discharge_Change"
    ]

    for i, feature in enumerate(features):

        st.write(
            f"**Qubit {i}:** {feature}"
        )

    st.divider()

    st.subheader("Quantum Architecture")

    st.code("""
Rainfall Today
       ↓
Rainfall 7-Day
       ↓
Discharge Today
       ↓
Discharge Change
       ↓
   4 Qubits
       ↓
Quantum Feature Map
       ↓
QSVC / VQC
       ↓
Flood Risk
""")

    st.info(
        "This is a conceptual representation of "
        "the quantum machine-learning pipeline."
    )

    st.subheader("QSVC")

    st.write(
        "Quantum Support Vector Classifier using "
        "a Fidelity Quantum Kernel."
    )

    st.subheader("VQC")

    st.write(
        "Variational Quantum Classifier using a "
        "trainable variational circuit."
    )

# -----------------------------------------
# MODEL COMPARISON
# -----------------------------------------

elif page == "📊 Model Comparison":

    st.header("📊 Model Performance Comparison")

    results = pd.DataFrame({
        "Model": [
            "Random Forest",
            "QSVC",
            "VQC"
        ],

        "Accuracy": [
            86.54,
            67.31,
            53.85
        ],

        "Precision": [
            71.43,
            35.71,
            28.00
        ],

        "Recall": [
            76.92,
            38.46,
            53.85
        ],

        "F1 Score": [
            74.07,
            37.04,
            36.84
        ]
    })

    st.dataframe(
        results,
        use_container_width=True
    )

    st.divider()

    st.subheader("Accuracy Comparison")

    chart_data = results.set_index(
        "Model"
    )["Accuracy"]

    st.bar_chart(chart_data)

    st.subheader("Precision Comparison")

    chart_data = results.set_index(
        "Model"
    )["Precision"]

    st.bar_chart(chart_data)

    st.subheader("Recall Comparison")

    chart_data = results.set_index(
        "Model"
    )["Recall"]

    st.bar_chart(chart_data)

    st.subheader("F1 Score Comparison")

    chart_data = results.set_index(
        "Model"
    )["F1 Score"]

    st.bar_chart(chart_data)

    st.divider()

    st.success(
        "🏆 Current best-performing model: "
        "Random Forest"
    )

    st.write(
        "Random Forest currently provides the strongest "
        "performance on the available dataset, while "
        "QSVC and VQC demonstrate the feasibility of "
        "Quantum Machine Learning."
    )

# -----------------------------------------
# EARLY WARNING
# -----------------------------------------

elif page == "🚨 Early Warning":

    st.header("🚨 Flood Early Warning System")

    warning_path = r"data\flood_early_warning.csv"

    try:

        warning_df = pd.read_csv(warning_path)

        warning_df["Date"] = pd.to_datetime(
            warning_df["Date"]
        )

        latest = warning_df.sort_values(
            "Date"
        ).iloc[-1]

        st.subheader("Current Flood Status")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Latest Date",
                latest["Date"].strftime("%Y-%m-%d")
            )

        with col2:
            st.metric(
                "Discharge",
                f'{latest["Discharge"]:.2f}'
            )

        with col3:
            st.metric(
                "Risk Ratio",
                f'{latest["Risk_Ratio"]:.3f}'
            )

        with col4:
            st.metric(
                "Warning Level",
                latest["Warning_Level"]
            )

        st.divider()

        level = latest["Warning_Level"]

        if level == "NORMAL":

            st.success(
                "NORMAL — Continue routine monitoring."
            )

        elif level == "WATCH":

            st.info(
                "WATCH — Increase monitoring and review vulnerable areas."
            )

        elif level == "WARNING":

            st.warning(
                "WARNING — Prepare response teams and emergency resources."
            )

        elif level == "CRITICAL":

            st.error(
                "CRITICAL — High-priority monitoring and emergency "
                "procedures should be considered."
            )

        st.divider()

        st.subheader("Historical Discharge and Risk")

        chart_df = warning_df[
            ["Date", "Discharge"]
        ].copy()

        chart_df = chart_df.set_index("Date")

        st.line_chart(
            chart_df
        )

        st.subheader("📊 Risk Distribution")

        risk_counts = warning_df[
            "Warning_Level"
        ].value_counts().reindex(
            ["NORMAL", "WATCH", "WARNING", "CRITICAL"],
            fill_value=0
        )

        st.bar_chart(
            risk_counts
        )
        st.caption(
            "The warning levels are project-defined analytical "
            "categories based on the selected discharge threshold."
        )

    except FileNotFoundError:

        st.error(
            "flood_early_warning.csv not found. "
            "Run Step 19 first."
        )

# -----------------------------------------
# SENSOR OPTIMIZATION
# -----------------------------------------

elif page == "⚛️ Sensor Optimization":

    st.header("⚛️ Quantum Sensor-Placement Optimization")

    st.write(
        """
        QAOA is used to select a limited number of high-priority
        candidate scenarios for flood-monitoring resource placement.
        """
    )

    selected_path = (
        r"optimization\quantum_selected_sensors.csv"
    )

    visualization_path = (
        r"optimization\sensor_placement_visualization.png"
    )

    try:

        selected = pd.read_csv(
            selected_path
        )

        st.subheader("QAOA Selected Candidates")

        st.dataframe(
            selected,
            use_container_width=True,
            hide_index=True
        )

        st.divider()

        if os.path.exists(visualization_path):

            st.image(
                visualization_path,
                caption="Risk-based candidate importance and QAOA selection"
            )

        st.info(
            """
            KR-01 to KR-06 are risk-based candidate scenarios generated
            from the available basin-level data. They are not physical
            geographic sensor locations.
            """
        )

    except FileNotFoundError:

        st.error(
            "Quantum sensor optimization results not found. "
            "Run Steps 14–18 first."
        )

# -----------------------------------------
# DISASTER RESPONSE
# -----------------------------------------

elif page == "🛟 Disaster Response":

    st.header("🛟 Disaster Response Recommendations")

    warning_path = r"data\flood_early_warning.csv"

    try:

        warning_df = pd.read_csv(
            warning_path
        )

        warning_df["Date"] = pd.to_datetime(
            warning_df["Date"]
        )

        latest = warning_df.sort_values(
            "Date"
        ).iloc[-1]

        level = latest["Warning_Level"]

        st.subheader("Current Risk Level")

        st.metric(
            "Warning Level",
            level
        )

        st.divider()

        st.subheader("Recommended Response")

        if level == "NORMAL":

            st.success(
                "Routine monitoring — continue normal monitoring "
                "of rainfall and discharge."
            )

        elif level == "WATCH":

            st.info(
                "Increase monitoring — increase monitoring frequency "
                "and review vulnerable areas."
            )

        elif level == "WARNING":

            st.warning(
                "Prepare response — prepare emergency teams, "
                "communication channels and evacuation resources."
            )

        elif level == "CRITICAL":

            st.error(
                "High-priority response — activate high-priority "
                "monitoring and follow applicable local emergency "
                "procedures."
            )

        st.divider()

        st.subheader("Response Framework")

        response_data = pd.DataFrame({
            "Risk Level": [
                "NORMAL",
                "WATCH",
                "WARNING",
                "CRITICAL"
            ],
            "Recommended Action": [
                "Routine monitoring",
                "Increase monitoring",
                "Prepare response resources",
                "High-priority response"
            ]
        })

        st.dataframe(
            response_data,
            use_container_width=True,
            hide_index=True
        )

    except FileNotFoundError:

        st.error(
            "Flood early-warning data not found. "
            "Run Step 19 first."
        )

# -----------------------------------------
# FUTURE SCOPE
# -----------------------------------------

elif page == "🚀 Future Scope":

    st.header("🚀 Future Development")

    st.subheader("Current Phase — Completed")

    st.success("✅ Historical data processing")
    st.success("✅ Flood-risk classification")
    st.success("✅ Random Forest")
    st.success("✅ QSVC")
    st.success("✅ VQC")
    st.success("✅ Model comparison")

    st.divider()

    st.subheader("Current Prototype — Completed")

    st.success("✅ Historical data processing")
    st.success("✅ Flood-risk classification")
    st.success("✅ Random Forest")
    st.success("✅ QSVC")
    st.success("✅ VQC")
    st.success("✅ QAOA sensor optimization")
    st.success("✅ Early warning system")
    st.success("✅ Risk distribution analysis")
    st.success("✅ Disaster response recommendations")
    st.success("✅ Integrated Streamlit dashboard")

    st.divider()

    st.subheader("Future Development")

    st.info("📡 Real-time telemetry integration")
    st.info("🗺️ Geographic station-level sensor mapping")
    st.info("🌊 Water-level data integration")
    st.info("📱 Automated alert notification")
    st.info("☁️ Cloud deployment")


   
    st.divider()

    st.subheader("Long-Term Vision")

    st.info(
        "IoT sensor integration → Real-time data → "
        "Flood prediction → Early warning → "
        "Disaster response"
    )