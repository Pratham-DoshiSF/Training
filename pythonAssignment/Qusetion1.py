word_to_digit = {
    "zero": "0", "one": "1", "two": "2", "three": "3",
    "four": "4", "five": "5", "six": "6", "seven": "7",
    "eight": "8", "nine": "9"
}

def convert_to_numbers(i):
    total_len = len(i)
    num = ""
    start = 0
    end= 0

    while (end<=total_len):
        word = i[start:end]
        if word in word_to_digit:
            num += word_to_digit[word]
            
            if end == total_len:
                return num
            start = end
            end = +1
        
        end+=1

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

i = input('Enter First Number : ').lower().replace(" ","")
j = input("Enter Second Number : ").lower().replace(" ","")

if i.isalpha() and j.isalpha():

    i = convert_to_numbers(i)
    j = convert_to_numbers(j)
    
    if i is None or j is None:
        print("Invlid input ")

    else:
        i = int(i)
        j = int(j)
        if i< j:
            num = j
            j = i
            i = num

        print("Gcd of given two number is " , gcd(i,j))


else:
    print("Input Should be in word")