from cars import Cars

class Haval(Cars):
    def __init__(self, model, year, for_sale, color):
        super().__init__("Haval", model, year, for_sale, color)