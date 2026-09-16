def calculate_grade(marks):
    """Return letter grade based on marks boundaries."""
    if marks >= 85:
        return "A"
    elif marks >= 70:
        return "B"
    elif marks >= 60:
        return "C"
    elif marks >= 50:
        return "D"
    else:
        return "F"


def calculate_bmi(weight_kg, height_m):
    """Return BMI rounded to two decimal places."""
    bmi = weight_kg / (height_m**2)
    return round(bmi, 2)


square = lambda number: number**2


def calculate_average(*marks):
    """Return arithmetic mean of positional arguments."""
    if not marks:
        return 0.0
    return sum(marks) / len(marks)


def format_student(**details):
    """Return formatted string from keyword arguments."""
    name = details.get("name", "Student")
    program = details.get("program", "AI")
    return f"{name} studies {program}"


def main():
    mark = int(input("Enter marks: "))
    print("Grade:", calculate_grade(mark))

    weight = float(input("Enter weight (kg): "))
    height = float(input("Enter height (m): "))
    print("BMI:", calculate_bmi(weight, height))

    print("Square of 4:", square(4))
    print("Average marks:", calculate_average(70, 80, 90))
    print("Student info:", format_student(name="Ali", program="AI"))


if __name__ == "__main__":
    main()
