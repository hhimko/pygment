import pygame
import pygment

COL_BLACK = (5,5,6)
COL_DARKGRAY = (23,22,26)
COL_LIGHTGRAY = (34,32,38)


pygame.init()
pygame.display.set_caption("Pygment example")
window = pygame.display.set_mode((400, 600), flags=pygame.RESIZABLE)

header = pygment.component.BlockComponent("header", (0, 0, "100sw", 50))
header.style.color = COL_DARKGRAY

button_style = {
    "color": COL_DARKGRAY, 
    "border_thickness": 4, 
    "border_radius": 20, 
    "border_color": COL_LIGHTGRAY
    }

button1 = pygment.component.BlockComponent("button1", ("15sw", 100, "70sw", 70), style=button_style)
button2 = pygment.component.BlockComponent("button2", ("15sw", 200, "70sw", 70), style=button_style)

layout = (header, button1, button2)
renderer = pygment.ViewRenderer(window.get_size(), layout)


finished = False
while not finished:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
            
        if event.type == pygame.VIDEORESIZE:
            renderer.size = event.size
            
    window.fill(COL_BLACK)
    renderer.render(window, (0, 0))
    pygame.display.flip()
    