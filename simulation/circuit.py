import json
import cv2
import numpy as np

class Goal:
    red = (255, 0, 0)
    green = (0, 255, 0)
    width = 2

    def __init__(self, p1, p2, active = False) -> None:
        self.p1 = p1
        self.p2 = p2
        self.active = active
        self.m = self.get_m()

        self.upper_limit_x = self.p1[0] if self.p1[0] > self.p2[0] else self.p2[0]
        self.lower_limit_x = self.p2[0] if self.p1[0] > self.p2[0] else self.p1[0]
        self.upper_limit_y = self.p1[1] if self.p1[1] > self.p2[1] else self.p2[1]
        self.lower_limit_y = self.p2[1] if self.p1[1] > self.p2[1] else self.p1[1]

        self.is_flat = self.upper_limit_y == self.lower_limit_y
        self.is_vertical = self.m is None

    def print_goal(self):
        print(f'Pendiente: {self.m}. Plana: {self.is_flat}. Vertical: {self.is_vertical}')
        print(f'Lower X: {self.lower_limit_x}. Upper X: {self.upper_limit_x}')
        print(f'Lower Y: {self.lower_limit_y}. Upper Y: {self.upper_limit_y}')

    def get_color(self):
        return self.red if self.active else self.green
    
    def get_m(self):
        var_x = self.p2[0] - self.p1[0]
        if var_x == 0:
            return None
        else:
            var_y = self.p2[1] - self.p1[1]
            return -1 * var_y / var_x
        
    def is_active(self):
        return self.is_active
        
    def has_crossed(self, p):
        margin = 25 # pixels
        px = p[0]
        py = p[1]
        
        if self.is_vertical:
            if py >= self.lower_limit_y and py <= self.upper_limit_y:
                return px >= self.p1[0] - margin and px <= self.p1[0] + margin
            else:
                return False
        elif self.is_flat:
            if px >= self.lower_limit_x and px <= self.upper_limit_x:
                return py >= self.p1[1] - margin and py <= self.p1[1] + margin
            else:
                return False
        else:
            if px >= self.lower_limit_x and px >= self.upper_limit_x and py >= self.lower_limit_y and py <= self.upper_limit_y:
                return py >= self.m * px - margin and py <= self.m * px + margin
            
    def switch_to(self, to):
        self.is_active = to

class Circuit:
    goals_file = 'goals.json'

    def __init__(self, name, extension) -> None:
        self.name = name
        self.extension = extension

        self.file = f'{self.name}.{self.extension}'
        self.goals = []
        self._load_goals()

    def _load_goals(self):
        with open(self.goals_file, 'r') as file:
            data = json.load(file)

        goals = data[self.name]['goals']
        for i,goal in enumerate(goals):
            self.goals.append(Goal(goal['p1'], goal['p2'], i == 0))

    def get_chord(self):
        imagen = cv2.imread(self.file, cv2.IMREAD_GRAYSCALE)
        # Aplicar el algoritmo de detección de contornos (Canny)
        bordes = cv2.Canny(imagen, 50, 150)
        # Encontrar los contornos cerrados en la imagen
        contornos, _ = cv2.findContours(bordes, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # Identificar el contorno que representa la cuerda (ajusta según tus necesidades)
        cuerda_contorno = max(contornos, key=cv2.contourArea)
        longitud_pixeles = cv2.arcLength(cuerda_contorno, closed=True)

        return longitud_pixeles
    
c = Circuit('map2', 'png')