# Week 6 Data Cleaning Report

## Overview
This report documents data quality issues found in `students_messy.csv` and the steps taken to clean, validate, and preprocess the dataset.

## Key Cleaning Decisions
1. **Duplicates Removal**: Exact duplicate rows were identified and removed, reducing redundancy.
2. **Text Standardization**: Program names (e.g., "BS AI", "AI") were normalized to standard codes (`BSAI`, `BSDS`, `BSCS`), and city names were standardized to title case with abbreviation expansion ("Rwp" to "Rawalpindi").
3. **Out-of-Range Handling**: Values outside the valid range [0, 100] (such as `-5` and `110`) were flagged, recorded in `invalid_records.csv`, and replaced with `pd.NA`.
4. **Missing Value Imputation**: Missing attendance values were imputed using program-level medians with an overall median fallback. Assessment scores were filled using column medians.
5. **Feature Engineering**: Derived metrics including `weighted_score`, `attendance_status`, letter `grade`, and an `at_risk` indicator were successfully created.