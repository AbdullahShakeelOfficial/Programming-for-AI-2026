import csv
from pathlib import Path
from student import Student


def load_students(file_path: Path | str) -> list[Student]:
    """Loads student records from a CSV file into Student instances."""
    students = []
    path = Path(file_path)

    try:
        with path.open("r", encoding="utf-8", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                marks = [
                    float(row["mark1"]),
                    float(row["mark2"]),
                    float(row["mark3"]),
                ]
                clean_sap = row["sap_id"].strip()
                clean_name = row["name"].strip()
                students.append(Student(clean_sap, clean_name, marks))
    except FileNotFoundError:
        print(f"Error: Missing CSV file at '{path}'. Check if data/students.csv exists.")
    except ValueError as e:
        print(f"Error processing CSV row data: {e}")
    except PermissionError:
        print(f"Error: Insufficient permissions to read '{path}'.")

    return students


def save_student_report(student: Student, file_path: Path | str) -> None:
    """Saves formatted individual student report to disk."""
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    try:
        report_text = (
            f"SAP ID: {student.sap_id}\n"
            f"Student Name: {student.name}\n"
            f"Average Score: {student.calculate_average():.2f}\n"
            f"Letter Grade: {student.calculate_grade()}\n"
        )
        with path.open("w", encoding="utf-8") as file:
            file.write(report_text)
    except PermissionError:
        print(f"Error: Unable to write report to '{path}' due to permissions.")


def main():
    lab_folder = Path(__file__).resolve().parent
    csv_path = lab_folder / "data" / "students.csv"

    students = load_students(csv_path)
    if not students:
        print("No student records loaded.")
        return

    print(f"Loaded {len(students)} students from CSV:\n")
    total_avg = 0.0

    for st in students:
        print(st.format_profile())
        total_avg += st.calculate_average()

        # Save individual report named after student SAP ID
        report_file = lab_folder / "reports" / f"{st.sap_id}.txt"
        save_student_report(st, report_file)

    class_avg = total_avg / len(students)
    print(f"\nOverall Class Average: {class_avg:.2f}")

    # Read and display saved text reports to confirm creation
    print("\n--- Displaying Saved Reports ---")
    for st in students:
        report_file = lab_folder / "reports" / f"{st.sap_id}.txt"
        if report_file.exists():
            print(f"\n[Report File: {report_file.name}]")
            print(report_file.read_text(encoding="utf-8").strip())


if __name__ == "__main__":
    main()