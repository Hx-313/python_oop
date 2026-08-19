#----------------------------------------
# Lesson: Static Methods (@staticmethod)
# A static method belongs to the CLASS, not to any instance.
# It does NOT receive `self` or `cls` - so it cannot access or modify
# instance attributes, and it cannot access class attributes directly.
#
# Key Concepts:
#   1. Decorator @staticmethod - marks the method as static
#   2. No Self - the method has no `self` parameter, so it works like
#      a normal function that just lives inside the class
#   3. Called on the Class - call it as Car.helper(...), not car.helper(...)
#      (it CAN be called on an instance too, but it ignores it)
#   4. Used For - utility / helper logic that relates to the class
#      concept but does not need instance data
#
# ============================================
# REGULAR vs STATIC METHOD (Why they are different)
# ============================================
# | Regular Method           | Static Method (@staticmethod)      |
# |--------------------------|------------------------------------|
# | Receives `self`          | Receives nothing extra - no self,  |
# | (the instance)           | no cls                             |
# | Can read / change the    | Cannot touch instance data at all  |
# | instance attributes      |                                    |
# | Called as obj.method()   | Called as Class.method()           |
# | Performs work tied to    | Utility / helper logic, like a     |
# | one specific object      | standalone function in the class   |
#
# Simple way to remember:
# - Regular method: "What can THIS car do?"        (needs the instance)
# - Static method:  "Is this a valid car color?"   (just a helper, no instance needed)
#----------------------------------------

class Car:
    # Static method: a helper that belongs to the class concept
    @staticmethod
    def is_valid_color(color):
        # No self, no cls - just plain logic using the arguments
        valid_colors = ["red", "blue", "black", "white", "green", "grey"]
        return color.lower() in valid_colors

    # Static method: another utility helper
    @staticmethod
    def calculate_speed(distance, time):
        # Works like a normal function - takes inputs, returns a result
        if time <= 0:
            return "Time must be greater than zero"
        return distance / time

    def __init__(self, brand, model, color):
        self.brand = brand
        self.model = model
        # Use the static helper INSIDE the constructor for validation
        if Car.is_valid_color(color):
            self.color = color
        else:
            self.color = "unknown"

    def display_info(self):
        print(f"Car: {self.brand} {self.model} - Color: {self.color}")

# Static methods are called on the CLASS, not on an instance
print(Car.is_valid_color("Red"))        # True - the helper validates without an instance
print(Car.is_valid_color("purple"))     # False - not in the valid colors list

# A static method is just a function - pass arguments, get a result
print(f"Speed: {Car.calculate_speed(100, 2)} km/h")

# You CAN call it through an instance, but it still gets no self
car = Car("Toyota", "Camry", "purple")  # purple is invalid -> color becomes "unknown"
car.display_info()
print(car.is_valid_color("blue"))       # works, but it is really a class helper