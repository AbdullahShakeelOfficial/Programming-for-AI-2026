import os

import numpy as np
import pandas as pd

# =============================================================
# MODULE 1: SETUP & DIRECTORIES INITIALIZATION
# Is module ka maqsad required output aur report folders banana hai.
# =============================================================
os.makedirs("week06/data/processed", exist_ok=True)
os.makedirs("week06/reports", exist_ok=True)


# =============================================================
# MODULE 2: DATA LOADING & INITIAL INSPECTION
# Raw messy CSV file ko load karna aur shuruati data check karna.
# =============================================================
students = pd.read_csv(
    "week06/data/raw/students_messy.csv",
    na_values=[" ", "missing", "N/A", "NaN"],
)

print("--- Initial Inspection ---")
print("Shape:", students.shape)
print("\nHead:\n", students.head())
print("\nInfo:")
students.info()
print("\nMissing Values:\n", students.isna().sum())
print("Exact Duplicates:", students.duplicated().sum())


# =============================================================
# MODULE 3: DUPLICATES REMOVAL & TEXT STANDARDIZATION
# Duplicate rows ko hatana aur text/category columns ko clean karna.
# =============================================================
# Exact duplicates remove karna aur index reset karna
students = students.drop_duplicates().reset_index(drop=True)

# Extra spaces remove karna
students["program"] = students["program"].astype("string").str.strip()
students["city"] = students["city"].astype("string").str.strip()

# Program names map karna (BSAI, BSDS standardization)
program_mapping = {
    "BS AI": "BSAI",
    "BS-AI": "BSAI",
    "AI": "BSAI",
    "BS DS": "BSDS",
    "BSDS": "BSDS",
    "BSCS": "BSCS",
    "BSAI": "BSAI",
}
students["program"] = students["program"].replace(program_mapping)

# City names standardize karna (Rwp -> Rawalpindi, Title case, missing -> Unknown)
students["city"] = students["city"].str.title()
students["city"] = students["city"].replace({"Rwp": "Rawalpindi"})
students["city"] = students["city"].fillna("Unknown")


# =============================================================
# MODULE 4: TYPE CONVERSION, RANGE VALIDATION & LOGGING
# Numeric types convert karna aur 0-100 ki range validate karna.
# Invalid values ko track kar ke cleaning log aur report banana.
# =============================================================
# Numeric conversions with errors="coerce"
numeric_cols = ["attendance", "assignment", "midterm", "final"]
for col in numeric_cols:
    students[col] = pd.to_numeric(students[col], errors="coerce")

# Dates parsing aur student_id ko string banana
students["admission_date"] = pd.to_datetime(
    students["admission_date"], dayfirst=True, errors="coerce"
)
students["student_id"] = students["student_id"].astype(str)

# Range Validation (0 to 100)
invalid_records_list = []
cleaning_log_list = []

for col in numeric_cols:
    invalid_mask = (students[col] < 0) | (students[col] > 100)
    if invalid_mask.any():
        bad_rows = students[invalid_mask].copy()
        bad_rows["issue_column"] = col
        invalid_records_list.append(bad_rows)
        for idx in students[invalid_mask].index:
            val = students.loc[idx, col]
            cleaning_log_list.append({
                "student_id": students.loc[idx, "student_id"],
                "column": col,
                "invalid_value": val,
                "action": "Replaced with pd.NA",
                "reason": "Out of valid 0-100 range",
            })
        students.loc[invalid_mask, col] = pd.NA

# Invalid records save karna CSV mein
if invalid_records_list:
    invalid_df = pd.concat(invalid_records_list, ignore_index=True)
    invalid_df.to_csv("week06/reports/invalid_records.csv", index=False)

# Cleaning log save karna CSV mein
cleaning_log_df = pd.DataFrame(cleaning_log_list)
cleaning_log_df.to_csv("week06/reports/cleaning_log.csv", index=False)


# =============================================================
# MODULE 5: MISSING VALUES IMPUTATION
# Missing attendance ko program median se (fallback overall median)
# aur assessment marks ko column medians se fill karna.
# =============================================================
program_medians = students.groupby("program")["attendance"].transform(
    "median"
)
overall_median = students["attendance"].median()
students["attendance_imputed_flag"] = students["attendance"].isna()
students["attendance"] = students["attendance"].fillna(program_medians).fillna(overall_median)

# Assessment marks fill with column medians
for col in ["assignment", "midterm", "final"]:
    col_median = students[col].median()
    students[f"{col}_imputed_flag"] = students[col].isna()
    students[col] = students[col].fillna(col_median)


# =============================================================
# MODULE 6: FEATURE ENGINEERING & CATEGORIZATION
# Weighted scores calculate karna, grades aur attendance status banana,
# aur at-risk flag generate karna.
# =============================================================
# Weighted Score (Assignment 20%, Midterm 30%, Final 50%)
students["weighted_score"] = (
    students["assignment"] * 0.20
    + students["midterm"] * 0.30
    + students["final"] * 0.50
)

# Attendance Status categories
conditions_att = [
    students["attendance"] < 75,
    (students["attendance"] >= 75) & (students["attendance"] < 85),
    students["attendance"] >= 85,
]
choices_att = ["Low", "Satisfactory", "Excellent"]
students["attendance_status"] = np.select(conditions_att, choices_att, default="Unknown")

# Grades using np.select
conditions_grade = [
    students["weighted_score"] >= 85,
    students["weighted_score"] >= 75,
    students["weighted_score"] >= 65,
    students["weighted_score"] >= 50,
]
choices_grade = ["A", "B", "C", "D"]
students["grade"] = np.select(conditions_grade, choices_grade, default="F")

# At-risk flag (Attendance < 75 OR Weighted Score < 50)
students["at_risk"] = (students["attendance"] < 75) | (students["weighted_score"] < 50)


# =============================================================
# MODULE 7: GROUPING & AGGREGATION (SUMMARIES)
# Program-wise summary aur grade distribution calculate karna.
# =============================================================
program_summary = (
    students.groupby("program")
    .agg(student_count=("student_id", "count"), avg_weighted_score=("weighted_score", "mean"))
    .reset_index()
)

grade_distribution = (
    students["grade"].value_counts().reset_index()
)
grade_distribution.columns = ["grade", "student_count"]


# =============================================================
# MODULE 8: SAVING CLEANED OUTPUTS
# Processed data aur summary files ko CSV format mein save karna.
# =============================================================
students.to_csv("week06/data/processed/students_clean.csv", index=False)
program_summary.to_csv("week06/data/processed/program_summary.csv", index=False)
grade_distribution.to_csv("week06/data/processed/grade_distribution.csv", index=False)

print("\n--- Processing Completed Successfully! All files saved module-wise. ---")