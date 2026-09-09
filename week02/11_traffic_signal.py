density = input("Enter traffic density (low, medium, high): ")
emergency = input("Is an emergency vehicle present? (yes/no): ")

if emergency == "yes":
    print("Emergency override: route receives immediate green.")
else:
    if density == "low":
        print("Green light time: 20 seconds")
    elif density == "medium":
        print("Green light time: 40 seconds")
    elif density == "high":
        print("Green light time: 60 seconds")
    else:
        print("Error: Unrecognized traffic density entered.")