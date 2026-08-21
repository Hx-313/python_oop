#----------------------------------------
# Lesson: Magic Methods (Dunder Methods)
# Magic methods are special methods with DOUBLE UNDERSCORES
# at the start and end: __init__, __str__, __len__, etc.
# Python calls them AUTOMATICALLY behind the scenes -
# you never call them directly.
#
# Key Concepts:
#   1. Double Underscores - __name__ (dunder) marks a magic method
#   2. Called Automatically - Python invokes them for you:
#      print(car)  ->  calls car.__str__()
#      len(cars)   ->  calls cars.__len__()
#      car + other ->  calls car.__add__(other)
#   3. Operators Are Magic Methods - +, -, ==, <, in, len(), print()
#      all map to magic methods under the hood
#   4. You Define Them - you decide what each operator/function does
#      for YOUR class
#
# ============================================
# COMMON MAGIC METHODS (Cheat Sheet)
# ============================================
# | Magic Method     | Triggered By             | Purpose                  |
# |------------------|--------------------------|--------------------------|
# | __init__(self,..)| Car("Toyota", 2020)      | constructor - build obj  |
# | __str__(self)    | print(car), str(car)     | human-readable string    |
# | __repr__(self)   | repr(car)                | developer-friendly copy  |
# | __len__(self)    | len(cars)                | length of the object     |
# | __add__(self, o) | car1 + car2              | define + operator        |
# | __eq__(self, o)  | car1 == car2             | define == comparison     |
# | __lt__(self, o)  | car1 < car2              | define < comparison      |
# | __getitem__(self,| cars[0]                  | index access []          |
# |                  |                          |                          |
# | __contains__(self| "Toyota" in cars         | define in operator       |
# |                  |                          |                          |
# | __iter__(self)   | for c in cars            | make object iterable     |
#
# Simple way to remember:
# - Magic methods are Python's hooks into your class.
# - When you write len(x), Python secretly runs x.__len__().
# - Defining them makes your objects behave like built-in types.
#----------------------------------------

class Car:
    def __init__(self, brand, model, year, price):
        # __init__: called automatically when you create Car(...)
        self.brand = brand
        self.model = model
        self.year = year
        self.price = price

    def __str__(self):
        # __str__: called automatically by print() and str()
        return f"{self.brand} {self.model} ({self.year})"

    def __repr__(self):
        # __repr__: developer-friendly representation (also used in lists)
        return f"Car('{self.brand}', '{self.model}', {self.year}, {self.price})"

    def __add__(self, other):
        # __add__: defines what car1 + car2 means
        # here: combining two cars gives the total price
        return f"Combined price: ${self.price + other.price}"

    def __eq__(self, other):
        # __eq__: defines what car1 == car2 means
        return self.brand == other.brand and self.model == other.model

    def __lt__(self, other):
        # __lt__: defines what car1 < car2 means (useful for sorting)
        return self.price < other.price

    def __len__(self):
        # __len__: defines what len(car) returns
        return self.year  # just for demo - len() returns the year

    def __getitem__(self, key):
        # __getitem__: defines what car[key] returns
        return {"brand": self.brand, "model": self.model, "year": self.year}.get(key)

    def __contains__(self, item):
        # __contains__: defines what "Toyota" in car means
        return item in (self.brand, self.model)


car1 = Car("Toyota", "Camry", 2020, 30000)
car2 = Car("Honda", "Civic", 2021, 25000)
car3 = Car("Toyota", "Camry", 2019, 20000)

# __str__ is called automatically by print()
print(car1)                     # Toyota Camry (2020)

# __repr__ - used in lists and debugging
print([car1, car2])

# __add__ - the + operator now works on cars
print(car1 + car2)              # Combined price: $55000

# __eq__ - comparing cars
print(car1 == car2)             # False (different brands)
print(car1 == car3)             # True (same brand and model)

# __lt__ - comparing cars (sorts by price)
cars = [car1, car2, car3]
cars.sort()                     # uses __lt__ to sort
print([str(c) for c in cars])

# __getitem__ - indexing
print(car1["brand"])            # Toyota

# __contains__ - the in operator
print("Toyota" in car1)         # True
print("Ford" in car1)           # False