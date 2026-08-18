#----------------------------------------
# Lesson: Abstract Classes in Python
# An Abstract Class is a blueprint (template) that CANNOT be instantiated directly.
# It defines WHAT methods a child class MUST have, but not HOW they work.
#
# Key Concepts:
#   1. ABC  - Abstract Base Class (from the 'abc' module)
#   2. @abstractmethod - marks a method as required; children MUST implement it
#   3. Blueprint Only  - Vehicle can't be created directly, only its children (Cars, Bikes)
#   4. Contract - every child must provide its own get_vehicle_info(), drive(), clean_driving()
#----------------------------------------

from abc import ABC, abstractmethod

# Vehicle is an Abstract Base Class (ABC) that defines the blueprint for all vehicles
# Any class that inherits from Vehicle MUST implement all abstract methods
class Vehicle(ABC):
    # get_vehicle_info() is an abstract method - child classes must provide their own implementation
    @abstractmethod
    def get_vehicle_info(self):
        pass
    
    # drive() is an abstract method - defines the driving behavior that children must implement
    @abstractmethod
    def drive(self):
        pass
    
    # clean_driving() is an abstract method - prints the driving action
    @abstractmethod
    def clean_driving(self):
        pass