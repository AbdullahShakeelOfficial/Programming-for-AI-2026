from pathlib import Path

import joblib
import pandas as pd
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

# ==========================================
# PART A: Setup and validate data
# ==========================================
DATA_PATH = Path("week09/data/machines_ml.csv")
machines = pd.read_csv(DATA_PATH)

required = {"temp_c", "vibration", "runtime", "pressure", "fault"}
missing = required - set(machines.columns)

if missing:
    raise ValueError(f"Missing columns: {sorted(missing)}")
if machines[list(required)].isna().any().any():
    raise ValueError("Required columns contain missing values.")
if not set(machines["fault"].unique()).issubset({0, 1}):
    raise ValueError("fault must contain only 0 and 1.")

print("Data Shape:", machines.shape)
print("Target Class Proportions:\n", machines["fault"].value_counts(normalize=True))

# ==========================================
# PART B: Features and train-test split
# ==========================================
FEATURES = ["temp_c", "vibration", "runtime", "pressure"]
X = machines[FEATURES]
y = machines["fault"]

# Create a reproducible, stratified split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"\nTrain rows: {len(X_train)}, Test rows: {len(X_test)}")

# ==========================================
# PART C: Train and evaluate a classifier
# ==========================================
# C1. Train a baseline tree
model = DecisionTreeClassifier(max_depth=3, random_state=42)
model.fit(X_train, y_train)

train_predictions = model.predict(X_train)
test_predictions = model.predict(X_test)

train_accuracy = accuracy_score(y_train, train_predictions)
test_accuracy = accuracy_score(y_test, test_predictions)

print(f"\nBaseline Tree - Train Accuracy: {train_accuracy:.4f}")
print(f"Baseline Tree - Test Accuracy: {test_accuracy:.4f}")

# C2. Interpret the result (Confusion Matrix)
cm = confusion_matrix(y_test, test_predictions)
tn, fp, fn, tp = cm.ravel()
manual_accuracy = (tn + tp) / cm.sum()

print("\nConfusion Matrix Results:")
print({"TN": tn, "FP": fp, "FN": fn, "TP": tp})
assert abs(manual_accuracy - test_accuracy) < 1e-12

# ==========================================
# PART D: Depth experiment and persistence
# ==========================================
# D1. Compare model complexity
results = []
for depth in [1, 2, 3, 5, None]:
    candidate = DecisionTreeClassifier(max_depth=depth, random_state=42)
    candidate.fit(X_train, y_train)
    
    train_score = candidate.score(X_train, y_train)
    test_score = candidate.score(X_test, y_test)
    
    results.append({
        "max_depth": str(depth),
        "train_accuracy": train_score,
        "test_accuracy": test_score,
        "gap": train_score - test_score
    })

comparison = pd.DataFrame(results)
reports_dir = Path("week09/reports")
reports_dir.mkdir(parents=True, exist_ok=True)
comparison.to_csv("week09/reports/model_comparison.csv", index=False)

print("\nDepth Experiment Results:")
print(comparison)

# D2. Save and reload the model bundle
bundle_path = Path("week09/models/machine_predictor.joblib")
bundle_path.parent.mkdir(parents=True, exist_ok=True)

bundle = {"model": model, "features": FEATURES}
joblib.dump(bundle, bundle_path)

loaded = joblib.load(bundle_path)
reloaded_predictions = loaded["model"].predict(X_test[loaded["features"]])
assert (reloaded_predictions == test_predictions).all()
print("\nModel saved and reloaded successfully!")

# ==========================================
# PART E: Predict new records
# ==========================================
new_machines = pd.DataFrame([
    {"temp_c": 98, "vibration": 6.5, "runtime": 14200, "pressure": 3.2},
    {"temp_c": 61, "vibration": 1.2, "runtime": 2700, "pressure": 6.7},
    {"temp_c": 81, "vibration": 3.8, "runtime": 8600, "pressure": 4.8},
])

feature_order = loaded["features"]
if set(new_machines.columns) != set(feature_order):
    raise ValueError("Prediction columns do not match training features.")

new_machines["predicted_fault"] = loaded["model"].predict(new_machines[feature_order])
print("\nPredictions for new data:")
print(new_machines)