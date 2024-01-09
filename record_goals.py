import pygame
import sys
import os
from PIL import Image

# Inicializar Pygame
pygame.init()

def get_image_size(self):
        with Image.open(self.file) as img:
            return img.size
        
circuit = os.path.join('data', 'circuits', 'images', 'sochi.png')

with Image.open(circuit) as img:
    ANCHO, ALTO = img.size

# Definir colores
BLANCO = (255, 255, 255)

# Configuración de la pantalla
pantalla = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Ejemplo de Click en Pygame")

# Cargar una imagen
imagen = pygame.image.load(circuit)
imagen = pygame.transform.scale(imagen, (ANCHO, ALTO))

# Bucle principal
ejecutando = True
while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            # Obtener la posición del clic
            print(f'Down: {pygame.mouse.get_pos()}')
        elif evento.type == pygame.MOUSEBUTTONUP:
            print(f'Up: {pygame.mouse.get_pos()}')
    # Mostrar la imagen en la pantalla
    pantalla.blit(imagen, (0, 0))

    # Actualizar la pantalla
    pygame.display.flip()

# Salir de Pygame
pygame.quit()
sys.exit()
