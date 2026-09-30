# ---------------------------------------------------------
# 1. Floating-point (decimal numbers) read karne ka function
# ---------------------------------------------------------
def read_float(prompt, minimum, maximum):
    """
    Yeh function user se ek decimal number (float) input leta hai.
    Jab tak user sahi number aur correct range (minimum se maximum) ke andar
    input nahi deta, yeh repeat (loop) hota rahega.
    """
    while True: # Yeh infinite loop tab tak chalega jab tak return na ho jaye
        user_input = input(prompt) # User se text input lena
        try:
            # Step A: String ko decimal number (float) mein convert karne ki koshish
            value = float(user_input)
            
            # Step B: Check karna ki value range ke andar hai ya nahi
            if minimum <= value <= maximum:
                return value # Agar sahi hai, toh value return karo aur function khatam
            else:
                print(f"Error: Value must be between {minimum} and {maximum}.")
        except ValueError:
            # Agar user ne letters/text type kiya jo float mein convert nahi ho sakta
            print("Error: Invalid input. Please enter a numeric value.")


# ---------------------------------------------------------
# 2. Integer (whole numbers) read karne ka function
# ---------------------------------------------------------
def read_int(prompt, minimum):
    """
    Yeh function user se ek whole number (integer) input leta hai.
    Yeh check karta hai ki input number minimum value se bada ya barabar ho.
    """
    while True:
        user_input = input(prompt)
        try:
            # String ko whole number (int) mein convert karna
            value = int(user_input)
            
            # Check karna ki minimum mark se bada hai ya barabar
            if value >= minimum:
                return value
            else:
                print(f"Error: Value must be {minimum} or greater.")
        except ValueError:
            # Agar user ne float (e.g. 2.5) ya text enter kiya
            print("Error: Invalid input. Please enter a whole number.")


# ---------------------------------------------------------
# 3. Support Category Classify karne ka function
# ---------------------------------------------------------
def classify_support(attendance, assignment_average, missed_submissions):
    """
    Yeh function teen values leta hai aur student ki category determine karta hai.
    Rules ko sequence mein check kiya jata hai (Priority 1, phir 2, phir 3).
    Is function mein koi input() ya print() nahi hota.
    """
    # Priority 1 Rule: Attendance 60% se kam HO ya missed submissions 4 ya zyada ho
    if attendance < 60 or missed_submissions >= 4:
        return "High priority"
    
    # Priority 2 Rule: Attendance 75% se kam HO ya assignment avg 60% se kam HO ya missed >= 2
    elif attendance < 75 or assignment_average < 60 or missed_submissions >= 2:
        return "Moderate priority"
    
    # Priority 3 Rule: Agar upar wala koi rule match nahi hua
    else:
        return "Routine monitoring"


# ---------------------------------------------------------
# 4. Message format karne ka function
# ---------------------------------------------------------
def format_message(category):
    """
    Yeh function category name leta hai aur uske hisab se 
    advisory message text return karta hai.
    """
    if category == "High priority":
        return "Immediate academic support is recommended."
    elif category == "Moderate priority":
        return "Monitor progress and provide targeted guidance."
    elif category == "Routine monitoring":
        return "Continue routine monitoring."
    else:
        return "Unknown category."


# ---------------------------------------------------------
# 5. Main Execution Flow
# ---------------------------------------------------------
def main():
    """
    Yeh main function hai jo poore program ke steps ko run karta hai.
    """
    print("--- Student Support Rule Engine ---")
    
    # Step 1: User se teeno values input lena (Validation ke saath)
    attendance = read_float("Attendance percentage: ", 0, 100)
    assignment_average = read_float("Assignment average: ", 0, 100)
    missed_submissions = read_int("Missed submissions: ", 0)
    
    # Step 2: Category determine karna function call karke
    category = classify_support(attendance, assignment_average, missed_submissions)
    
    # Step 3: Advisory message get karna function call karke
    advisory = format_message(category)
    
    # Step 4: Output screen par display karna
    print(f"Support category: {category}")
    print(f"Advisory: {advisory}")


# ---------------------------------------------------------
# Entry Point Check
# ---------------------------------------------------------
# `__name__` ek internal Python variable hai.
# Jab hum script ko direct run karte hain (`python support_engine.py`),
# toh `__name__` ki value `"__main__"` hoti hai.
# Iska faida yeh hai ki jab test file is script se functions import karegi,
# toh main() automatic execute nahi hoga.
if __name__ == "__main__":
    main()