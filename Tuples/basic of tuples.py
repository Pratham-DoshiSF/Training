# Creating a tuple
tuple1 = ("apple", "banana", "cherry")
print(f"Tuple used is {tuple1}")

# Length and type of the tuple
print(f"Length of tuple: {len(tuple1)}")
print(f"Type of tuple: {type(tuple1)}")

# Using the tuple constructor
thistuple = tuple(("apple", "banana", "cherry"))
print(f"This is an example of tuple constructor: {thistuple}")

# Accessing tuple items
print(f"Accessing first element of the tuple: {tuple1[0]}")


# tuple concatenation:
tuple1 = tuple1 + ("orange",)
print(f"Example of adding to tuple (by concatenation): {tuple1}")

#joining tuple elements into a string
tuple2 = ("apple", "banana", "cherry")
tuple3 = tuple1 + tuple2 
print(f"Joining two tuple {tuple3}")
