def gen(a):
    for i in range(1, a):
        yield i
    
for i in gen(5):
    print(i)