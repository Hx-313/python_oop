# this cars is to create a cars class from vehicles abstract class
from abstract_classes import Vehicle
class Cars(Vehicle):
        def __init__(self, brand, model, year, for_sale, color):
            self.brand = brand
            self.model = model
            self.year = year
            self.for_sale = for_sale
            self.color = color

        def get_vehicle_info(self):
            return f"{self.brand} {self.model} ({self.year}) - Color: {self.color}, For Sale: {self.for_sale}"
        def drive(self):
            return f"{self.brand} {self.model} is getting driven around {self.year}"
        def clean_driving(self):
            print(f"{self.brand} {self.model} is getting driven around {self.year}")


class Bikes(Vehicle):
        def __init__(self, brand, model, year, for_sale, color):
            self.brand = brand
            self.model = model
            self.year = year
            self.for_sale = for_sale
            self.color = color

        def get_vehicle_info(self):
            return f"{self.brand} {self.model} ({self.year}) - Color: {self.color}, For Sale: {self.for_sale} and has two wheels"
        def drive(self):
            return f"{self.brand} {self.model} is getting driven around {self.year} on a bike path with two wheels and a helmet"
        def clean_driving(self):
            print(f"{self.brand} {self.model} is getting driven around {self.year} on a bike path")


car = Cars("Toyota", "Camry", 2020, True, "blue")
bike = Bikes("Giant", "Defy", 2020, False, "red")

car.clean_driving()
bike.clean_driving()