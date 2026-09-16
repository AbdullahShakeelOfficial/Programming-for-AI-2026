def average(a, b):
    return (a + b) / 2


print("G1 Average:", average(10, 20))


def double(number):
    return number * 2


print("G2 Double:", double(5))

try:
    age = int(input("G3 Enter Age: "))
    print("Recorded Age:", age)
except ValueError:
    print("Please enter a valid numeric age.")

def calculate_student_grade(mark):
    """Return grade category for refactored student checks."""
    if mark >= 85:
        return "A"
    elif mark >= 70:
        return "B"
    else:
        return "below B"


students = [("Ali", 88), ("Sara", 73), ("Hamza", 62)]

for name, mark in students:
    grade = calculate_student_grade(mark)
    print(f"{name}: {grade}")