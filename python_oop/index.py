#----------------------------------------
# Main program: using the Cars and Haval classes
# This is where the objects (actual cars) are created and used.
#----------------------------------------

from cars import Cars        # import the Cars class from cars.py
from inheritence import Haval # import the Haval class from inheritence.py

# Creating an object: Cars(...) runs __init__ and returns a Car instance
car1 = Cars("Haval", "H5", 2020, True, "Mate Black") # a Haval H5, up for sale
car2 = Cars("Toyota", "Camry", 2021, False, "White") # a Toyota Camry, not for sale

# Calling a method on the object: object_name.method_name()
print(car1.get_car_info()) # prints a summary of car1 (Haval H5)

# Haval is a subclass, so it inherits all methods from Cars.
# It only needs 4 arguments because the brand is set automatically.
haval = Haval("H6", 2025, True, "Red") # brand "Haval" is filled in by inheritance

print(haval.driving())       # inherited method: prints the driving message
print(haval.get_car_info())  # inherited method: prints the full info summary
