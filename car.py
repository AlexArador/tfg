import math

class Car:
    
    mass = 700
    power = 350000
    width = 2
    length = 5.5
    
    acceleration = 0
    
    def __init__(self) -> None:        
        pass
    
    def _acceleration(self):
        self.acceleration = self.power / self.mass
        return self.acceleration
        
        
car = Car()

print(f'Acceleration: {car._acceleration()}')