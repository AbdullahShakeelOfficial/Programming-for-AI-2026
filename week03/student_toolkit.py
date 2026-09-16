from student_utils import calculate_average, calculate_grade


def parse_marks(text):
    """Convert comma-separated text into a validated list of marks."""
    if not text.strip():
        raise ValueError("Enter at least one mark.")

    parts = text.split(",")
    marks = []

    for part in parts:
        if not part.strip():
            raise ValueError("A mark is missing between commas.")

        mark = float(part.strip())

        if mark < 0 or mark > 100:
            raise ValueError("Every mark must be between 0 and 100.")

        marks.append(mark)

    return marks


def generate_summary(name, marks):
    """Return a multi-line report containing student details and performance."""
    avg = calculate_average(marks)
    grade = calculate_grade(avg)

    return (
        f"========================================\n"
        f"         STUDENT ANALYTICS REPORT       \n"
        f"========================================\n"
        f"Student Name : {name}\n"
        f"Marks List   : {marks}\n"
        f"Class Average: {avg:.2f}\n"
        f"Final Grade  : {grade}\n"
        f"========================================\n"
    )


def save_report(filename, report):
    """Write the summary report to a UTF-8 text file."""
    with open(filename, "w", encoding="utf-8") as file:
        file.write(report)