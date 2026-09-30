import numpy as np

# Base Matrix
data = np.array([
    [10, 20, 30, 40],
    [50, 60, 70, 80],
    [90, 100, 110, 120],
    [130, 140, 150, 160]
])

print("Original Matrix:\n", data)
print("\nFirst row:", data[0])
print("Last column:", data[:, -1])
print("Middle 2x2 block:\n", data[1:3, 1:3])
print("Every second row:\n", data[::2])
print("Values > 75:", data[data > 75])
print("Values divisible by 20:", data[(data % 20 == 0)])