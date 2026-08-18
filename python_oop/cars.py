class Cars:

    working_year = 2026
    cars_created  = 0
    def __init__(self, brand, model, year, for_sale, color):
        self.brand = brand
        self.model =model
        self.year = year
        self.for_sale = for_sale
        self.color = color
        Cars.cars_created += 1

    def get_car_info(self):
        return f"{self.brand} {self.model} ({self.year}) - Color: {self.color}, For Sale: {self.for_sale}, Working year: {Cars.working_year}, Cars Created so far: {Cars.cars_created}"