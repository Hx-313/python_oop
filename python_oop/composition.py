#----------------------------------------
# Lesson: Composition
# Composition is an "OWNS-A" relationship between classes.
# One class is BUILT FROM other classes - the parts cannot exist without the whole.
# A Car OWNS an Engine and Wheels - if the car is destroyed, the engine and wheels die with it.
#
# Key Concepts:
#   1. Dependent Classes   - Engine and Wheels are created INSIDE the Car's __init__
#   2. OWNS-A Relationship - Car creates and owns its parts; they do not live on their own
#   3. Objects Are Created In - car's constructor builds Engine and Wheels automatically
#   4. Lifetime Control    - parts share the car's lifetime (no car = no engine)
#
# ============================================
# COMPOSITION vs AGGREGATION (Why they are different)
# ============================================
# | Aggregation ("HAS-A")   | Composition ("OWNS-A")                |
# |-------------------------|---------------------------------------|
# | Showroom HAS a list of  | Car OWNS its Engine and Wheels       |
# | cars (passed in)        | (created inside the constructor)      |
# | Parts exist on their    | Parts die with the owner - they are  |
# | own even without owner  | not independent objects              |
# | add_car(car) receives   | Engine(horse_power, engine_type) is  |
# | an object that already  | created inside __init__              |
# | exists outside          |                                       |
#
# Simple way to remember:
# - Aggregation: "A showroom HAS a car."   (car can live without the showroom)
# - Composition: "A car OWNS an engine."   (engine cannot exist without the car)
# - In composition the parts are created inside the owner, so they share its life.
#----------------------------------------


class Engine:
    # OWNS-A: Engine is a part of Car, created inside the Car constructor
    def __init__(self, horspower, type):
        self.horspower = horspower  # part's attribute
        self.type = type            # part's attribute

class Wheels:
    # OWNS-A: Wheels are parts of Car, created inside the Car constructor
    def __init__(self, size, type):
        self.size = size   # part's attribute
        self.type = type   # part's attribute


class Car:
    # Car is the OWNER - it creates Engine and Wheels inside its constructor,
    # which means they cannot exist independently of the Car
    def __init__(self, brand, model, year, color, horse_power, engine_type, size, wheel_type):
        self.brand = brand
        self.model = model
        self.year = year
        self.color  = color
        self.engine = Engine(horse_power, engine_type)  # composition: engine built inside the car
        self.wheels = [Wheels(size, wheel_type) for _ in range(4)]  # composition: 4 wheels built inside the car

    def display_info(self):
        # Accessing the parts through the owner (car.engine, car.wheels)
        print(f"Car: {self.brand} {self.model} ({self.year}) - Color: {self.color}")
        print(f"Engine: {self.engine.horspower} HP, Type: {self.engine.type}")
        print(f"Wheels: {len(self.wheels)} wheels of size {self.wheels[0].size} and type {self.wheels[0].type}")

# The engine and wheels only exist because the car exists - that is composition
car = Car("Toyota", "Camry", 2020, "Red", 300, "V6", 18, "Alloy")
car.display_info()
print(car.brand)

#----------------------------------------
# BONUS: Nested Classes
# A class can also be DEFINED INSIDE another class.
# This is the strongest form of composition - the inner class only
# makes sense inside the outer class, so it is declared there.
#
# Key Concepts:
#   1. Inner Class - Engine and Wheels are defined inside Car (nested)
#   2. Access Path - inner classes are reached through the outer class:
#      Car.Engine, Car.Wheels
#   3. Same OWNS-A Lifetime - the inner classes still live and die with the owner
#   4. Instance Still Created In __init__ - nesting only changes WHERE the
#      class is declared, not how it is used
#----------------------------------------

class Car2:
    # Nested classes are defined inside the owner class body
    class Engine:
        def __init__(self, horse_power, type):
            self.horse_power = horse_power
            self.type = type

    class Wheels:
        def __init__(self, size, type):
            self.size = size
            self.type = type

    def __init__(self, brand, model, year, color, horse_power, engine_type, size, wheel_type):
        self.brand = brand
        self.model = model
        self.year = year
        self.color = color
        # same composition pattern - parts are created inside the constructor,
        # but now they are built from the NESTED classes
        self.engine = Car2.Engine(horse_power, engine_type)
        self.wheels = [Car2.Wheels(size, wheel_type) for _ in range(4)]

    def display_info(self):
        print(f"Car: {self.brand} {self.model} ({self.year}) - Color: {self.color}")
        print(f"Engine: {self.engine.horse_power} HP, Type: {self.engine.type}")
        print(f"Wheels: {len(self.wheels)} wheels of size {self.wheels[0].size} and type {self.wheels[0].type}")

# Nested classes are accessed through the outer class: Car2.Engine / Car2.Wheels
car2 = Car2("Honda", "Civic", 2021, "Blue", 158, "Turbo", 17, "Steel")
car2.display_info()
print(f"Nested classes live inside Car2: {Car2.Engine} , {Car2.Wheels}")