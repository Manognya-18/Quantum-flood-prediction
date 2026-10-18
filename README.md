# 🌊 Quantum Flood Prediction & Disaster Early Warning System

## 📌 Project Overview

Floods can cause severe damage to human lives, infrastructure, agriculture, and the environment. Early prediction and effective disaster preparedness can help reduce these impacts.

This project explores the use of **Machine Learning, Quantum Machine Learning, and quantum optimization** to support flood prediction and sensor placement for disaster preparedness.

The prototype uses rainfall and river discharge data from the Krishna River basin to study flood prediction and identify promising sensor locations under a limited budget.

## 🎯 Objectives

- Analyze rainfall and river discharge data.
- Build a classical Machine Learning model for flood prediction.
- Explore Quantum Machine Learning using Qiskit.
- Optimize sensor placement using the Quantum Approximate Optimization Algorithm (QAOA).
- Compare quantum-based approaches with classical methods.

## 🛠️ Technologies Used

- Python
- Pandas and NumPy
- Scikit-learn
- Qiskit
- Quantum Machine Learning
- QAOA (Quantum Approximate Optimization Algorithm)
- Streamlit (for the dashboard, if implemented)
- Matplotlib and Seaborn (if used for visualization)

## ⚙️ Project Workflow

1. Collect and preprocess rainfall and river discharge data.
2. Prepare features for flood prediction.
3. Train and evaluate a classical Machine Learning model.
4. Experiment with Quantum Machine Learning using Qiskit.
5. Formulate a sensor placement optimization problem.
6. Compare QAOA-based sensor selection with exhaustive classical optimization.
7. Visualize the results using a dashboard, if implemented.

## 📊 Model Evaluation

The current prototype produced the following results on the test dataset:

| Metric | Classical ML Baseline |
|---|---:|
| Accuracy | 86.54% |
| Precision | 71.43% |
| Recall | 76.92% |
| F1-score | 74.07% |

Quantum model performance is evaluated separately because the current experiments show that it does not consistently outperform the classical baseline.

These results are experimental and do not represent a validated operational flood warning system.

## ⚛️ Sensor Placement Optimization

The project uses QAOA to explore sensor placement under a budget constraint.

In the current experiment:

- Sensor budget: 3 locations
- QAOA-selected locations: S2, S3, S5
- Exhaustive classical selection: S2, S3, S5
- Both methods selected the same locations in this experiment.

This demonstrates agreement between the optimization approaches for the tested configuration; it does not establish quantum advantage.

## 📁 Project Structure

```text
Quantum Flood Project/
├── data/
│   ├── krishna_rainfall_daily.csv
│   └── krishna_discharge_daily.csv
├── optimization/
│   ├── sensor_locations.csv
│   └── quantum_vs_classical_sensor_placement.csv
├── results/
│   └── quantum_model_predictions.csv
├── prepare_rainfall.py
├── train_vqc_model.py
├── README.md
└── requirements.txt
```

Update this structure to match the files actually present in your repository.

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/quantum-flood-prediction.git
cd quantum-flood-prediction
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

If you have not created `requirements.txt` yet, create it with the dependencies your code actually imports and requires.

### 4. Run the project

Run the relevant preprocessing, training, optimization, and dashboard scripts using the instructions that match your actual file names and folder structure.

## 🔮 Future Enhancements

- Improve flood prediction performance and model generalization.
- Explore additional quantum circuit designs and feature maps.
- Integrate real-time rainfall and river-level data.
- Develop a more interactive monitoring dashboard.
- Add geographic maps and sensor location visualization.
- Investigate practical integration with early warning systems.

## 👩‍💻 Project Purpose

This project is an educational prototype exploring how classical and quantum computing techniques may support flood risk analysis and disaster preparedness.

**Note:** This system is experimental and is not intended to replace official flood forecasts or emergency alerts.
