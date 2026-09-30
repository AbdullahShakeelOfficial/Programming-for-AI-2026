import numpy as np

marks = np.array([78, 85, 91, 66, 88])
matrix = np.arange(12).reshape(3, 4)
images = np.zeros((2, 4, 4))
identity = np.eye(4)
values = np.linspace(0, 1, 10)

arrays = {
    "Marks": marks,
    "Matrix": matrix,
    "Images": images,
    "Identity": identity,
    "Values": values,
}

for name, arr in arrays.items():
    print(f"--- {name} ---")
    print(f"Shape: {arr.shape}")
    print(f"Dimensions (ndim): {arr.ndim}")
    print(f"Size: {arr.size}")
    print(f"Data type (dtype): {arr.dtype}\n")

assert matrix.size == 12
assert images.ndim == 3
print("Hafiz Abdullah Shakeel 72405")