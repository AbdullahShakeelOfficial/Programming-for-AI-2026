obtained_marks = float(input("Enter obtained marks: "))
total_marks = float(input("Enter total marks: "))

percentage = (obtained_marks / total_marks) * 100
print("Percentage:", round(percentage, 2))

# Test 1: obtained = 76, total = 100 -> Expected: 76.0
# Test 2: obtained = 450, total = 500 -> Expected: 90.0