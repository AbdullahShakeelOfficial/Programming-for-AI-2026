# Week 10: Comparing Classification Algorithms with Spambase

## Overview and Attribution
This project evaluates classification algorithms using the UCI Spambase dataset. 
* **Source**: Donated in 1999, available at [https://archive.ics.uci.edu/dataset/94/spambase](https://archive.ics.uci.edu/dataset/94/spambase).

## Data Curation and Features
* **Features**: The dataset uses 57 features (48 word-frequency percentages, 6 character-frequency percentages, and 3 capital-run statistics).
* **Target Mapping**: `0` = Legitimate email, `1` = Spam.
* **Row Counts**: The raw dataset contains 4,601 rows[cite: 20].
* **Excluded-Row Rule**: We removed 391 exact duplicate rows and excluded 6 ambiguous rows where feature-identical patterns had opposite labels. The final usable dataset has 4,204 rows.

## Methodology
* **Data Split**: A 75/25 train/test split was created using `stratify=y` and `random_state=42`.
* **Cross-Validation**: 5-fold Stratified CV was performed on the development set.
* **Preprocessing**: `StandardScaler` was used inside `make_pipeline` for k-NN and Logistic Regression to prevent data leakage during CV.
* **Selection Rule**: The model with the highest mean unrounded CV F1-score was selected (an exact tie uses alphabetical model name). 

## Results & Error Interpretation
* The cross-validation metrics and final test metrics are saved in `reports/model_comparison.csv` and `reports/final_test_metrics.csv`.
* **Error Interpretation**: A False Positive (FP) flags legitimate mail as spam (blocking important emails), while a False Negative (FN) lets spam through to the inbox. High precision is often required to protect legitimate mail.

## Limitations and Responsible AI
* **Historical Benchmark**: Spambase is a historical benchmark from 1999, not a modern filter. Words like "george" or "650" reflect the specific corpus of the donor and may not generalize today.
* **Curation Bias**: Removing difficult feature-identical cases with opposite labels artificially simplifies the dataset; actual performance on unfiltered, current email would likely be lower.