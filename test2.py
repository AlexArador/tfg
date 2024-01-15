import pandas as pd
import os

drivers_list = list(set(pd.read_csv(os.path.join('data', 'circuits', 'times.csv'))['driverId'].tolist()))

print(drivers_list)