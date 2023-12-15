import cv2
import numpy as np

# Cargar la imagen
imagen = cv2.imread('circuito.jpg')

# Convertir a escala de grises
imagen_gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

# Aplicar filtro Gaussiano para reducir el ruido
imagen_suavizada = cv2.GaussianBlur(imagen_gris, (5, 5), 0)

# Detectar bordes con el detector de Canny
bordes = cv2.Canny(imagen_suavizada, 50, 150)

# Encontrar contornos con jerarquía completa (incluyendo contornos internos y externos)
contornos, jerarquia = cv2.findContours(bordes, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Dibujar contornos en la imagen original (contornos exteriores en verde y contornos interiores en rojo)
imagen_contornos = imagen.copy()
for i, contorno in enumerate(contornos):
    if jerarquia[0, i, 3] == -1:
        # Contorno exterior (sin padre)
        cv2.drawContours(imagen_contornos, [contorno], -1, (0, 255, 0), 2)
    else:
        # Contorno interior (con padre)
        cv2.drawContours(imagen_contornos, [contorno], -1, (0, 0, 255), 2)

imagen = cv2.imread('circuito.jpg', cv2.IMREAD_GRAYSCALE)
# Aplicar umbral para obtener una imagen binaria (blanco y negro)
_, binaria = cv2.threshold(imagen, 128, 255, cv2.THRESH_BINARY)
# Aplicar una transformación morfológica para eliminar pequeños detalles
kernel = np.ones((5, 5), np.uint8)
binaria = cv2.morphologyEx(binaria, cv2.MORPH_OPEN, kernel)
# Encontrar contornos
contornos, _ = cv2.findContours(binaria, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# Seleccionar el contorno del circuito (suponemos el contorno más grande)
contorno_circuito = max(contornos, key=cv2.contourArea)
# Crear una imagen en blanco para dibujar la línea del centro
linea_centro_imagen = np.zeros_like(imagen)
# Dibujar la línea del centro
cv2.drawContours(imagen_contornos, [contorno_circuito], -1, (255, 0, 255), 2)

cuerda = cv2.arcLength(contorno_circuito, closed=True)

print(f'Longitud: {cuerda}')

# Mostrar y guardar la imagen resultante
cv2.imshow('Imagen con Contornos', imagen_contornos)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.imwrite('circuito_con_contornos.jpg', imagen_contornos)
