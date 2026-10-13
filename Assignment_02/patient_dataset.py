import json
from pathlib import Path

import numpy as np
import pandas as pd


class PatientDataset:
    """Load, audit, and clean a synthetic patient dataset."""

    # Class-level constants for required columns and missing markers[cite: 25, 28]
    REQUIRED_COLUMNS = ["patient_id", "age", "heart_rate", "department"]  # noqa: RUF012
    MISSING_MARKERS = ["", "missing", "N/A", "-", "NaN"]  # noqa: RUF012

    def __init__(self, path):
        """Load the CSV and retain the original DataFrame[cite: 26, 28]."""
        self.path = Path(path)
        # Load CSV recognizing missing markers and forcing patient_id as string[cite: 26, 28]
        self.raw = pd.read_csv(
            self.path,
            na_values=self.MISSING_MARKERS,
            dtype={"patient_id": str},
        )

    def validate_required(self, columns):
        """Raise ValueError if required columns are missing[cite: 26, 28]."""
        missing = [col for col in columns if col not in self.raw.columns]
        if missing:
            raise ValueError(f"Missing required columns: {missing}")

    def audit(self):
        """Return a JSON-safe audit of the original data[cite: 26, 28]."""
        # 1. Check required columns first[cite: 26]
        self.validate_required(self.REQUIRED_COLUMNS)

        row_count = len(self.raw)
        column_count = len(self.raw.columns)

        # Missing counts per column as loaded[cite: 26]
        missing_counts = {col: int(val) for col, val in self.raw.isna().sum().items()}

        # Exact duplicate count[cite: 26]
        exact_duplicate_count = int(self.raw.duplicated().sum())

        # Repeated ID count after exact duplicates removed (occurrences beyond the first)[cite: 26]
        df_no_exact_dups = self.raw.drop_duplicates()
        if "patient_id" in df_no_exact_dups.columns:
            id_counts = df_no_exact_dups["patient_id"].value_counts()
            repeated_id_count = int((id_counts[id_counts > 1] - 1).sum())
        else:
            repeated_id_count = 0

        # Invalid value counts and nonnumeric counts for numeric columns[cite: 26]
        invalid_value_counts = {}
        nonnumeric_counts = {}

        numeric_rules = {
            "age": (0, 120),
            "heart_rate": (30, 220),
        }

        for col, (min_val, max_val) in numeric_rules.items():
            if col in self.raw.columns:
                # Convert to numeric to check nonnumeric vs invalid range
                converted = pd.to_numeric(self.raw[col], errors="coerce")
                nonnumeric = int(self.raw[col].notna().sum() - converted.notna().sum())
                nonnumeric_counts[col] = nonnumeric

                # Out of range among non-missing numeric values[cite: 26]
                valid_numeric = converted.dropna()
                invalid_count = int(((valid_numeric < min_val) | (valid_numeric > max_val)).sum())
                invalid_value_counts[col] = invalid_count
            else:
                nonnumeric_counts[col] = 0
                invalid_value_counts[col] = 0

        # Distinct non-missing department labels before standardization[cite: 26]
        if "department" in self.raw.columns:
            dept_labels = self.raw["department"].dropna().astype(str).unique().tolist()
            department_labels = sorted(dept_labels)
        else:
            department_labels = []

        audit_dict = {
            "row_count": row_count,
            "column_count": column_count,
            "missing_counts": missing_counts,
            "exact_duplicate_count": exact_duplicate_count,
            "repeated_id_count": repeated_id_count,
            "invalid_value_counts": invalid_value_counts,
            "nonnumeric_counts": nonnumeric_counts,
            "department_labels": department_labels,
        }

        return audit_dict

    def cleaned(self):
        """Return an independent cleaned DataFrame[cite: 27, 28]."""
        # 1. Check required columns exist[cite: 27]
        self.validate_required(self.REQUIRED_COLUMNS)

        # 2. Start with a deep copy of raw[cite: 27]
        df = self.raw.copy(deep=True)

        # 3. Remove exact duplicate rows and reset index with drop=True[cite: 27]
        df = df.drop_duplicates().reset_index(drop=True)

        # 4. Remove surrounding spaces from patient_id[cite: 27]
        df["patient_id"] = df["patient_id"].astype(str).str.strip()

        # 5. Raise ValueError if an ID is missing, empty, or repeated after exact deduplication[cite: 27]
        if df["patient_id"].isna().any() or (df["patient_id"] == "").any() or (df["patient_id"] == "nan").any():
            raise ValueError("Found missing or empty patient IDs after deduplication.")
        if df["patient_id"].duplicated().any():
            raise ValueError("Found conflicting repeated patient IDs after exact deduplication.")

        # 6. Strip department values and convert to uppercase[cite: 27]
        df["department"] = df["department"].astype(str).str.strip().str.upper()

        # 7. Map department variants[cite: 27]
        dept_mapping = {
            "GEN MED": "GENERAL MEDICINE",
            "GENERAL MED": "GENERAL MEDICINE",
            "GENERAL-MED": "GENERAL MEDICINE",
            "CARDIO": "CARDIOLOGY",
        }
        df["department"] = df["department"].replace(dept_mapping)

        # 8. Replace missing or empty department values with 'Unknown'[cite: 27]
        df["department"] = df["department"].replace(["NAN", "NONE", "NAT"], np.nan)
        df["department"] = df["department"].fillna("Unknown")

        # 9. Convert age and heart_rate to numeric with errors="coerce"[cite: 27]
        df["age_numeric_raw"] = pd.to_numeric(df["age"], errors="coerce")
        df["hr_numeric_raw"] = pd.to_numeric(df["heart_rate"], errors="coerce")

        # 10. Replace age outside 0-120 and heart_rate outside 30-220 with missing values[cite: 25, 27]
        age_invalid = (df["age_numeric_raw"] < 0) | (df["age_numeric_raw"] > 120)
        hr_invalid = (df["hr_numeric_raw"] < 30) | (df["hr_numeric_raw"] > 220)

        # 11. Create Boolean age_imputed and heart_rate_imputed columns before filling missing values[cite: 27]
        # Flags cover originally missing, failed numeric conversion, and invalid numeric values[cite: 27]
        df["age_imputed"] = df["age"].isna() | df["age_numeric_raw"].isna() | age_invalid
        df["heart_rate_imputed"] = df["heart_rate"].isna() | df["hr_numeric_raw"].isna() | hr_invalid

        # Apply range bounds restriction by turning invalid/out-of-range into NaN
        df["age_clean"] = df["age_numeric_raw"].mask(age_invalid)
        df["heart_rate_clean"] = df["hr_numeric_raw"].mask(hr_invalid)

        # 12. Fill each numeric column with its own median, calculated from valid values only[cite: 27]
        # 13. Raise ValueError if a numeric column has no valid values[cite: 27]
        if df["age_clean"].dropna().empty:
            raise ValueError("Age column has no valid values to calculate a median.")
        if df["heart_rate_clean"].dropna().empty:
            raise ValueError("Heart rate column has no valid values to calculate a median.")

        age_median = df["age_clean"].median()
        hr_median = df["heart_rate_clean"].median()

        df["age"] = df["age_clean"].fillna(age_median)
        df["heart_rate"] = df["heart_rate_clean"].fillna(hr_median)

        # Drop helper columns
        df = df.drop(columns=["age_numeric_raw", "hr_numeric_raw", "age_clean", "heart_rate_clean"])

        # 14. Return the cleaned DataFrame[cite: 27]
        return df

    def save_audit(self, path):
        """Save the original-data audit as JSON[cite: 28]."""
        audit_data = self.audit()
        out_path = Path(path)
        out_path.parent.mkdir(parents=True, exist_ok=True)

        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(audit_data, f, indent=4)