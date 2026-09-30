import numpy as np

a = np.ones((3, 4))
b = np.ones((3, 4)) 
result_f1 = a + b
print("F1 Result shape:", result_f1.shape)

values = np.array([10, 20, 30, 40])
selected = values[(values > 15) & (values < 35)]
print("F2 Selected values:", selected)

scores = np.array([[70, 80, 90], [60, 75, 85]])
student_averages = np.mean(scores, axis=1)
print("F3 Correct student averages:", student_averages)