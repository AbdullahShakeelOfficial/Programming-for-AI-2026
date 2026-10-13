from pathlib import Path

import pandas as pd
from patient_dataset import PatientDataset


def main():
    """Run the patient dataset audit and cleaning demonstration[cite: 28]."""
    # 1. Locate Assignment_02 using Path(__file__).resolve().parent[cite: 28]
    base_dir = Path(__file__).resolve().parent
    csv_path = base_dir / "data" / "patients_messy.csv"
    audit_json_path = base_dir / "output" / "audit.json"
    clean_csv_path = base_dir / "output" / "patients_clean.csv"

    try:
        # 2. Create a PatientDataset object[cite: 28]
        print(f"Loading dataset from {csv_path}...")
        dataset = PatientDataset(csv_path)

        # 3. Display original-data audit[cite: 28]
        audit_res = dataset.audit()
        print("\n--- Original Dataset Audit ---")
        print(f"Original rows: {audit_res['row_count']}")
        print(f"Original columns: {audit_res['column_count']}")
        print(f"Exact duplicates to remove: {audit_res['exact_duplicate_count']}")
        print(f"Invalid age values: {audit_res['invalid_value_counts'].get('age', 0)}")
        print(f"Invalid heart rate values: {audit_res['invalid_value_counts'].get('heart_rate', 0)}")

        # 4. Obtain and display cleaned DataFrame[cite: 28]
        cleaned_df = dataset.cleaned()
        print("\n--- Cleaning Completed ---")
        print(f"Cleaned rows: {len(cleaned_df)}")
        print(f"Age values imputed: {cleaned_df['age_imputed'].sum()}")
        print(f"Heart-rate values imputed: {cleaned_df['heart_rate_imputed'].sum()}")

        # 5. Save audit as JSON[cite: 28]
        dataset.save_audit(audit_json_path)
        print(f"Saved: {audit_json_path.relative_to(base_dir.parent)}")

        # 6. Save cleaned DataFrame as CSV without index[cite: 28]
        clean_csv_path.parent.mkdir(parents=True, exist_ok=True)
        cleaned_df.to_csv(clean_csv_path, index=False)
        print(f"Saved: {clean_csv_path.relative_to(base_dir.parent)}")

    except FileNotFoundError as e:
        print(f"Error: File not found. {e}")
    except pd.errors.EmptyDataError:
        print("Error: The CSV file is empty.")
    except pd.errors.ParserError:
        print("Error: Failed to parse the CSV file due to formatting issues.")
    except ValueError as e:
        print(f"ValueError encountered: {e}")
    except OSError as e:
        print(f"OS error encountered: {e}")


if __name__ == "__main__":
    main()