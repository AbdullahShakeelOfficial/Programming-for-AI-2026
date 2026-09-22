def read_float(prompt, minimum, maximum):
    """Read and return a valid floating-point value."""
    while True:
        user_input = input(prompt)
        try:
            value = float(user_input)
            if minimum <= value <= maximum:
                return value
            else:
                print(f"Error: Value must be between {minimum} and {maximum}.")
        except ValueError:
            print("Error: Invalid input. Please enter a numeric value.")


def read_int(prompt, minimum):
    """Read and return a valid integer value."""
    while True:
        user_input = input(prompt)
        try:
            value = int(user_input)
            if value >= minimum:
                return value
            else:
                print(f"Error: Value must be {minimum} or greater.")
        except ValueError:
            print("Error: Invalid input. Please enter a whole number.")


def classify_support(attendance, assignment_average, missed_submissions):
    """Return the student support-priority category."""
    if attendance < 60 or missed_submissions >= 4:
        return "High priority"
    elif attendance < 75 or assignment_average < 60 or missed_submissions >= 2:
        return "Moderate priority"
    else:
        return "Routine monitoring"


def format_message(category):
    """Return an advisory message for the category."""
    if category == "High priority":
        return "Immediate academic support is recommended."
    elif category == "Moderate priority":
        return "Monitor progress and provide targeted guidance."
    elif category == "Routine monitoring":
        return "Continue routine monitoring."
    else:
        return "Unknown category."


def main():
    """Run the student support rule engine."""
    print("--- Student Support Rule Engine ---")
    
    # 1. Read and validate the three required inputs.
    attendance = read_float("Attendance percentage: ", 0, 100)
    assignment_average = read_float("Assignment average: ", 0, 100)
    missed_submissions = read_int("Missed submissions: ", 0)
    
    # 2. Call classify_support().
    category = classify_support(attendance, assignment_average, missed_submissions)
    
    # 3. Call format_message().
    advisory = format_message(category)
    
    # 4. Display the category and advisory message.
    print(f"Support category: {category}")
    print(f"Advisory: {advisory}")


if __name__ == "__main__":
    main()