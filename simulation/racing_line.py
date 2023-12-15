import pandas as pd

class RacingLine:
    def __init__(self, generation) -> None:
        self.generation = generation
        self.df = pd.DataFrame([], columns=['car'])
        self.cars = []
    
    def get_data(self, car, racing_line):
        if car not in self.cars:
            df = pd.DataFrame([[car, racing_line]], columns=['car', 'racing_line'])            
            
            self.df = pd.concat([self.df, df])            
            self.cars = set(self.df['car'].tolist())
        
    def dump(self):
        self.df.to_csv(f'gen{self.generation}.csv', index=False, header=True)