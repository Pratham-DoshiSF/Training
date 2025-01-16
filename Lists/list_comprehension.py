# without using list comprehension
list1 = ["apple" , "banana","cherry"]

newlist = []
for x in list1:
    if "a" in x:
        newlist.append(x)

print(newlist)

# using list comprehension

newlist = [x for x in list1 if "a" in x]
print(newlist)