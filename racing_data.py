import pandas as pd
import os

class DataPoint:
    def __init__(self, x, y, speed, angle, action) -> None:
        self.x = x
        self.y = y
        self.speed = speed
        self.angle = angle        
        self.action = action

    def export(self):
        return [self.x, self.y, self.speed, self.angle, self.action]   

class RacingLine:
    data_folder = os.path.join('data', 'racing_line')

    def __init__(self, generation) -> None:
        self.generation = generation
        self.df = pd.DataFrame([], columns=['car'])
        self.cars = []

        if not os.path.exists(self.data_folder):
            os.mkdir(self.data_folder)
    
    @staticmethod
    def _export_list(data_points: list[DataPoint]):
        return [x.export() for x in data_points]
    
    def get_data(self, car, data_points: list[DataPoint]):
        if car not in self.cars:
            df = pd.DataFrame([[car, RacingLine._export_list(data_points)]], columns=['car', 'racing_line'])
            
            self.df = pd.concat([self.df, df])
            self.cars = set(self.df['car'].tolist())
        
    def dump(self):
        self.df.to_csv(os.path.join(self.data_folder, f'gen{self.generation}.csv'), index=False, header=True)