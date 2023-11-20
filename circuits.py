import os
import pandas as pd

data_path = 'data'
image_path = 'images'

circuit_images = os.listdir(image_path)
available_circuits = [c[:c.find('.')] for c in circuit_images]

df_circuits = pd.read_csv(os.path.join(data_path, 'raw', 'circuits.csv'))
df_circuits = df_circuits[df_circuits['circuitRef'].isin(available_circuits)]

print(f'Available circuits: {len(df_circuits)}')
print(f'Available images: {len(circuit_images)}')

df_circuits = df_circuits[['circuitId', 'circuitRef', 'name', 'country', 'lat', 'lng']]
df_circuits.to_csv(os.path.join(data_path, 'circuits.csv'), index=False, header=True)

print(df_circuits.head())