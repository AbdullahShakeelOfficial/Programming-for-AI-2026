def main():
    try:
        age = int(input("Age: "))
        print("Age recorded:", age)
    except ValueError:
        print("Enter a whole number.")

    print("-" * 40)

    try:
        numerator = float(input("Numerator: "))
        denominator = float(input("Denominator: "))
        result = numerator / denominator
    except ValueError:
        print("Enter numeric values only.")
    except ZeroDivisionError:
        print("The denominator cannot be zero.")
    else:
        print("Result:", result)

if __name__ == "__main__":
    main()