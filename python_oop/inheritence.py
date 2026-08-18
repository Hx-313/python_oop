#----------------------------------------
# Lesson: Inheritance
# Inheritance lets a new class (child) reuse
# the code of an existing class (parent).
# Here Haval inherits everything from Cars.
#
# Key Concepts:
#   1. Parent Class (Cars) - provides the base attributes and methods
#   2. Child Class (Haval) - inherits everything from the parent for free
#   3. super().__init__()  - calls the parent's constructor to reuse its setup
#   4. Method Overriding   - Haval redefines driving() with its own custom message
#----------------------------------------

from cars import Cars # import the parent class from cars.py

class Haval(Cars): # Haval is the child class; (Cars) means it inherits from Cars
    # Haval overrides __init__ so the brand is always "Haval"
    # so the caller doesn't have to type the brand every time
    def __init__(self, model, year, for_sale, color):
        # super().__init__ calls the parent (Cars) __init__,
        # passing "Haval" as the brand automatically
        super().__init__("Haval", model, year, for_sale, color)

    def driving(self):
        return f"Haval {self.model} is getting driven around {self.year} (Haval version)" # overrides the parent method with a custom message
