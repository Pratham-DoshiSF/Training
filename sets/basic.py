# Creating a set
set1 = {"apple", "banana", "cherry"}
print(f"Set used is {set1}")

# Length and type of the set
print(f"Length of set: {len(set1)}")
print(f"Type of set: {type(set1)}")

# Using the set constructor
thisset = set(("apple", "banana", "cherry"))
print(f"set constructor: {thisset}")

# We can loop through the set to access items
print("elements in the set:")
for item in set1:
    print(item)

# Adding to a set
set1.add("orange")  # Adds a single element
print(f"adding to set: {set1}")

# Adding multiple elements using update
set1.update(["mango", "grape"])
print(f"adding multiple items to set: {set1}")

# Removing items from a set
set1.remove("banana")  # Removes a specific item
print(f"removing 'banana' from the set: {set1}")

# Pop an item from the set (removes and returns an arbitrary element)
removed_item = set1.pop()
print(f"Item removed using pop: {removed_item}")
print(f"Set after pop: {set1}")

# Checking membership
print(f"Is 'apple' in set? {'apple' in set1}")
print(f"Is 'banana' in set? {'banana' in set1}")

# Union of two sets (combines all unique elements from both sets)
set2 = {"cherry", "pear", "melon"}
union_set = set1.union(set2)
print(f"Union of sets: {union_set}")

# Intersection of two sets (common elements)
intersection_set = set1.intersection(set2)
print(f"Intersection of sets: {intersection_set}")

# Difference of two sets (elements in set1 but not in set2)
difference_set = set1.difference(set2)
print(f"Difference of sets (set1 - set2): {difference_set}")
