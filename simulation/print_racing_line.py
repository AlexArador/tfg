import pandas as pd
import matplotlib.pyplot as plt
import cv2

df = pd.read_csv('gen4.csv')
df['racing_line'] = df['racing_line'].apply(lambda x: eval(x))

df['len'] = df.apply(lambda x: len(x['racing_line']), axis=1)
df = df.sort_values(by=['len'], ascending=False)
print(df.iloc[0])

longest_car_path = df.iloc[0]['car']
#longest_car_path = 26

# map2.png 1920 10180

racing_line = df['racing_line'][df['car'] == longest_car_path].iloc[0]
coordenadas_x = [x[0] for x in racing_line]
coordenadas_y = [x[1] for x in racing_line]

imagen_circuito = cv2.imread('map2.png')

# Crear un gráfico de dispersión sobre la imagen
plt.imshow(cv2.cvtColor(imagen_circuito, cv2.COLOR_BGR2RGB))  # Convertir BGR a RGB para Matplotlib
plt.scatter(coordenadas_x, coordenadas_y, color='red', s=5)  # Puedes ajustar el tamaño (s) según tu preferencia

# Mostrar la imagen con las coordenadas
plt.show()

