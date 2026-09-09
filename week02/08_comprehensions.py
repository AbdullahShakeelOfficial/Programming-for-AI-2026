squares_loop = []
for number in range(1, 21):
    squares_loop.append(number ** 2)

squares_comp = [number ** 2 for number in range(1, 21)]

print("Squares (Loop):", squares_loop)
print("Squares (Comp):", squares_comp)
print("E1 Match:", squares_loop == squares_comp)

print("-" * 50)

evens_loop = []
odds_loop = []
for number in range(1, 51):
    if number % 2 == 0:
        evens_loop.append(number)
    else:
        odds_loop.append(number)

evens_comp = [number for number in range(1, 51) if number % 2 == 0]
odds_comp = [number for number in range(1, 51) if number % 2 != 0]
print("Evens Match:", evens_loop == evens_comp)
print("Odds Match:", odds_loop == odds_comp)