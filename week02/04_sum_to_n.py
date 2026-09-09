n = int(input("Enter a Positive Integer:"))
if n < 0:
    print("Please Enter Positive Integer")
else:
    total_sum = 0
    for i in range(1, n + 1):
        total_sum += i
    print(f"Sum from 1 to {n} is: {total_sum}")