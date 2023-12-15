import pandas as pd

class RacingLine:
    def __init__(self, generation) -> None:
        self.generation = generation
        self.df = pd.DataFrame([], columns=['generation', 'car'])
        self.cars = []
    
    def get_data(self, car, racing_line):
        if len(self.df[self.df['car'] == car]) == 0:
            df = pd.DataFrame(racing_line, columns=['x', 'y'])
            df['car'] = [car] * len(df)
            
            self.df = pd.concat([self.df, df])
            
            self.cars = set
        
    def dump(self):
        self.df.to_csv(f'racing_line_gen{self.generation}.csv', index=False, header=True)