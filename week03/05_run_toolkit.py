from student_toolkit import generate_summary, parse_marks, save_report


def main():
    name = input("Enter student name: ").strip()
    marks_text = input("Enter marks (comma-separated, e.g. 78, 65, 92): ")

    try:
        marks = parse_marks(marks_text)
        report = generate_summary(name, marks)

        print("\n" + report)

        # Save to text file inside week03
        output_file = "week03/student_report.txt"
        save_report(output_file, report)
        print(f"Report successfully saved to {output_file}")

    except ValueError as error:
        print("Invalid marks input:", error)


if __name__ == "__main__":
    main()