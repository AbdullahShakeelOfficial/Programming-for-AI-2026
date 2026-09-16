import student_utils

name = "Ayesha"
marks = [78, 86, 91]

average = student_utils.calculate_average(marks)
grade = student_utils.calculate_grade(average)
summary = student_utils.format_summary(name, average, grade)

print(summary)
name2 = "Ali"
marks2 = [62, 74, 58]

average2 = student_utils.calculate_average(marks2)
grade2 = student_utils.calculate_grade(average2)
summary2 = student_utils.format_summary(name2, average2, grade2)

print(summary2)