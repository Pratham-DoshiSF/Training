cars = ["Ford", "Volvo", "BMW"]

print(f"Printing first element {cars[0]}")

cars.append("Toyota")
print(f"Added toyota {cars}")

cars.pop()
print(f"Popped last element{cars}")


print(f"Lopping through array")
for x in cars :
    print(x)