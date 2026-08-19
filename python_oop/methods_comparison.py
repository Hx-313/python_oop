#----------------------------------------
# Lesson: Instance vs Static vs Class Methods
# Python classes can have THREE kinds of methods.
# The difference is what the method receives automatically:
# self (the instance), cls (the class), or nothing at all.
#
# ============================================
# THE THREE METHOD TYPES (Side by Side)
# ============================================
# | Instance Method  | Static Method   | Class Method          |
# |------------------|-----------------|-----------------------|
# | Receives self    | Receives NOTHING| Receives cls         |
# | (the instance)   | (no self, no    | (the class itself)   |
# |                  |  cls)           |                       |
# | Can read/change  | Cannot touch    | Can read/change      |
# | instance AND     | instance or     | CLASS attributes,    |
# | class attributes | class attributes| NOT instance ones    |
# | Called as        | Called as       | Called as            |
# | obj.method()     | Class.method()  | Class.method()       |
# | Typical use:     | Typical use:    | Typical use:         |
# | behavior of one  | helper /        | alternative          |
# | specific object  | utility logic   | constructors         |
# |------------------|-----------------|----------------------|
# | def method(self) | @staticmethod   | @classmethod         |
# |                  | def method()    | def method(cls)      |
#
# Simple way to remember:
# - Instance method: "What can THIS car do?"        -> self
# - Static method:   "Is this color valid?"         -> no object needed
# - Class method:    "Build a car from a string."   -> cls
#----------------------------------------

class Car:
    total_cars = 0  # class attribute

    def __init__(self, brand, model):
        self.brand = brand    # instance attribute
        self.model = model
        Car.total_cars += 1

    # 1. INSTANCE METHOD - receives self, works on one specific car
    def display_info(self):
        print(f"Car: {self.brand} {self.model}")

    # 2. STATIC METHOD - receives nothing, just a helper
    @staticmethod
    def is_valid_brand(brand):
        return brand in ["Toyota", "Honda", "Ford", "BMW"]

    # 3. CLASS METHOD - receives cls, works with the class itself
    @classmethod
    def from_string(cls, data):
        brand, model = data.split()
        return cls(brand, model)  # cls(...) creates a Car

    # 4. CLASS METHOD - reads the class attribute
    @classmethod
    def get_total_cars(cls):
        return f"Total cars: {cls.total_cars}"


# --- Using the three method types ---

# Instance method: needs an object first
car1 = Car("Toyota", "Camry")
car1.display_info()          # self = car1

# Static method: no object needed at all
print(Car.is_valid_brand("Toyota"))   # True
print(Car.is_valid_brand("Tesla"))    # False

# Class method: builds an object (alternative constructor)
car2 = Car.from_string("Honda Civic") # cls = Car, so cls(...) is Car(...)
car2.display_info()

# Class method: reads class-level data
print(Car.get_total_cars())

# --- Same idea, different scope ---
# instance method CAN see class attributes too:
def show_total(self):
    return self.total_cars  # self can reach class attributes

Car.show_total = show_total  # added at runtime just for the demo
print(car1.show_total())

# but a static method CANNOT reach them:
@staticmethod
def cannot_see():
    # no self / no cls -> no access to attributes at all
    return "I have no access to Car data"

print(cannot_see())