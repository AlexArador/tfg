import cv2
import numpy as np

# Cargar la imagen en blanco y negro
imagen_path = 'map2_nofinish.png'
imagen = cv2.imread(imagen_path, cv2.IMREAD_GRAYSCALE)

# Aplicar un desenfoque para suavizar la imagen (opcional)
imagen = cv2.GaussianBlur(imagen, (5, 5), 0)

# Aplicar el algoritmo de detección de contornos (Canny)
bordes = cv2.Canny(imagen, 50, 150)

# Encontrar los contornos cerrados en la imagen
contornos, _ = cv2.findContours(bordes, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Identificar el contorno que representa la cuerda (ajusta según tus necesidades)
cuerda_contorno = max(contornos, key=cv2.contourArea)
longitud_pixeles = cv2.arcLength(cuerda_contorno, closed=True)

print(f'Cuerda: {longitud_pixeles}')

# Dibujar la cuerda en la imagen original
cuerda_dibujada = cv2.drawContours(np.zeros_like(imagen), [cuerda_contorno], -1, 255, 2)

# Mostrar la imagen con la cuerda dibujada
cv2.imshow('Cuerda Detectada', cuerda_dibujada)
cv2.waitKey(0)
cv2.destroyAllWindows()
