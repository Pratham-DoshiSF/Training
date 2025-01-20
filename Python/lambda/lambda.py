x = lambda a,b : a*b

print(x(4,5))

def myfunc(n):
  return lambda a : a * n

mydoubler = myfunc(2)

print(f"Using lamda in function {mydoubler(11)}")