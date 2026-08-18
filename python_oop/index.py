from cars import Cars
from inheritence import Haval
car1 = Cars("Haval", "H5", 2020, True, "Mate Black")
car2 = Cars("Toyota", "Camry", 2021, False, "White")
print(car1.get_car_info())


haval = Haval("H6", 2025, True, "Red")
print(haval.driving())
print(haval.get_car_info())