#----------------------------------------
# Lesson: Implementing Abstract Classes
# This file shows how to use the abstract Vehicle blueprint from abstract_classes.py.
# Cars and Bikes are concrete classes that MUST implement every abstract method.
#
# Key Concepts:
#   1. Concrete Class  - a real class you can create objects from (unlike abstract)
#   2. Implementing    - providing actual code for the abstract methods
#   3. Same Contract, Different Behavior - Cars and Bikes implement the same methods
#      but with vehicle-specific details (e.g., Bikes mention "two wheels")
#----------------------------------------

# Cars is a concrete class that inherits from Vehicle abstract class
# It implements all required abstract methods (get_vehicle_info, drive, clean_driving)
from abstract_classes import Vehicle

class Cars(Vehicle):
        # __init__ initializes all car attributes
        def __init__(self, brand, model, year, for_sale, color):
            self.brand = brand
            self.model = model
            self.year = year
            self.for_sale = for_sale
            self.color = color

        # get_vehicle_info() returns a formatted string with car details
        def get_vehicle_info(self):
            return f"{self.brand} {self.model} ({self.year}) - Color: {self.color}, For Sale: {self.for_sale}"
        
        # drive() returns a driving message (inherited from Vehicle)
        def drive(self):
            return f"{self.brand} {self.model} is getting driven around {self.year}"
        
        # clean_driving() prints the driving action (inherited from Vehicle)
        def clean_driving(self):
            print(f"{self.brand} {self.model} is getting driven around {self.year}")


# Bikes is another concrete class that inherits from Vehicle abstract class
# It implements the same abstract methods but with bike-specific behavior
class Bikes(Vehicle):
        # __init__ initializes all bike attributes (same as Cars)
        def __init__(self, brand, model, year, for_sale, color):
            self.brand = brand
            self.model = model
            self.year = year
            self.for_sale = for_sale
            self.color = color

        # get_vehicle_info() returns bike details with two-wheel info
        def get_vehicle_info(self):
            return f"{self.brand} {self.model} ({self.year}) - Color: {self.color}, For Sale: {self.for_sale} and has two wheels"
        
        # drive() returns a bike-specific driving message
        def drive(self):
            return f"{self.brand} {self.model} is getting driven around {self.year} on a bike path with two wheels and a helmet"
        
        # clean_driving() prints the bike driving action
        def clean_driving(self):
            print(f"{self.brand} {self.model} is getting driven around {self.year} on a bike path")


# Creating instances to test the abstract class implementations
car = Cars("Toyota", "Camry", 2020, True, "blue")
bike = Bikes("Giant", "Defy", 2020, False, "red")

# Testing clean_driving() method from both classes
car.clean_driving()
bike.clean_driving()