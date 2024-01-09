import pandas as pd
import os

class DataPoint:
    def __init__(self, x, y, speed, angle, action) -> None:
        self.x = x
        self.y = y
        self.speed = speed
        self.angle = angle
        #self.distance = distance
        self.action = action

    def export(self):
        #return [self.x, self.y, self.speed, self.angle, self.distance, self.action]
        return [self.x, self.y, self.speed, self.angle, self.action]

class RacingLine:

    def __init__(self, data_folder, generation) -> None:
        self.generation = generation
        self.data_folder = data_folder
        self.df = pd.DataFrame([], columns=['car'])
        self.cars = []

        if not os.path.exists(self.data_folder):
            os.mkdir(self.data_folder)

    @staticmethod
    def _export_list(data_points: list[DataPoint]):
        return [x.export() for x in data_points]
    
    @staticmethod
    def convert_time(s):
        minutes = int(s // 60)
        seconds = s % 60
        fractions = int((seconds - int(seconds)) * 1000)
        seconds = int(seconds)
        
        return "{:02}:{:02}.{:03}".format(minutes, seconds, fractions)

    def get_data(self, car, data_points: list[DataPoint], circuit, time, goals_crossed):
        df_columns = ['car', 'time', 'circuit', 'goals_crossed', 'racing_line']
        if car not in self.cars:
            df = pd.DataFrame([[car, time, circuit, goals_crossed, RacingLine._export_list(data_points)]], columns=df_columns)

            self.df = pd.concat([self.df, df])
            self.cars = set(self.df['car'].tolist())

    def dump(self):
        self.df.to_csv(os.path.join(self.data_folder, f'gen{self.generation}.csv'), index=False, header=True)
