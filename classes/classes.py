class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def myfunc(self):
        print("My name is " + self.name)


p1 = Person("pratham", 20)

print(p1.name)
print(p1.age)
p1.myfunc()

p1.age = 21
print("updated age " , p1.age)