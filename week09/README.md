# Week 9: Introduction to Machine Learning with scikit-learn

## Overview
This lab implements a binary classification pipeline using scikit-learn[cite: 11]. We trained a `DecisionTreeClassifier` to predict machine faults (`1` = fault, `0` = normal) based on temperature, vibration, runtime, and pressure[cite: 12].

## Method
1. Validated and loaded `machines_ml.csv`[cite: 12].
2. Separated features (`X`) from the target (`y`), excluding identifiers to prevent leakage[cite: 13].
3. Performed a reproducible 80/20 train-test split using `stratify=y` to maintain class proportions[cite: 13].
4. Evaluated multiple tree depths and exported performance metrics to `reports/model_comparison.csv` to analyze the training/testing gap (overfitting/underfitting)[cite: 14].
5. Saved the best model and its expected feature names into a `.joblib` bundle for safe reloading.

## Results
* Baseline tree (`max_depth=3`) was evaluated using Accuracy and a Confusion Matrix[cite: 13, 14].
* Testing performance revealed the model's true ability to generalize to unseen data[cite: 11].

## Limitations
* The dataset lacks external context variables (e.g., maintenance history, machine brand)[cite: 15].
* The decision tree model optimization is limited, as selecting depth purely based on one small test set can lead to overfitting on that specific test data[cite: 14].