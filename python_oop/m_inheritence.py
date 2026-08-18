from cars import Cars
class SportsVehicle(Cars):
    def __init__(self, name, model, year, for_sale, color, top_speed):
        super().__init__(name, model, year, for_sale, color)
        self.top_speed = top_speed

    def sports_info(self):
        Cars.get_car_info(self)
        print(f"{self.brand} {self.model} ({self.year}) - Color: {self.color}, For Sale: {self.for_sale}")
        print(f"Top Speed: {self.top_speed} km/h")

class LuxuryVehicle(Cars):
    def __init__(self, name, model, year, for_sale, color, luxury_features):
        super().__init__(name, model, year, for_sale, color)
        self.luxury_features = luxury_features

    def luxury_info(self):
        Cars.get_car_info(self)
        print(f"{self.brand} {self.model} ({self.year}) - Color: {self.color}, For Sale: {self.for_sale}")
        print(f"Luxury Features: {', '.join(self.luxury_features)}")

class Haval(LuxuryVehicle):
    pass

class Ferrari(SportsVehicle):
    pass

class Toyota(SportsVehicle, LuxuryVehicle):
    def __init__(self, name, model, year, for_sale, color, top_speed, luxury_features):
        Cars.__init__(self, name, model, year, for_sale, color)
        self.top_speed = top_speed
        self.luxury_features = luxury_features
    
    def display_info(self):
        print(f"{self.brand} {self.model} ({self.year}) - Color: {self.color}, For Sale: {self.for_sale}")
        print(f"Top Speed: {self.top_speed} km/h")
        print(f"Luxury Features: {', '.join(self.luxury_features)}")


h6 = Haval("Haval", "H6", 2022, False, "white", ["Leather Seats", "Sunroof", "Advanced Infotainment"])
ferrari = Ferrari("Ferrari", "488 GTB", 2021, True, "red", 330)
supra = Toyota("Toyota", "Supra", 2023, False, "blue", 250, ["Adaptive Cruise Control", "Premium Audio System"])
lexus = Toyota("Lexus", "LC 500", 2022, True, "black", 270, ["Heated Seats", "Heads-Up Display"])


h6.luxury_info()
h6.driving()
print("\n")
ferrari.sports_info()
print("\n")
supra.display_info()
print("\n")
lexus.display_info()

