#----------------------------------------
# Lesson: The super() Method
# super() is used inside a child class to call a method from its PARENT class.
# It lets the child reuse the parent's setup instead of rewriting it.
#
# Key Concepts:
#   1. super().__init__(...) - calls the parent's constructor to set shared attributes
#   2. Reusing Parent Code   - the child adds its OWN attributes on top of the parent's
#   3. DRY Principle         - Don't Repeat Yourself: brand/model/year are set once in Cars
#   4. MRO (Method Resolution Order) - Python finds the right parent automatically
#----------------------------------------

# Cars is the base (parent) class - it holds attributes shared by ALL vehicles
class Cars:
    # Parent constructor: sets the common attributes every car needs
    def __init__(self, brand, model, year, for_sale, color):
        self.brand = brand
        self.model = model
        self.year = year
        self.for_sale = for_sale
        self.color = color
    def display_info(self):
        print(f"{self.brand} {self.model} ({self.year}) - Color: {self.color}, For Sale: {self.for_sale}")

# LuxuryVehicle is a child of Cars - it inherits all car attributes via super()
class LuxuryVehicle(Cars):
    # Child constructor: uses super() to let the parent handle the common attributes
    # then adds its OWN extra attribute (luxury_features) on top
    def __init__(self, brand, model, year, for_sale, color, luxury_features):
        super().__init__(brand, model, year, for_sale, color)  # super() = run Cars.__init__() for us
        self.luxury_features = luxury_features  # new attribute only LuxuryVehicle has

    # display_info() shows the inherited car details plus the luxury features
    def display_info(self):
        super().display_info()
        print(f"Luxury Features: {', '.join(self.luxury_features)}")  # join() turns the list into a comma-separated string


# SportsVehicle is another child of Cars - same super() pattern, different extra attribute
class SportsVehicle(Cars):
    # Child constructor: super() sets the shared attributes, then top_speed is added
    def __init__(self, brand, model, year, for_sale, color, top_speed):
        super().__init__(brand, model, year, for_sale, color)  # super() = run Cars.__init__() for us
        self.top_speed = top_speed  # new attribute only SportsVehicle has

    # display_info() shows the inherited car details plus the top speed
    def display_info(self):
        super().display_info()
        print(f"Top Speed: {self.top_speed} km/h")


class Hatchback(Cars):
    # Child constructor: super() sets the shared attributes, then cargo_space is added
    def __init__(self, brand, model, year, for_sale, color, cargo_space):
        super().__init__(brand, model, year, for_sale, color)  # super() = run Cars.__init__() for us
        self.cargo_space = cargo_space  # new attribute only Hatchback has

    # display_info() shows the inherited car details plus the cargo space
    def display_info(self):
        super().display_info()
        print(f"Cargo Space: {self.cargo_space} liters")

class SUV(Cars):
    # Child constructor: super() sets the shared attributes, then offroad_capability is added
    def __init__(self, brand, model, year, for_sale, color, offroad_capability):
        super().__init__(brand, model, year, for_sale, color)  # super() = run Cars.__init__() for us
        self.offroad_capability = offroad_capability  # new attribute only SUV has

    # display_info() shows the inherited car details plus the off-road capability
    def display_info(self):
        super().display_info()
        print(f"Off-Road Capability: {self.offroad_capability}")

# Creating a SportsVehicle - only 6 args needed because super() handles the shared setup
supra = SportsVehicle("Toyota", "Supra", 2020, True, "red", 250)
supra.display_info()

# Creating a LuxuryVehicle - same pattern, adds its luxury features
lambo = LuxuryVehicle("Lamborghini", "Aventador", 2021, False, "yellow", ["Leather Seats", "Sunroof"])
lambo.display_info()

# Creating a Hatchback - same pattern, adds its cargo space
grande = Hatchback("Hyundai", "Grandeur", 2022, True, "white", 500)
grande.display_info()

# Creating an SUV - same pattern, adds its off-road capability
terrain = SUV("Jeep", "Wrangler", 2022, True, "black", "All-Terrain")   
terrain.display_info()