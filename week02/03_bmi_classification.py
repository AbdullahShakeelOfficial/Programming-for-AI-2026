weight = float(input("Enter your weight in kilograms: "))
height = float(input("Enter your height in meters: "))
BMI = weight / (height ** 2)
print(BMI)
if BMI < 18.5:
    print("Classification: Underweight")
elif BMI < 25.0:
    print("Classification: Normal")
elif BMI < 30.0:
    print("Classification: Overweight")
else:
    print("Classification: Obese")