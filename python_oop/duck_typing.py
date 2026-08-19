
#----------------------------------------
# Lesson: Duck Typing
# Duck typing is ANOTHER way to achieve polymorphism in Python.
# The name comes from the saying: "If it walks like a duck and quacks like a duck, then it's a duck."
# In Python, we don't check WHAT TYPE an object is - we check WHAT IT CAN DO.
#
# Key Concepts:
#   1. Focus on Behavior, Not Type - we only care that an object HAS the method we call
#   2. No Inheritance Required    - Boats does NOT inherit from Vehicle, yet it still works!
#   3. Python Trusts the Object    - Python never forces you to prove the type; it just calls the method
#   4. Same Loop, Different Classes - one for-loop works on Cars, Bikes, AND Boats
#
# ============================================
# DUCK TYPING vs POLYMORPHISM (Why they look the same, but work differently)
# ============================================
# Both let us call the same method on different objects - but the RULES are different:
#
# | Polymorphism (Inheritance)  | Duck Typing (Behavior)         |
# |-----------------------------|--------------------------------|
# | Requires a shared parent    | No parent needed at all        |
# | Child MUST inherit Vehicle  | Any class with drive() works   |
# | "You MUST be a Vehicle"     | "You MUST be able to drive()"  |
# | Checks the CLASS            | Checks the METHOD              |
#
# Simple way to remember:
# - Polymorphism asks: "Is it a Vehicle?"  (type-based)
# - Duck typing asks:   "Can it drive()?"   (behavior-based)
# - Polymorphism = the MENU (declared, inherited rules)
# - Duck typing   = "I don't care what you ARE, just drive()!"
#----------------------------------------

# Vehicle is NOT abstract here - it's just a plain base class.
# Cars and Bikes DO inherit from it, but that is NOT what makes duck typing work.
class Vehicle:

    can_drive = True

class Cars(Vehicle):
    def drive(self):
        print("car can be driven on four wheels " if self.can_drive else "car cannot be driven")

class Bikes(Vehicle):
    def drive(self):
        print("bike can be driven on two wheels " if self.can_drive else "bike cannot be driven")

# Boats does NOT inherit from Vehicle at all!
# Duck typing does not care - as long as Boats HAS a drive() method, it qualifies.
class Boats:
    can_drive = False
    def drive(self):
        print("boat can be driven on water " if self.can_drive else "boat cannot be driven")

# A list mixing 3 DIFFERENT classes: two subclasses of Vehicle + one unrelated class (Boats).
vehicles = [Cars(), Bikes(), Boats()]

# One loop, SAME method call - but Python never checks the type.
# It just trusts that every object can drive() (duck typing in action).
# If Boats had NO drive() method, Python would crash with AttributeError.
for vehicle in vehicles:
    vehicle.drive()  # This will call the drive method of each object, regardless of its class