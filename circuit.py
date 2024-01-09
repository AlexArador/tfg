import json
import cv2
import pygame
import math
from PIL import Image
import os
import pandas as pd
from datetime import datetime

class Goal:
    red = (255, 0, 0)
    green = (0, 255, 0)
    black = (0, 0, 0, 255)
    width = 5

    def __init__(self, p1, p2, active = False) -> None:
        self.p1 = p1
        self.p2 = p2
        self._active = active
        self.m = self.get_m()

    def print_goal(self):
        print(f'Línea: {self.get_line()}. Activa: {self._active}')

    def draw_goal(self, game_map):
        fp, lp = self.get_points_in_line(game_map)
        self.p1 = fp
        self.p2 = lp
        pygame.draw.line(game_map, self.get_color(), self.p1, self.p2, self.width)
        
    def get_points_in_line(self, game_map):
        x1 = self.p1[0]
        y1 = self.p1[1]
        
        x2 = self.p2[0]
        y2 = self.p2[1]
        
        puntos = []
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        error = dx - dy

        while x1 != x2 or y1 != y2:
            if game_map.get_at((x1, y1)) == self.black:
                puntos.append((x1, y1))
            e2 = 2 * error
            if e2 > -dy:
                error -= dy
                x1 += sx
            if e2 < dx:
                error += dx
                y1 += sy

        if game_map.get_at((x2, y2)) == self.black:
            puntos.append((x2, y2))
        return puntos[0], puntos[-1]


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

    def __init__(self, name, extension) -> None:
        self.data_folder = os.path.join('data', 'circuits')
        self.goals_file = os.path.join(self.data_folder, 'circuits.json')
        self.circuits_file = os.path.join(self.data_folder, 'circuits.csv')

        self.name = name
        self.extension = extension

        self.file = os.path.join(self.data_folder, 'images', f'{self.name}.{self.extension}')
        self.goals = []

        self.circuit_id = self._get_circuit_id()
        self.chord = self._get_chord()
        self.length = self._get_length()
        self._load_goals()

        self.start_position, self.start_angle = self._load_start()

    def set_active_goal(self, to):
        for i,g in enumerate(self.goals):
            g.switch_to(i == to)
    
    def _get_circuit_id(self):
        df = pd.read_csv(self.circuits_file)
        return df['circuitId'][df['circuitRef'] == self.name].iloc[0]

    def get_best_time(self, best: bool = True): # False
        df = pd.read_csv(os.path.join(self.data_folder, 'times.csv'))
        
        df = df[df['circuitId'] == self.circuit_id].sort_values(by='time', ascending=best)
        t = datetime.strptime(df['time'].iloc[0], '%H:%M:%S.%f').time()
        return (t.minute * 60 + t.second) * 1000 + t.microsecond // 1000 

    def _get_length(self):
        df = pd.read_csv(self.circuits_file)
        return df['length'][df['circuitRef'] == self.name].iloc[0]

    def _load_goals(self):
        with open(self.goals_file, 'r', encoding='utf-8') as file:
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
        bordes = cv2.Canny(imagen, 50, 150)
        contornos, _ = cv2.findContours(bordes, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
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

    @staticmethod
    def get_circuits():
        data_path = 'data'

        circuit_images = os.listdir(os.path.join(data_path, 'circuits', 'real'))
        available_circuits = [c[:c.find('.')] for c in circuit_images]

        df_circuits = pd.read_csv(os.path.join(data_path, 'raw', 'circuits.csv'))
        df_circuits = df_circuits[df_circuits['circuitRef'].isin(available_circuits)]

        print(f'Available circuits: {len(df_circuits)}')
        print(f'Available images: {len(circuit_images)}')

        df_circuits = df_circuits[['circuitId', 'circuitRef', 'name', 'country', 'lat', 'lng']]
        circuits_file = os.path.join(data_path, 'circuits', 'circuits.csv')
        df_circuits.to_csv(circuits_file, index=False, header=True)

    @staticmethod
    def convert_time(t, time_format = '%M:%S.%f'):
        try:
            return datetime.strptime(t, time_format).time()
        except:
            return None

    @staticmethod
    def get_laptimes():
        data_path = 'data'

        df_quali = pd.read_csv(os.path.join(data_path, 'raw', 'qualifying.csv'))
        df_quali['q1'] = df_quali['q1'].apply(lambda x: Circuit.convert_time(x))
        df_quali['q2'] = df_quali['q3'].apply(lambda x: Circuit.convert_time(x))
        df_quali['q3'] = df_quali['q3'].apply(lambda x: Circuit.convert_time(x))

        df_races = pd.read_csv(os.path.join(data_path, 'raw', 'races.csv'))

        df_races = df_races[['raceId', 'circuitId']]
        df = pd.merge(df_quali, df_races, how='inner', on='raceId')

        q1 = df[['circuitId', 'q1']].rename(columns={'q1': 'time'})
        q2 = df[['circuitId', 'q2']].rename(columns={'q2': 'time'})
        q3 = df[['circuitId', 'q3']].rename(columns={'q3': 'time'})

        qt = pd.concat([q1, q2, q3], ignore_index=True)
        qt = qt[~qt['time'].isna()]

        df.to_csv(os.path.join(data_path, 'circuits', 'qualifying.csv'), header=True, index=False)
        qt.to_csv(os.path.join(data_path, 'circuits', 'times.csv'), header=True, index=False)
