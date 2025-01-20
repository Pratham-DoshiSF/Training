list1 = ["apple" , "banana","cherry"]
list2 = ["bat" , "cat","dog"]

list3 = list1 + list2
print(f"Example of joining{list3}")

for x in list2:
    list1.append(x)
print(f"Joining Second list at the end {list1}")