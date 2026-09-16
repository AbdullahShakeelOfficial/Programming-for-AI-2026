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


def calculate_average(marks):
    """Return the arithmetic mean of a non-empty marks list."""
    if not marks:
        return 0.0
    return sum(marks) / len(marks)


def format_summary(name, average, grade):
    """Return a formatted single-line summary string."""
    return f"Student: {name} | Average: {average:.2f} | Grade: {grade}"