#----------------------------------------
# Lesson: Polymorphism
# Polymorphism = "many forms" (Greek: poly = many, morph = form).
# The SAME method name (drive) behaves DIFFERENTLY depending on which object calls it.
# You can call the same code on different objects and get object-appropriate behavior.
#
# Key Concepts:
#   1. Same Name, Different Behavior - drive() means different things for Cars vs Bikes
#   2. Method Overriding - each child redefines the parent's method with its own version
#   3. One Loop, Many Types - we call the SAME methods on a list of different objects
#   4. Works with Inheritance - polymorphism builds on top of inheritance (child shares parent's methods)
#
# ============================================
# POLYMORPHISM vs ABSTRACTION (Why they look the same, but serve different purposes)
# ============================================
# Both use abstract methods, so they LOOK similar - but their GOALS are different:
#
# | Abstraction (WHAT to do)        | Polymorphism (HOW to do it differently) |
# |----------------------------------|------------------------------------------|
# | Focuses on HIDING details        | Focuses on CHANGING behavior             |
# | Defines the CONTRACT / rules     | Shows different IMPLEMENTATIONS of it    |
# | "You MUST have a drive() method" | "Your drive() can be YOUR OWN version"   |
# | Vehicle says WHAT methods exist  | Cars/Bikes decide HOW those methods work |
#
# Why they look the same:
# - Both use @abstractmethod and both rely on inheritance.
# - Abstraction FORCES the child to write drive() (the rule).
# - Polymorphism is WHAT HAPPENS AFTER - each child writes drive() DIFFERENTLY,
#   and Python picks the right version at runtime based on the object's type.
#
# Simple way to remember:
# - Abstraction  = the MENU (declares what dishes exist)     -> "drive() exists"
# - Polymorphism = the COOKS (each kitchen cooks it its own way) -> "Cars vs Bikes drive()"
# - Abstraction asks "WHAT should exist?", Polymorphism asks "HOW should each one behave?"
#----------------------------------------

from abc import ABC, abstractmethod

# ============================================
# ABSTRACTION PART (the rules/contract)
# ============================================
# Vehicle defines the CONTRACT: every child MUST have these 3 methods.
# Vehicle itself can never be created - it's just a blueprint (abstract).
class Vehicle(ABC):
    @abstractmethod  # rule: every vehicle MUST have get_vehicle_info()
    def get_vehicle_info(self):
        pass

    @abstractmethod  # rule: every vehicle MUST have drive()
    def drive(self):
        pass

    @abstractmethod  # rule: every vehicle MUST have clean_driving()
    def clean_driving(self):
        pass


# ============================================
# POLYMORPHISM PART (the different behaviors)
# ============================================
# Cars implements the contract - one specific version of drive()
class Cars(Vehicle):
    def __init__(self, brand, model, year, for_sale, color):
        self.brand = brand
        self.model = model
        self.year = year
        self.for_sale = for_sale
        self.color = color

    # Cars' OWN version of get_vehicle_info() (polymorphism = different from Bikes)
    def get_vehicle_info(self):
        return f"{self.brand} {self.model} ({self.year}) - Color: {self.color}, For Sale: {self.for_sale}"

    # Cars' OWN version of drive() - no bike details here
    def drive(self):
        return f"{self.brand} {self.model} is getting driven around {self.year}"

    # Cars' OWN version of clean_driving() - plain driving message
    def clean_driving(self):
        print(f"{self.brand} {self.model} is getting driven around {self.year}")

# Bikes also implements the contract, but with a DIFFERENT version of each method
class Bikes(Vehicle):
    def __init__(self, brand, model, year, for_sale, color):
        self.brand = brand
        self.model = model
        self.year = year
        self.for_sale = for_sale
        self.color = color

    # Bikes' OWN version - adds "two wheels" info (polymorphism in action)
    def get_vehicle_info(self):
        return f"{self.brand} {self.model} ({self.year}) - Color: {self.color}, For Sale: {self.for_sale} and has two wheels"

    # Bikes' OWN version - mentions bike path, wheels, and helmet
    def drive(self):
        return f"{self.brand} {self.model} is getting driven around {self.year} on a bike path with two wheels and a helmet"

    # Bikes' OWN version - prints a bike-specific message
    def clean_driving(self):
        print(f"{self.brand} {self.model} is getting driven around {self.year} on a bike path")

# hayabusa extends Bikes (3rd level) - one MORE version of drive(), via overriding
class hayabusa(Bikes):
    def __init__(self, brand, model, year, for_sale, color, top_speed):
        super().__init__(brand, model, year, for_sale, color)  # reuse Bikes' setup, add top_speed
        self.top_speed = top_speed

    # OVERRIDES Bikes' drive() with a Hayabusa-specific message + top speed
    def drive(self):
        return f"{self.brand} {self.model} is getting driven around {self.year} on a bike path with two wheels and a helmet (Hayabusa version) at speed of {self.top_speed} km/h"


# ============================================
# POLYMORPHISM IN ACTION (the payoff!)
# ============================================
# A list holding THREE DIFFERENT types of objects
vehicle = [Cars("Toyota", "Camry", 2020, True, "blue"), Bikes("Giant", "Defy", 2020, False, "red"), hayabusa("Suzuki", "Hayabusa", 2020, False, "black", 300)]

# One loop, SAME 3 method calls - but each object runs ITS OWN version.
# Python decides at runtime which drive() to use based on the object's class.
for veh in vehicle:
    print(veh.get_vehicle_info())  # each type prints its own info format
    print(veh.drive())             # each type prints its own driving message
    veh.clean_driving()            # each type prints its own driving action
    print()  # Add a blank line for better readability

