class Student:
    """Represents a student with validated marks and grade evaluation."""

    def __init__(self, sap_id: str, name: str, marks: list[float]):
        self.sap_id = str(sap_id)
        self.name = str(name)
        self._marks = []
        self.set_marks(marks)

    def set_marks(self, marks: list[float]) -> None:
        """Sets internal marks after validating list size and score bounds."""
        if not marks:
            raise ValueError("Marks list cannot be empty.")
        for m in marks:
            if not (0 <= m <= 100):
                raise ValueError(f"Mark {m} is outside the valid range (0-100).")
        self._marks = list(marks)

    def get_marks(self) -> list[float]:
        """Returns a copy of the internal marks list to prevent mutation."""
        return self._marks.copy()

    def calculate_average(self) -> float:
        """Calculates the average score across all marks."""
        return sum(self._marks) / len(self._marks)

    def calculate_grade(self) -> str:
        """Returns letter grade based on boundary thresholds."""
        avg = self.calculate_average()
        if avg >= 85:
            return "A"
        elif avg >= 70:
            return "B"
        elif avg >= 60:
            return "C"
        elif avg >= 50:
            return "D"
        else:
            return "F"

    def format_profile(self) -> str:
        """Returns a human-readable summary profile."""
        avg = self.calculate_average()
        grade = self.calculate_grade()
        return f"SAP ID: {self.sap_id} | Name: {self.name} | Avg: {avg:.2f} | Grade: {grade}"


if __name__ == "__main__":
    # Test cases: Valid, Boundaries, Encapsulation
    s1 = Student("70123", "Ayesha", [78, 86, 91])
    s2 = Student("70124", "Hamza", [65, 72, 69])
    s3 = Student("70125", "Sara", [88, 92, 84])

    print("--- Student Profiles ---")
    print(s1.format_profile())
    print(s2.format_profile())
    print(s3.format_profile())

    # Verify encapsulation (mutating returned copy does not affect object)
    st_marks = s1.get_marks()
    st_marks.append(999)
    assert len(s1.get_marks()) == 3, "Encapsulation failed: internal state was mutated!"
    print("\nEncapsulation check passed successfully.")