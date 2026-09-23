import csv
import json

# ==========================================
# F1. Missing self
# ==========================================
# Error: TypeError: Student.__init__() takes 2 positional arguments but 3 were given.
# Cause: The constructor method was missing the mandatory 'self' parameter.
# Fix: Added 'self' as the first parameter in the __init__ signature.


class Student:

    def __init__(self, name: str, marks: list[float]):
        self.name = name
        self.marks = marks


# ==========================================
# F2. Wrong file mode
# ==========================================
# Error: io.UnsupportedOperation: not writable.
# Cause: Open mode was set to read ("r") instead of write ("w").
# Fix: Changed file mode parameter from "r" to "w".

with open("students.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Ali", 85])


# ==========================================
# F3. Raw object in JSON
# ==========================================
# Error: TypeError: Object of type Model is not JSON serializable.
# Cause: Standard json.dump cannot directly serialize custom Python class instances.
# Fix: Converted the object into a dictionary before serialization.


class Model:

    def __init__(self, name: str):
        self.name = name

    def to_dictionary(self) -> dict:
        return {"name": self.name}


model = Model("ResNet50")
with open("model.json", "w", encoding="utf-8") as file:
    json.dump(model.to_dictionary(), file, indent=4)

print("Debugging corrections executed successfully.")