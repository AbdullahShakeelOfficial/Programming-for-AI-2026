import numpy as np

temperature = np.array([20,25,30,35,40])
fahrenheit = (temperature * 9/5) + 32
marks = np.array([55,67,72,88,91])
adjusted_marks = marks + 5
adjusted = np.minimum(marks + 5, 100)
normalized = (marks - marks.min()) / (marks.max() - marks.min())
print(np.round(normalized, 2))
age = np.array([20,40,60])
income = np.array([30000, 150000, 300000])

print(f"age: {age}")
print(f"income: {income}")

normalized_age = (age - age.min()) / (age.max() - age.min())
normalized_income = (income - income.min()) / (income.max() - income.min())
print(f"Normalized age: {np.round(normalized_age, 2)}")
print(f"Normalized income: {np.round(normalized_income, 2)}")