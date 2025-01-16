# Creating a dictionary
dict1 = {"name": "Alice", "age": 25, "city": "New York"}
print(f"Dictionary used is: {dict1}")

# Length and type of the dictionary
print(f"Length of dictionary: {len(dict1)}")
print(f"Type of dictionary: {type(dict1)}")

# Using the dictionary constructor
thisdict = dict([("name", "Bob"), ("age", 30), ("city", "Los Angeles")])
print(f"This is an example of dictionary constructor: {thisdict}")

# Accessing dictionary items
print(f"Accessing 'name' from dictionary: {dict1['name']}")

# Changing values in a dictionary
dict1["age"] = 26
print(f"Updated dictionary after changing age: {dict1}")

# Adding items to a dictionary
dict1["email"] = "alice@example.com"
print(f"Dictionary after adding email: {dict1}")

# Removing items from a dictionary
del dict1["city"]  # Deletes the 'city' key-value pair
print(f"Dictionary after removing 'city': {dict1}")

# Using pop() to remove an item and return its value
removed_item = dict1.pop("email")
print(f"Removed item: {removed_item}")
print(f"Dictionary after using pop: {dict1}")

# Iterating through keys, values, and items in the dictionary
print("Iterating through dictionary keys:")
for key in dict1:
    print(key)

print("Iterating through dictionary values:")
for value in dict1.values():
    print(value)

print("Iterating through dictionary items (key-value pairs):")
for key, value in dict1.items():
    print(f"{key}: {value}")

# Dictionary methods: copy(), clear(), update()

# Copying a dictionary
dict2 = dict1.copy()
print(f"Copied dictionary: {dict2}")

# Clearing all items in the dictionary
dict1.clear()  # This will remove all key-value pairs
print(f"Dictionary after clear: {dict1}")

# Updating a dictionary with another dictionary
dict2.update({"country": "USA", "job": "Engineer"})
print(f"Dictionary after update: {dict2}")
