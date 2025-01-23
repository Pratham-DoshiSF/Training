para = ["(" , ")"]

i = int(input("Enter number : "))
total_length = 2*i
result = []

def generateSequence(  total_length   ,sequance = ""  ):
    if total_length  == 0:
        if sequance[0] == "(" and sequance[-1] == ")" and sequance.count("(") == i:
            result.append(sequance)
    else :
        for element in para:
            generateSequence( total_length  -1 , sequance + element )

generateSequence(total_length)

print(result)









