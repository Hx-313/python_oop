#----------------------------------------
# Lesson: Multiple Inheritance in Python
# Multiple Inheritance = a class inherits from TWO or more parent classes.
# This lets a child class combine behaviors from multiple sources.
#
# Inheritance Chain:
#   Cars (base class)
#    ├── SportsVehicle   (single inheritance from Cars)
#    │    ├── Ferrari    (single inheritance from SportsVehicle)
#    │    └── Toyota     (multiple inheritance from SportsVehicle AND LuxuryVehicle)
#    └── LuxuryVehicle   (single inheritance from Cars)
#         ├── Haval      (single inheritance from LuxuryVehicle)
#         └── Toyota     (multiple inheritance from SportsVehicle AND LuxuryVehicle)
#
# Key Concepts:
#   1. super().__init__()  - calls the PARENT's constructor to reuse its setup
#   2. Method Inheritance  - child gets parent's methods (e.g., driving())
#   3. Method Overriding   - child can redefine a parent's method with its own version
#   4. Multiple Inheritance - class inherits from 2+ parents (Toyota example)
#----------------------------------------

from cars import Cars

# ============================================
# SINGLE INHERITANCE EXAMPLES
# ============================================

# SportsVehicle inherits from Cars.
# It adds a new attribute (top_speed) on top of everything Cars provides.
class SportsVehicle(Cars):
    # __init__ adds 'top_speed' to the parent's attributes
    def __init__(self, name, model, year, for_sale, color, top_speed):
        super().__init__(name, model, year, for_sale, color)  # super() = call Cars.__init__() to set brand, model, year, etc.
        self.top_speed = top_speed  # new attribute only SportsVehicle has

    # sports_info() calls parent's get_car_info() then adds its own output
    def sports_info(self):
        Cars.get_car_info(self)  # explicitly calling parent method
        print(f"{self.brand} {self.model} ({self.year}) - Color: {self.color}, For Sale: {self.for_sale}")
        print(f"Top Speed: {self.top_speed} km/h")

    # nitro_boost() adds 50 km/h to top speed for a temporary speed burst
    def nitro_boost(self):
        print(f"{self.brand} {self.model} is using nitro boost to reach {self.top_speed + 50} km/h!")


# LuxuryVehicle also inherits from Cars.
# It adds luxury_features (a list of special features).
class LuxuryVehicle(Cars):
    # __init__ adds 'luxury_features' list to the parent's attributes
    def __init__(self, name, model, year, for_sale, color, luxury_features):
        super().__init__(name, model, year, for_sale, color)
        self.luxury_features = luxury_features  # list of features like ["Leather Seats", "Sunroof"]

    # luxury_info() calls parent's get_car_info() then adds luxury features
    def luxury_info(self):
        Cars.get_car_info(self)
        print(f"{self.brand} {self.model} ({self.year}) - Color: {self.color}, For Sale: {self.for_sale}")
        print(f"Luxury Features: {', '.join(self.luxury_features)}")  # join() turns list into comma-separated string

    # activate_luxury_mode() displays all luxury features being activated
    def activate_luxury_mode(self):
        print(f"{self.brand} {self.model} is activating luxury mode with features: {', '.join(self.luxury_features)}")


# ============================================
# MULTILEVEL INHERITANCE (3 levels deep)
# ============================================

# Haval inherits from LuxuryVehicle (which inherits from Cars).
# So Haval has access to ALL methods: luxury_info(), get_car_info(), driving()
# 'pass' means we don't add anything new - it uses everything from the parent as-is.
class Haval(LuxuryVehicle):
    # ev_mode() switches the vehicle to silent electric driving mode
    def ev_mode(self):
        print(f"{self.brand} {self.model} is now in electric mode, silently gliding down the road.")

# Ferrari inherits from SportsVehicle (which inherits from Cars).
# Same idea - it gets sports_info(), get_car_info(), driving() for free.
class Ferrari(SportsVehicle):
    # drag_race() simulates a high-speed track race
    def drag_race(self):
        print(f"{self.brand} {self.model} is racing down the track at {self.top_speed} km/h!")


# ============================================
# MULTIPLE INHERITANCE (the main topic!)
# ============================================

# Toyota inherits from BOTH SportsVehicle AND LuxuryVehicle.
# This means it gets top_speed (from SportsVehicle) AND luxury_features (from LuxuryVehicle).
#
# WHY DOES THIS MATER?
# - We can combine two different "categories" into one car
# - Toyota Supra is BOTH sporty AND luxurious
#
# NOTE: We can't use super().__init__() here because it would only call ONE parent.
# Instead, we call Cars.__init__() directly and set both attributes manually.
class Toyota(SportsVehicle, LuxuryVehicle):
    # __init__ sets both sport and luxury attributes (skips both parents)
    def __init__(self, name, model, year, for_sale, color, top_speed, luxury_features):
        Cars.__init__(self, name, model, year, for_sale, color)  # skip both parents, go straight to grandparent
        self.top_speed = top_speed            # from SportsVehicle
        self.luxury_features = luxury_features  # from LuxuryVehicle

    # Custom method that displays BOTH sport and luxury info
    def display_info(self):
        print(f"{self.brand} {self.model} ({self.year}) - Color: {self.color}, For Sale: {self.for_sale}")
        print(f"Top Speed: {self.top_speed} km/h")
        print(f"Luxury Features: {', '.join(self.luxury_features)}")


# ============================================
# CREATING OBJECTS (instances)
# ============================================

# Haval H6 - a luxury SUV (inherits from LuxuryVehicle -> Cars)
h6 = Haval("Haval", "H6", 2022, False, "white", ["Leather Seats", "Sunroof", "Advanced Infotainment"])

# Ferrari 488 GTB - a sports car (inherits from SportsVehicle -> Cars)
ferrari = Ferrari("Ferrari", "488 GTB", 2021, True, "red", 330)

# Toyota Supra - BOTH sporty AND luxurious (inherits from SportsVehicle AND LuxuryVehicle)
supra = Toyota("Toyota", "Supra", 2023, False, "blue", 250, ["Adaptive Cruise Control", "Premium Audio System"])

# Lexus LC 00 - same class, different data
lexus = Toyota("Lexus", "LC 500", 2022, True, "black", 270, ["Heated Seats", "Heads-Up Display"])


# ============================================
# TESTING OUR OBJECTS
# ============================================

# h6 is a LuxuryVehicle, so it has luxury_info() and driving() (from Cars)
h6.luxury_info()
h6.driving()
h6.activate_luxury_mode()
h6.ev_mode()
print("\n")

# ferrari is a SportsVehicle, so it has sports_info()
ferrari.sports_info()
ferrari.nitro_boost()
ferrari.drag_race()

print("\n")

# supra and lexus are Toyota (multiple inheritance), so they have display_info()
supra.display_info()
supra.nitro_boost()
supra.activate_luxury_mode()
print("\n")
lexus.luxury_info()

