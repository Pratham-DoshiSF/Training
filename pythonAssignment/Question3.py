# ["eat","tea","tan","ate","nat","bat"]

list_of_string = ["eat","tea","tan","ate","nat","bat"]
sub = {}

for i in list_of_string:
    sorted_element = "".join(sorted(i))

    if sorted_element in sub:
        sub[sorted_element].append(i)
    else :
        sub[sorted_element] = [i]
    

print(list(sub.values()))
    
