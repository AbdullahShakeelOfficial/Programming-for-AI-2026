birth_year = int(input("Enter birth year: "))
current_year = int(input("Enter current year: "))

age = current_year - birth_year
print("Approximate age:", age)

# Test 1: birth_year = 2006, current_year = 2026 -> Expected Age: 20
# Test 2: birth_year = 2000, current_year = 2026 -> Expected Age: 26