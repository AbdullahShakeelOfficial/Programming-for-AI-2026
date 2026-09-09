marks = [78, 65, 92, 85, 48, 91]

passing = [m for m in marks if m >= 50]
failing = [m for m in marks if m < 50]

average = sum(marks) / len(marks)
highest = max(marks)
lowest = min(marks)

print("Passing:", passing)
print("Failing:", failing)
print("Average:", average)
print("Highest:", highest)
print("Lowest:", lowest)