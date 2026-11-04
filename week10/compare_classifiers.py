from io import BytesIO
from pathlib import Path
from urllib.request import urlretrieve
from zipfile import ZipFile

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sklearn
from sklearn.base import clone
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    make_scorer,
    precision_score,
    recall_score,
)
from sklearn.model_selection import StratifiedKFold, cross_validate, train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier

RANDOM_STATE = 42

# ==============================================================
# Part A: Setup, email data, and fixed cleaning rules
# ==============================================================
LAB_DIR = Path("week10")
DATA_DIR = LAB_DIR / "data"
REPORTS_DIR = LAB_DIR / "reports"
FIGURES_DIR = LAB_DIR / "figures"
MODELS_DIR = LAB_DIR / "models"

for folder in [DATA_DIR, REPORTS_DIR, FIGURES_DIR, MODELS_DIR]:
    folder.mkdir(parents=True, exist_ok=True)

archive_path = DATA_DIR / "spambase.zip"
if not archive_path.exists():
    urlretrieve("https://archive.ics.uci.edu/static/public/94/spambase.zip", archive_path)

with ZipFile(archive_path) as archive:
    names_text = archive.read("spambase.names").decode("utf-8")
    FEATURES = [line.split(":")[0] for line in names_text.splitlines() 
                if line.startswith(("word_freq_", "char_freq_", "capital_run_length_"))]
    data = pd.read_csv(BytesIO(archive.read("spambase.data")), header=None)
    data.columns = FEATURES + ["is_spam"]

# Validations
assert len(FEATURES) == 57 and data.shape[1] == 58
assert all(pd.api.types.is_numeric_dtype(data[c]) for c in data)
assert np.isfinite(data.to_numpy()).all(), "Missing or infinite value"
assert set(data["is_spam"].unique()) == {0, 1}

print("Raw shape:", data.shape)
print("Missing values:", int(data.isna().sum().sum()))
print("Raw class counts:", data["is_spam"].value_counts().to_dict())

# Curation rules
exact_duplicates = int(data.duplicated().sum())
clean = data.drop_duplicates().copy()
ambiguous = clean.duplicated(subset=FEATURES, keep=False)

print("Exact duplicate rows removed:", exact_duplicates)
print("Ambiguous feature rows excluded:", int(ambiguous.sum()))

clean = clean.loc[~ambiguous].reset_index(drop=True)
X = clean[FEATURES].copy()
y = clean["is_spam"].astype(int)

print("Usable feature matrix:", X.shape)
print("Class counts:", y.value_counts().sort_index().to_dict())
print("Class proportions:", y.value_counts(normalize=True).round(3))

# ==============================================================
# Part B: Development/test split and model pipelines
# ==============================================================
X_dev, X_test, y_dev, y_test = train_test_split(
    X, y, test_size=0.25, random_state=RANDOM_STATE, stratify=y
)

assert set(X_dev.index).isdisjoint(X_test.index)
assert not X.duplicated().any()

print("\nDevelopment:", X_dev.shape, y_dev.value_counts().to_dict())
print("Final test:", X_test.shape, y_test.value_counts().to_dict())

models = {
    "Decision Tree": DecisionTreeClassifier(max_depth=4, random_state=RANDOM_STATE),
    "k-NN": make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=5)),
    "Logistic Regression": make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000)),
    "Gaussian NB": GaussianNB(),
    "Majority baseline": DummyClassifier(strategy="most_frequent"),
}

# ==============================================================
# Part C: Cross-validation of four classifiers and baseline
# ==============================================================
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
folds = list(cv.split(X_dev, y_dev))

scoring = {
    "accuracy": "accuracy",
    "precision": make_scorer(precision_score, zero_division=0),
    "recall": make_scorer(recall_score, zero_division=0),
    "f1": make_scorer(f1_score, zero_division=0),
}

results = []
for name, candidate in models.items():
    scores = cross_validate(candidate, X_dev, y_dev, cv=folds, scoring=scoring)
    row = {"model": name}
    for metric in scoring:
        values = scores[f"test_{metric}"]
        row[metric] = values.mean()
        row[f"{metric}_std"] = values.std(ddof=1)
    results.append(row)

comparison = pd.DataFrame(results).sort_values(
    ["f1", "model"], ascending=[False, True]
).reset_index(drop=True)

print("\nCross-Validation Results:")
print(comparison.round(3).to_string(index=False))
comparison.to_csv(REPORTS_DIR / "model_comparison.csv", index=False)

# ==============================================================
# Part D: Selection, refit, and final test evaluation
# ==============================================================
# D1. Visualize
metrics = ["accuracy", "precision", "recall", "f1"]
ax = comparison.set_index("model")[metrics].plot(
    kind="bar", ylim=(0, 1), figsize=(10, 5)
)
ax.set_ylabel("Mean validation score")
ax.set_xlabel("Model")
ax.set_title("Spambase: five-fold cross-validation on development data")
plt.xticks(rotation=20, ha="right")
plt.tight_layout()
plt.savefig(FIGURES_DIR / "model_comparison.png", dpi=200)
plt.close()

# D2. Select, refit, and evaluate
selected_name = comparison.iloc[0]["model"]
selected_model = clone(models[selected_name])
selected_model.fit(X_dev, y_dev)

test_predictions = selected_model.predict(X_test)
print("\nSelected using CV only:", selected_name)

final_metrics = pd.DataFrame([{
    "model": selected_name,
    "accuracy": accuracy_score(y_test, test_predictions),
    "precision": precision_score(y_test, test_predictions, zero_division=0),
    "recall": recall_score(y_test, test_predictions, zero_division=0),
    "f1": f1_score(y_test, test_predictions, zero_division=0),
}])

print(final_metrics.round(3).to_string(index=False))
final_metrics.to_csv(REPORTS_DIR / "final_test_metrics.csv", index=False)

# D3. Interpret errors
cm = confusion_matrix(y_test, test_predictions, labels=[0, 1])
tn, fp, fn, tp = cm.ravel()
assert cm.sum() == len(y_test)

print("\nConfusion Matrix (Rows=actual; columns=predicted; label order=[0,1])")
print(cm)
print(f"TN={tn}, FP={fp}, FN={fn}, TP={tp}")
pd.DataFrame(cm, index=["actual_0", "actual_1"], columns=["pred_0", "pred_1"]).to_csv(REPORTS_DIR / "confusion_matrix.csv")

# ==============================================================
# Part E: Persistence, predictions, debugging, and Git
# ==============================================================
# E1. Save the fitted estimator
bundle_path = MODELS_DIR / "spam_predictor.joblib"
bundle = {
    "model": selected_model,
    "features": FEATURES,
    "target_mapping": {0: "legitimate", 1: "spam"},
    "selected_name": selected_name,
    "sklearn_version": sklearn.__version__,
}
joblib.dump(bundle, bundle_path)

loaded = joblib.load(bundle_path)
reloaded_predictions = loaded["model"].predict(X_test[loaded["features"]])
assert np.array_equal(reloaded_predictions, test_predictions)
print("\nSaved and verified:", bundle_path)

# E2. Test one existing record
new_email = X_test.iloc[[0]].copy()
aligned = new_email[loaded["features"]]
prediction = int(loaded["model"].predict(aligned)[0])

print("\nPredicted:", loaded["target_mapping"][prediction])
print("Actual:", loaded["target_mapping"][int(y_test.iloc[0])])