def decorator_function(func):
    def wrapper():
        print("Before the function runs")
        func()
        print("After the function runs")
    return wrapper

@decorator_function
def greet():
    print("Hello!")

greet()