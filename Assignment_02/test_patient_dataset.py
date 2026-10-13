import json
from pathlib import Path

import pandas as pd
from patient_dataset import PatientDataset

# Setup paths for testing
base_dir = Path(__file__).resolve().parent
messy_path = base_dir / "data" / "patients_messy.csv"
audit_out = base_dir / "output" / "test_audit.json"

# 1. Test missing required column raises ValueError[cite: 29]
# We create a temporary bad CSV
bad_csv = base_dir / "data" / "bad_columns.csv"
pd.DataFrame({"wrong_col": [1, 2]}).to_csv(bad_csv, index=False)
try:
    ds_bad = PatientDataset(bad_csv)
    ds_bad.validate_required(["patient_id", "age"])
    raise AssertionError("Expected ValueError for missing columns was not raised.")
except ValueError:
    pass  # Expected
finally:
    if bad_csv.exists():
        bad_csv.unlink()

# Load main dataset for subsequent tests
dataset = PatientDataset(messy_path)

# 2. Original-data audit reports 100 rows and 1 exact duplicate[cite: 29]
audit_res = dataset.audit()
assert audit_res["row_count"] == 100, f"Expected 100 rows, got {audit_res['row_count']}"
assert audit_res["exact_duplicate_count"] == 1, f"Expected 1 exact duplicate, got {audit_res['exact_duplicate_count']}"

# 3. Cleaned dataset has 99 rows (exact duplicate removed)[cite: 27, 29]
cleaned_df = dataset.cleaned()
assert len(cleaned_df) == 99, f"Expected 99 rows after cleaning, got {len(cleaned_df)}"

# 4. Invalid numeric values are replaced and filled; bounds checked[cite: 29]
assert cleaned_df["age"].between(0, 120).all(), "Some ages are out of 0-120 range after cleaning."
assert cleaned_df["heart_rate"].between(30, 220).all(), "Some heart rates are out of 30-220 range."

# 5. Medians and imputation counts match expected results[cite: 27, 29]
assert cleaned_df["age_imputed"].sum() == 11, f"Expected 11 age imputations, got {cleaned_df['age_imputed'].sum()}"
assert cleaned_df["heart_rate_imputed"].sum() == 9, f"Expected 9 HR imputations, got {cleaned_df['heart_rate_imputed'].sum()}"

# 6. Conflicting repeated ID raises ValueError[cite: 29]
conflict_csv = base_dir / "data" / "conflict_id.csv"
conflict_data = pd.DataFrame({
    "patient_id": ["P101", "P101"],
    "age": [30, 45],
    "heart_rate": [70, 80],
    "department": ["Cardiology", "Neurology"]
})
conflict_data.to_csv(conflict_csv, index=False)
try:
    ds_conflict = PatientDataset(conflict_csv)
    ds_conflict.cleaned()
    raise AssertionError("Expected ValueError for conflicting repeated ID was not raised.")
except ValueError:
    pass
finally:
    if conflict_csv.exists():
        conflict_csv.unlink()

# 7. Original data preserved (audit and cleaned do not alter self.raw)[cite: 26, 27, 29]
raw_row_count_before = len(dataset.raw)
dataset.audit()
dataset.cleaned()
assert len(dataset.raw) == raw_row_count_before, "self.raw was modified during audit() or cleaned()."

# 8. Independent cleaned result (changing returned df does not change self.raw)[cite: 27, 29]
modified_df = dataset.cleaned()
modified_df.loc[0, "age"] = 999
assert dataset.raw.loc[0, "age"] != 999, "Modifying cleaned DataFrame affected self.raw."

# Reload audit.json using json.load() to confirm valid JSON export[cite: 28, 29]
dataset.save_audit(audit_out)
with open(audit_out, "r", encoding="utf-8") as f:
    reloaded_audit = json.load(f)
assert reloaded_audit["row_count"] == 100

print("All tests passed.")