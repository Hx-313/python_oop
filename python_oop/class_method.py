#----------------------------------------
# Lesson: Class Methods (@classmethod)
# A class method belongs to the CLASS itself, not to any instance.
# It receives `cls` (the class) instead of `self` (the instance),
# so it can read and modify CLASS attributes - but not instance data.
#
# Key Concepts:
#   1. Decorator @classmethod - marks the method as a class method
#   2. cls Parameter - the first argument is the class itself (cls),
#      automatically passed - you never send it manually
#   3. Called on the Class - call it as Car.create_red(...), not car.create_red(...)
#   4. Used For - alternative constructors (other ways to build an object)
#      and logic that needs to work with class-level data
#
# ============================================
# STATIC vs CLASS METHOD (Why they are different)
# ============================================
# | Static Method           | Class Method (@classmethod)          |
# |-------------------------|---------------------------------------|
# | No self, no cls - like  | Receives `cls` - the class itself    |
# | a plain function        |                                       |
# | Cannot touch class or   | Can read / change CLASS attributes    |
# | instance attributes     | (cls.total_cars)                     |
# | Utility / helper logic  | Alternative constructors and class-  |
# | with no class data      | level operations                      |
# | Class.helper(...)       | Class.build_from_string(...)          |
#
# Simple way to remember:
# - Static method:  "Is this color valid?"   (just a helper)
# - Class method:   "Build a car from a string." (works with the CLASS)
# - cls is to the class what self is to the instance.
#----------------------------------------

class Car:
    total_cars = 0  # class attribute - shared by all instances

    def __init__(self, brand, model, color):
        self.brand = brand
        self.model = model
        self.color = color
        Car.total_cars += 1  # every new car updates the class attribute

    # Class method: alternative constructor
    # Builds a Car object from a single string like "Toyota Camry Red"
    @classmethod
    def from_string(cls, data):
        brand, model, color = data.split()
        return cls(brand, model, color)

    # Class method: works with the class attribute
    @classmethod
    def get_total_cars(cls):
        return f"Total cars created: {cls.total_cars}"

    # Regular method still works on the instance
    def display_info(self):
        print(f"Car: {self.brand} {self.model} - Color: {self.color}")

# Class methods are called on the CLASS
# cls inside from_string is Car, so cls(...) creates a Car
car1 = Car.from_string("Honda Civic Blue")
car1.display_info()

car2 = Car.from_string("Ford Mustang Red")
car2.display_info()

# The class method can see the class attribute
print(Car.get_total_cars())

# Regular construction still works alongside the alternative one
car3 = Car("Toyota", "Camry", "Black")
print(Car.get_total_cars())

# cls is automatically passed - you never send it yourself
print(Car.get_total_cars())
# It can even be called on an instance, but cls still refers to the class
print(car1.get_total_cars())