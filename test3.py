import pygame

pygame.init()

width, height = 400, 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Comprobar Color de una Línea")

# Dibujar una línea (por ejemplo, roja)
pygame.draw.line(screen, (255, 0, 0), (100, 100), (300, 300), 2)

pygame.display.flip()

# Obtener el color en una posición específica (por ejemplo, en el centro de la línea)
x_centro = (100 + 300) // 2
y_centro = (100 + 300) // 2

color_centro = screen.get_at((x_centro, y_centro))

print(f"El color en el centro de la línea es: {color_centro}")

# Mantener la ventana abierta hasta que se cierre
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            color_centro = screen.get_at(pygame.mouse.get_pos())
            print(f"El color del sitio donde has hecho click es: {color_centro}")

pygame.quit()
