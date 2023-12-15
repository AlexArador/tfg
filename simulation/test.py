import cv2
import numpy as np

# Definir la posición inicial y final de la línea de interés
punto_inicio = (831, 849)
punto_fin = (831, 1020)

# Definir el punto que quieres verificar
punto_a_verificar = (250, 180)

# Calcular la ecuación de la línea (y = mx + b)
m = (punto_fin[1] - punto_inicio[1]) / (punto_fin[0] - punto_inicio[0])
b = punto_inicio[1] - m * punto_inicio[0]

# Calcular la posición del punto en relación con la línea
posicion_punto = punto_a_verificar[1] - (m * punto_a_verificar[0] + b)

# Verificar si el punto ha cruzado la línea (positivo significa que está arriba, negativo abajo)
if posicion_punto > 0:
    print('El punto ha cruzado la línea.')
else:
    print('El punto no ha cruzado la línea.')
