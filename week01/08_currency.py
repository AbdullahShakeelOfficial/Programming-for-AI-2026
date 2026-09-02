usd_amount = float(input("Enter amount in USD: "))
exchange_rate = float(input("Enter exchange rate (local per USD): "))

converted = usd_amount * exchange_rate
print("Converted amount to PKR:", round(converted, 2))

# Test 1: usd = 25, rate = 280.50 -> Expected: 7012.50
# Test 2: usd = 100, rate = 278.00 -> Expected: 27800.00