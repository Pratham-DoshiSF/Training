list1 = ["apple" , "banana","cherry"]
print(f"List used is {list1}")
print(len(list1))
print(type(list1))

#using list constructor

thislist  = list(("apple" , "banana","cherry"))
print(f"This is example of constructor {thislist}")

#access list 

print(list1[0])

#change in list 
list1[1] = "mango"
print(f"Example pf change in list{list1}")


#add to list
list1.append("orange")
print(f"Example of adding to list {list1}")

#remove list items
list1.pop()
print(f"Example of removing last element {list1}")

# sorting
list1.sort(reverse=True)
print(f"Using sorting {list1}")