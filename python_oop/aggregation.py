#----------------------------------------
# Lesson: Aggregation
# Aggregation is a "HAS-A" relationship between classes.
# Each class is INDEPENDENT of the others, but they are still RELATED to each other.
# A Showroom HAS cars and bikes - but a car can exist even if the showroom disappears.
#
# Key Concepts:
#   1. Independent Classes - Cars and Bikes are self-contained; they don't need Showroom to exist
#   2. HAS-A Relationship  - Showroom holds a list of cars and a list of bikes
#   3. Objects Are Passed In - showroom.add_car(car) receives objects that already exist
#   4. Management System   - this is a tiny shop system practicing core OOP:
#      classes, __init__, methods, __str__, lists of objects, and user input
#
# ============================================
# AGGREGATION vs INHERITANCE (Why they are different)
# ============================================
# | Inheritance ("IS-A")    | Aggregation ("HAS-A")             |
# |-------------------------|-----------------------------------|
# | Cars IS a Vehicle       | Showroom HAS a list of Cars       |
# | Child shares parent's   | Owner keeps a reference, but the  |
# | attributes & methods    | owned object lives on its own    |
# | Single parent, built-in | Any number of objects, passed in |
#
# Simple way to remember:
# - Inheritance: "A car IS a vehicle."         (what something IS)
# - Aggregation: "A showroom HAS a car."       (what something HOLDS)
# - The car does not die when the showroom closes - the classes are independent.
#----------------------------------------

class Showroom:
    def __init__(self, name):
        self.name = name
        self.cars = []   # HAS-A: Showroom holds many Cars
        self.bikes = []  # HAS-A: Showroom holds many Bikes

    def add_bike(self, bike):
        self.bikes.append(bike)
        print(f"{bike.company} {bike.model} is Added to Showroom")

    def add_car(self, car):
        self.cars.append(car)
        print(f"{car.company} {car.model} is Added to Showroom")

    def show_cars(self):
        return [
            f"{car.company} {car.model} ({car.year}), {car.color}, "
            f"{'Booked' if car.booked else 'Available'}"
            for car in self.cars
        ]

    def show_bikes(self):
        return [
            f"{bike.company} {bike.model} ({bike.year}) {bike.cc}cc in {bike.color} "
            f"{'Booked' if bike.booked else 'Available'}"
            for bike in self.bikes
        ]

    def check_Availability(self, model):
        for car in self.cars:
            if model.lower() in car.model.lower():
                return f"This model is in the Showroom {'but already booked' if car.booked else 'and Available to buy'}"

        for bike in self.bikes:
            if model.lower() in bike.model.lower():
                return f"This model is in the Showroom {'but already booked' if bike.booked else 'and Available to buy'}"

        return "This model is not available"

class Cars:
    def __init__(self, company, model, year, color, booked):
        self.company = company
        self.model = model
        self.year = year
        self.color = color
        self.booked = booked

    def __str__(self):
        status = "booked" if self.booked else "available"
        return f"{self.company} {self.model} ({self.year}, {self.color}, {status})"

class Bikes:
    def __init__(self, company, model, year, color, cc, booked):
        self.company = company
        self.model = model
        self.year = year
        self.color = color
        self.booked = booked
        self.cc = cc

showroom = Showroom("Civic Center")

car1 = Cars("Toyota", "Camry", "2020", "Grey", False)
car2 = Cars("Haval", "H6", "2024", "Grey", False)
car3 = Cars("Porsche", "Cayman", "2020", "Python Green", True)

bike1 = Bikes("Suzuki", "GSX-150", "2025", "Red", 150, False)
bike2 = Bikes("Honda", "CBR 250", "2023", "Black", 250, True)
bike3 = Bikes("Yamaha", "MT-07", "2024", "Blue", 689, False)

print(f"Welcome to {showroom.name}")
print(showroom.show_bikes())
print(showroom.show_cars())

showroom.add_bike(bike1)
showroom.add_bike(bike2)
showroom.add_bike(bike3)
showroom.add_car(car1)
showroom.add_car(car2)
showroom.add_car(car3)

print(showroom.show_bikes())
print(showroom.show_cars())

model = input("Enter the model of the bike or car you want to check: ")

print(showroom.check_Availability(model))