import json
import cv2
import numpy as np
import pygame
import math
from PIL import Image
import os

class Goal:
    red = (255, 0, 0)
    green = (0, 255, 0)
    width = 2

    def __init__(self, p1, p2, active = False) -> None:
        self.p1 = p1
        self.p2 = p2
        self._active = active
        self.m = self.get_m()

    def print_goal(self):
        print(f'Línea: {self.get_line()}. Activa: {self._active}')

    def draw_goal(self, game_map):
        pygame.draw.line(game_map, 'green', self.p1, self.p2, self.width)

    def get_color(self):
        return self.red if self._active else self.green

    def get_m(self):
        var_x = self.p2[0] - self.p1[0]
        if var_x == 0:
            return None
        else:
            var_y = self.p2[1] - self.p1[1]
            return -1 * var_y / var_x

    def switch_to(self, to):
        self._active = to
        
    def get_line(self):
        return (self.p1, self.p2)
        
    def is_active(self):
        return self._active

class Circuit:
    goals_file = os.path.join('data', 'circuits', 'goals.json')

    def __init__(self, name, extension) -> None:
        self.name = name
        self.extension = extension

        self.file = f'{self.name}.{self.extension}'
        self.goals = []
        
        self.chord = self._get_chord()
        self.length = 2400
        self._load_goals()

        self.start_position, self.start_angle = self._load_start()

    def _load_goals(self):
        with open(self.goals_file, 'r') as file:
            data = json.load(file)
            
            file.close()

        goals = data[self.name]['goals']
        for i,goal in enumerate(goals):
            self.goals.append(Goal(goal['p1'], goal['p2'], i == 0))

    def _load_start(self):
        with open(self.goals_file, 'r') as file:
            data = json.load(file)
            file.close()

        start = data[self.name]['start']
        start1 = start['start1']
        start2 = start['start2']

        return start1, Circuit.calculate_angle(start1, start2)

    def _get_chord(self):
        imagen = cv2.imread(self.file, cv2.IMREAD_GRAYSCALE)
        # Aplicar el algoritmo de detección de contornos (Canny)
        bordes = cv2.Canny(imagen, 50, 150)
        # Encontrar los contornos cerrados en la imagen
        contornos, _ = cv2.findContours(bordes, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # Identificar el contorno que representa la cuerda (ajusta según tus necesidades)
        cuerda_contorno = max(contornos, key=cv2.contourArea)
        longitud_pixeles = cv2.arcLength(cuerda_contorno, closed=True)

        return int(round(longitud_pixeles, 0))
    
    def get_image_size(self):
        with Image.open(self.file) as img:
            return img.size
    
    def get_startposition(self):
        return self.start_position
    
    def get_prop(self):
        return 1.0 * self.chord / self.length

    @staticmethod
    def calculate_angle(point1, point2):
        x = point2[0] - point1[0]
        y = point1[1] - point2[1]

        h = math.sqrt(math.pow(x, 2) + math.pow(y, 2))
        cos = x / h
        return math.degrees(math.acos(cos))