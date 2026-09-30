# support_engine.py file se sirf `classify_support` function ko import karna
from support_engine import classify_support

# ---------------------------------------------------------
# Assertions (Automated Testing)
# ---------------------------------------------------------
# `assert` statement check karta hai ki condition True hai ya nahi.
# Agar condition True hai, toh kuch print nahi hota (silent pass).
# Agar False hui, toh program AssertionError throw karke ruk jayega.

# Test 1: Attendance boundary check (< 60) -> High priority
assert classify_support(59.9, 90, 0) == "High priority"

# Test 2: Missed submissions boundary check (>= 4) -> High priority
assert classify_support(60, 90, 4) == "High priority"

# Test 3: Attendance boundary check (< 75) -> Moderate priority
assert classify_support(74.9, 90, 0) == "Moderate priority"

# Test 4: Average boundary check (< 60) -> Moderate priority
assert classify_support(75, 59.9, 0) == "Moderate priority"

# Test 5: Missed submissions boundary check (>= 2) -> Moderate priority
assert classify_support(90, 90, 2) == "Moderate priority"

# Test 6: Safe threshold values -> Routine monitoring
assert classify_support(75, 60, 1) == "Routine monitoring"

# Test 7: Maximum valid inputs -> Routine monitoring
assert classify_support(100, 100, 0) == "Routine monitoring"

# Agar saare assertions pass ho jayein, tab yeh line chalegi
print("All tests passed.")