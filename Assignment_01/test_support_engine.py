from support_engine import classify_support, format_message

# 1. Below attendance boundary
assert classify_support(59.9, 90, 0) == "High priority"

# 2. High missed boundary
assert classify_support(60, 90, 4) == "High priority"

# 3. Below attendance boundary (Moderate)
assert classify_support(74.9, 90, 0) == "Moderate priority"

# 4. Below average boundary
assert classify_support(75, 59.9, 0) == "Moderate priority"

# 5. Moderate missed boundary
assert classify_support(90, 90, 2) == "Moderate priority"

# 6. Minimum routine values
assert classify_support(75, 60, 1) == "Routine monitoring"

# 7. Maximum valid values
assert classify_support(100, 100, 0) == "Routine monitoring"

print("All tests passed.")