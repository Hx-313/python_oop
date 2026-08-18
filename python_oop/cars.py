#----------------------------------------
# Lesson: Classes (Object Oriented Programming)
# A class is a blueprint for creating objects.
# Each object created from this class is a Car.
#
# Key Concepts:
#   1. Class Attribute  - belongs to the class, shared by ALL objects (working_year, cars_created)
#   2. Instance Attribute - belongs to ONE object, set in __init__ (brand, model, year, etc.)
#   3. Constructor (__init__) - runs automatically when a new object is created
#   4. Methods - functions inside a class that act on the object's data
#----------------------------------------

class Cars:

    working_year = 2026 # class attribute: shared by ALL car objects
    cars_created  = 0   # class attribute: counts how many cars were made

    # __init__ is the constructor, called automatically when a new object is created.
    # "self" refers to the specific object being created/used.
    def __init__(self, brand, model, year, for_sale, color):
        self.brand = brand       # instance attribute: stored on THIS car only
        self.model = model       # instance attribute
        self.year = year         # instance attribute
        self.for_sale = for_sale # instance attribute
        self.color = color       # instance attribute
        Cars.cars_created += 1   # increase the class counter each time a car is made

    # A method is a function that belongs to a class.
    # It returns a formatted message about this car being driven
    def driving(self):
        return f"{self.brand} {self.model} is getting driven around {self.year}" # f-string: injects variable values into the text


    def clean_driving(self):
        print( f"{self.brand} {self.model} is getting driven around {self.year}")



    # This method returns a full summary of the car
    def get_car_info(self):
        return f"{self.brand} {self.model} ({self.year}) - Color: {self.color}, For Sale: {self.for_sale}, Working year: {Cars.working_year}, Cars Created so far: {Cars.cars_created}" # combines instance + class attributes


    def clean_car_info(self):
        print(f"{self.brand} {self.model} ({self.year}) - Color: {self.color}, For Sale: {self.for_sale}, Working year: {Cars.working_year}, Cars Created so far: {Cars.cars_created}")