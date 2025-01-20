f = open("file handling/demofile.txt", "a")
f.write("I live in ahmedabad")
f.close()

f = open("file handling/demofile.txt", "r")
for line in f:
    print(line.strip())  
f.close()
