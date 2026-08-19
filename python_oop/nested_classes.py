#----------------------------------------
# Lesson: Nested Classes
# A class can be DEFINED INSIDE another class.
# The inner class is a part of the outer class - it only makes sense
# inside the owner, so it is declared right there in the class body.
#
# Key Concepts:
#   1. Inner Class - Engine is defined inside Car (nested)
#   2. Access Path - nested classes are reached through the outer class:
#      Car.Engine(...) or self.Engine(...) inside the outer class
#   3. Created In __init__ - the outer class builds its inner class
#      parts inside its constructor (composition pattern)
#   4. Inheritance - a child class can OVERRIDE the nested class with
#      its own version (SportsCar.Engine replaces Car.Engine)
#
# ============================================
# NESTED vs OUTER (Why they are different)
# ============================================
# | Outer Class             | Nested (Inner) Class                |
# |-------------------------|--------------------------------------|
# | The owner / container   | The part - declared inside the owner |
# | Reached as Car          | Reached as Car.Engine               |
# | Creates inner parts in  | Cannot be used on its own - it is   |
# | its constructor         | only accessed through the outer     |
# | Can be inherited and    | Can be inherited and overridden too |
# | overridden              | (SportsCar.Engine)                  |
#
# Simple way to remember:
# - Nested class: "The Engine class lives INSIDE the Car class."
# - The inner class is part of the outer class's definition.
# - Creating an inner object is still composition: the part is built
#   inside the owner and dies with it.
#----------------------------------------

class Car:

    def __init__(self, name, model, year, color):
        self.name = name
        self.model = model
        self.year = year
        self.color = color

        # composition: the inner Engine object is created inside the constructor
        self.engine = self.Engine(2000, "Petrol", 4)

    def display_info(self):
        print(f"Car: {self.name} {self.model}")
        print(f"Year: {self.year}")
        print(f"Color: {self.color}")
        # reaching the nested class part through the instance
        self.engine.display_engine_info()


    # Nested Class
    # Engine is declared INSIDE Car - it cannot be used without Car
    class Engine:

        def __init__(self, cc, fuel_type, cylinders):
            self.cc = cc
            self.fuel_type = fuel_type
            self.cylinders = cylinders

        def display_engine_info(self):
            print(f"Engine: {self.cc}cc")
            print(f"Fuel: {self.fuel_type}")
            print(f"Cylinders: {self.cylinders}")


toyota = Car("Toyota", "Supra", 2025, "Black")

toyota.display_info()   



#----------------------------------------
# BONUS: Nested Classes with Inheritance
# A child class can OVERRIDE the parent's nested class.
# SportsCar defines its OWN Engine version, so calling
# SportsCar.Engine gives the child's engine, not the parent's.
#----------------------------------------

class Car:

    def __init__(self, name):
        self.name = name

    class Engine:

        def __init__(self, type):
            self.type = type

        def display(self):
            print(f"Car Engine: {self.type}")


class SportsCar(Car):
    # overriding the nested class - SportsCar has its own Engine
    class Engine:

        def __init__(self, type):
            self.type = type

        def display(self):
            print(f"SportsCar Engine: {self.type}")


# Normal Car
car = Car("Toyota")
# nested class accessed through the outer class: Car.Engine
car_engine = Car.Engine("Petrol")

# Sports Car
sports_car = SportsCar("Supra")
# the child's nested class replaces the parent's: SportsCar.Engine
sports_engine = SportsCar.Engine("V6 Twin Turbo")


car_engine.display()
sports_engine.display()