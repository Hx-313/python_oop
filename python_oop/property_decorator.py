#----------------------------------------
# Lesson: Property Decorator (@property)
# The @property decorator turns a METHOD into an ATTRIBUTE.
# You define a method, but you read/write it like a plain attribute:
# car.speed instead of car.speed().
#
# Key Concepts:
#   1. @property  - makes a getter: car.speed reads the value
#   2. @setter    - makes a setter: car.speed = 100 validates + stores
#   3. @deleter   - makes a deleter: del car.speed
#   4. Encapsulation - you control HOW the attribute is read and written,
#      so invalid values can be rejected or converted
#   5. Attribute Name - the property name (speed) is used by all three,
#      while the real data hides in a private attribute (_speed)
#
# ============================================
# REGULAR ATTRIBUTE vs PROPERTY (Why they are different)
# ============================================
# | Plain Attribute        | Property (@property)                |
# |-------------------------|-------------------------------------|
# | self.speed = 100        | self._speed = 100 (private)        |
# | Read: car.speed         | Read: car.speed  (calls the getter)|
# | Write: car.speed = 100  | Write: car.speed = 100 (calls the  |
# |                         | setter - validation possible)      |
# | No control - any value  | Control - setter can reject bad    |
# | is stored as-is         | values (negative, too fast, etc.)  |
# | Caller sees it directly | Caller still uses the SAME syntax, |
# |                         | but the class controls the logic   |
#
# Simple way to remember:
# - Property: "car.speed" looks like an attribute but RUNS code.
# - Getter controls reading, setter controls writing.
# - You can change the internal logic without changing the caller's code.
#----------------------------------------

class Car:
    def __init__(self, brand, model, max_speed):
        self.brand = brand
        self.model = model
        self.max_speed = max_speed
        self._speed = 0  # private attribute - real storage of the property

    @property
    def speed(self):
        # GETTER: runs when you read car.speed
        print("-> getter called")
        return self._speed

    @speed.setter
    def speed(self, value):
        # SETTER: runs when you write car.speed = value
        print(f"-> setter called with {value}")
        if value < 0:
            raise ValueError("Speed cannot be negative")
        if value > self.max_speed:
            raise ValueError(f"Speed cannot exceed {self.max_speed} km/h")
        self._speed = value

    @speed.deleter
    def speed(self):
        # DELETER: runs when you write del car.speed
        print("-> deleter called")
        del self._speed

    def __str__(self):
        return f"{self.brand} {self.model}"


car = Car("Toyota", "Camry", 240)

# GETTER - reading looks like a normal attribute (no parentheses)
print(car.speed)          # -> getter called, 0

# SETTER - writing also looks like a normal attribute,
# but the setter VALIDATES the value before storing it
car.speed = 120
print(car.speed)          # -> getter called, 120

# invalid values are rejected by the setter
try:
    car.speed = -50       # raises ValueError (negative)
except ValueError as e:
    print(f"Rejected: {e}")

try:
    car.speed = 300       # raises ValueError (over max speed)
except ValueError as e:
    print(f"Rejected: {e}")

# DELETER - removing the property
del car.speed             # -> deleter called

# The caller's code never changes - car.speed just works,
# while the class controls everything behind the scenes