from abc import ABC,  abstractmethod

class Vehicle(ABC):
    @abstractmethod
    def get_vehicle_info(self):
        pass
    @abstractmethod
    def drive(self):
        pass
    @abstractmethod
    def clean_driving(self):
        pass