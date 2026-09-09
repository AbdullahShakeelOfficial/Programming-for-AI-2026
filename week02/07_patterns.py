rows = int(input("Enter number of rows: "))
if rows <= 0:
    print("Please enter a positive number.")
else:
    print("\n--- Pattern 1: Increasing ---")
    for i in range(1, rows + 1):
        for j in range(i):
            print("*", end="")
        print()

    print("\n--- Pattern 2: Decreasing ---")
    for i in range(rows, 0, -1):
        for j in range(i):
            print("*", end="")
        print()