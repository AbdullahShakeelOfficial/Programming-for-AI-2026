import numpy as np
import os

score = np.array([[70, 75, 80], [60, 65, 70], [85, 90, 95]])
bonus = np.array([2, 3, 5])
adjusted_score = score + bonus
print("Adjusted Score:\n", adjusted_score)

patient_data = np.array([
    [101, 45, 38.5, 100, 92],
    [102, 23, 37.0, 110, 88],
    [103, 67, 39.0, 120, 95],
    [104, 54, 36.5, 130, 90], 
    [105, 34, 37.5, 140, 85],
    [106, 72, 38.0, 150, 80]
], dtype=float)

print(f"\nShape: {patient_data.shape}")
print(f"Dimensions: {patient_data.ndim}")
print(f"Size: {patient_data.size}")
print(f"Data type: {patient_data.dtype}")

patient_ids = patient_data[:, 0].astype(int)
print("Patient IDs:", patient_ids)

features = patient_data[:, 1:]
print(f"Clinical Features:\n{features}")

age = patient_data[:, 1]
temp = patient_data[:, 2]
heart_press = patient_data[:, 3]
oxygen = patient_data[:, 4]

average_age = age.mean()
print(f"Average Age: {average_age:.2f}")

features_mean = features.mean(axis=0)
print("Age Mean: ", round(features_mean[0], 2))
print("Temperature Mean: ", round(features_mean[1], 2))
print("Heart Rate Mean: ", round(features_mean[2], 2))
print("Oxygen Level Mean: ", round(features_mean[3], 2))

older_than_60 = patient_data[age > 60]
print(f"\nPatients older than 60:\n{older_than_60}")

hotter_than_38 = patient_data[temp > 38.0]
print(f"Patients with temperature > 38:\n{hotter_than_38}")

oxygen_below_94 = patient_data[oxygen < 94]
print(f"Patients with oxygen level < 94:\n{oxygen_below_94}")

high_risk_marks = ((temp > 38.0) & (oxygen < 94))
print(f"Count High Risk Patients: {np.count_nonzero(high_risk_marks)}")
print(f"High Risk Patients IDs:\n{patient_ids[high_risk_marks]}")

features_min = features.min(axis=0)
features_range = features.max(axis=0) - features.min(axis=0)
normalized_features = (features - features_min) / features_range

print("\nNormalized Clinical Features:\n")
print(np.round(normalized_features, 2))

os.makedirs("week05/data", exist_ok=True)
os.makedirs("week05/output", exist_ok=True)

np.save("week05/data/patient_data.npy", patient_data)
loaded_npy = np.load("week05/data/patient_data.npy")

np.savetxt("week05/output/normalized_features.csv", normalized_features, delimiter=",", fmt="%.4f")
loaded_csv = np.loadtxt("week05/output/normalized_features.csv", delimiter=",")

print("\nLoaded Normalized Features from CSV:\n", loaded_csv)