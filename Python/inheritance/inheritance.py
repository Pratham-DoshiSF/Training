# Base class
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        return f"{self.name} makes a sound."

# Derived class
class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name)
        self.breed = breed

    def speak(self):
        return f"{self.name}, a {self.breed}, barks!"



generic_animal = Animal("Some Animal")
dog = Dog("Buddy", "Golden Retriever")

# Demonstrating method calls
print(generic_animal.speak())  
print(dog.speak())             
