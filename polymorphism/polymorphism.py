class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        return f"{self.name} makes a sound."



class Dog(Animal):
    def speak(self):
        return f"{self.name} barks."

class Cat(Animal):
    def speak(self):
        return f"{self.name} meows."

class Cow(Animal):
    def speak(self):
        return f"{self.name} moos."

def animal_sounds(animal):
    print(animal.speak())


dog = Dog("Buddy")
cat = Cat("Whiskers")
cow = Cow("Bessie")

# Call the same function 
animal_sounds(dog)    
animal_sounds(cat)    
animal_sounds(cow) 