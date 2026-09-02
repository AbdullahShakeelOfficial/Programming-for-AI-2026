weight = float(input("Enter weight in kg: "))
height = float(input("Enter height in meters: "))

bmi = weight / (height ** 2)
print("BMI:", round(bmi, 2))

# Test 1: weight = 60, height = 1.65 -> Expected BMI: 22.04
# Test 2: weight = 70, height = 1.75 -> Expected BMI: 22.86