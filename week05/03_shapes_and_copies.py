import numpy as np

original = np.array([10, 20, 30, 40, 50])
view = original[1:4]
view[0] = 999 
print("Original after view modification:", original)

original_fresh = np.array([10, 20, 30, 40, 50])
independent = original_fresh[1:4].copy()
independent[0] = 999
print("Original safe after independent copy modification:", original_fresh)
print("Independent copy:", independent)

values = np.arange(1, 13)
reshaped = values.reshape(3, 4)
transposed = reshaped.T
flattened = transposed.flatten()

arr1 = np.ones((2, 2))
arr2 = np.zeros((2, 2))
v_stacked = np.vstack((arr1, arr2))
h_stacked = np.hstack((arr1, arr2))

split_parts = np.split(np.arange(12), 3)

print("\nShape Transformations:")
print("Reshaped (3x4):\n", reshaped)
print("Transposed shape:", transposed.shape)
print("Flattened shape:", flattened.shape)
print("Vertical Stack shape:", v_stacked.shape)
print("Horizontal Stack shape:", h_stacked.shape)
print("Split parts lengths:", [len(p) for p in split_parts])