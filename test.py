import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import Normalize
import numpy as np

# Generar datos de ejemplo
x = np.linspace(0, 10, 50)
y = np.sin(x)

# Asignar colores específicos a los puntos
colores = np.where(x < 5, 'red', 'blue')

# Crear un scatter plot con colores específicos para los puntos
scatter = plt.scatter(x, y, c=colores)

# Crear segmentos de línea entre puntos de diferentes colores
segmentos = np.column_stack([x, y]).reshape(len(x), 1, 2)
segmentos = np.concatenate([segmentos[:-1], segmentos[1:]], axis=1)

# Crear una LineCollection con un gradiente de color
norm = plt.Normalize(0, len(x)-1)
gradiente_linea = LineCollection(segmentos, cmap='RdYlGn', norm=norm)
gradiente_linea.set_array(np.arange(len(x)-1))

# Añadir colorbar para mostrar el gradiente
cbar = plt.colorbar(gradiente_linea, ticks=np.arange(len(x)))
cbar.set_label('Segmentos de Línea')

# Configurar el aspecto del plot
plt.title('Scatter Plot con Línea y Gradiente de Color')
plt.xlabel('X')
plt.ylabel('Y')

# Añadir la LineCollection al plot
plt.gca().add_collection(gradiente_linea)

# Mostrar el plot
plt.show()
