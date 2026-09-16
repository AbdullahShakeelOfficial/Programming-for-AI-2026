import student_utils

assert student_utils.calculate_grade(100) == "A"
assert student_utils.calculate_grade(85) == "A"
assert student_utils.calculate_grade(84) == "B"
assert student_utils.calculate_grade(70) == "B"
assert student_utils.calculate_grade(69) == "C"
assert student_utils.calculate_grade(60) == "C"
assert student_utils.calculate_grade(59) == "D"
assert student_utils.calculate_grade(50) == "D"
assert student_utils.calculate_grade(49) == "F"
assert student_utils.calculate_grade(0) == "F"

assert student_utils.calculate_average([60, 70, 80]) == 70.0
assert student_utils.calculate_average([100, 100]) == 100.0
assert student_utils.calculate_average([]) == 0.0

print("All assertion checks passed successfully!")