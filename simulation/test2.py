import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import Normalize
import numpy as np

import os
import pandas as pd

data_folder = 'racing_line'
generation = 69

csv = os.path.join(data_folder, f'gen{generation}.csv')

df = pd.read_csv(csv)
df['racing_line'] = df['racing_line'].apply(lambda x: eval(x))

df['len'] = df.apply(lambda x: len(x['racing_line']), axis=1)
df = df.sort_values(by=['len'], ascending=False)
print(df.iloc[0])

longest_car_path = df.iloc[0]['car']

print(f'Selected car: {longest_car_path}')

print(df.iloc[0]['racing_line'][0][4])

racing_line = df['racing_line'][df['car'] == longest_car_path].tolist()
racing_line = racing_line[0]

print(set([x[4] for x in racing_line]))