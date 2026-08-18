#----------------------------------------
# Lesson: Inheritance
# Inheritance lets a new class (child) reuse
# the code of an existing class (parent).
# Here Haval inherits everything from Cars.
#----------------------------------------

from cars import Cars # import the parent class from cars.py

class Haval(Cars): # Haval is the child class; (Cars) means it inherits from Cars
    # Haval overrides __init__ so the brand is always "Haval"
    # so the caller doesn't have to type the brand every time
    def __init__(self, model, year, for_sale, color):
        # super().__init__ calls the parent (Cars) __init__,
        # passing "Haval" as the brand automatically
        super().__init__("Haval", model, year, for_sale, color)
