# Assignment 2: Patient Dataset Audit Toolkit

## Program Description
A modular Python toolkit featuring the `PatientDataset` class to load, validate, audit, and clean synthetic hospital patient records, handling missing markers, text standardization, range bounds, and median imputation[cite: 24, 28].

## Files Included
* `patient_dataset.py`: Core `PatientDataset` class implementation[cite: 24].
* `demo.py`: Main execution script displaying audits and saving outputs[cite: 24, 28].
* `test_patient_dataset.py`: Comprehensive test suite with assertions[cite: 24, 29].
* `README.md`: Project documentation and explanations[cite: 30, 31].
* `AI_USE.md`: AI tool usage records[cite: 30, 31].

## Key Decisions & Explanations
1. **Deep Copy (`cleaned()`)**: Starts with `self.raw.copy(deep=True)` to ensure raw data remains completely immutable[cite: 27, 30].
2. **Exact Duplicates First**: Removed before checking repeated IDs to avoid false positives from redundant identical entries[cite: 26, 27, 30].
3. **`errors="coerce"`**: Converts nonnumeric entries to `NaN` safely without crashing[cite: 27, 30].
4. **Excluding Invalid Values Before Medians**: Ensures median imputation is calculated solely from valid clinical measurements[cite: 27, 30].
5. **Imputation Flags (`age_imputed`, `heart_rate_imputed`)**: Boolean tracking columns that clearly distinguish original values from imputed substitutes for reviewers[cite: 27, 30].

## Run Commands
```powershell
uv run python Assignment_02/demo.py
uv run python Assignment_02/test_patient_dataset.py