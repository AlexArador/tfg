import cv2
import numpy as np

# Cargar la imagen original
imagen_original = cv2.imread('circuito.jpg')

# Convertir la imagen a escala de grises
imagen_gris = cv2.cvtColor(imagen_original, cv2.COLOR_BGR2GRAY)

# Aplicar umbral para obtener una imagen binaria (blanco y negro)
_, binaria = cv2.threshold(imagen_gris, 128, 255, cv2.THRESH_BINARY)

# Encontrar contornos
contornos, _ = cv2.findContours(binaria, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Seleccionar el contorno del circuito (suponemos el contorno más grande)
contorno_circuito = max(contornos, key=cv2.contourArea)

# Calcular la longitud del contorno
longitud_contorno = cv2.arcLength(contorno_circuito, closed=True)

# Mostrar la longitud del contorno
print(f"Longitud del contorno: {longitud_contorno}")

# Dibujar el contorno en la imagen original
cv2.drawContours(imagen_original, [contorno_circuito], -1, (0, 255, 0), 2)

# Mostrar y guardar la imagen con el contorno
cv2.imshow('Contorno del Circuito', imagen_original)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.imwrite('imagen_con_contorno.jpg', imagen_original)
