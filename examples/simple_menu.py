import pygame
import pygment
from pygment.component import BlockComponent, Div

COL_BLACK = (5,5,6)
COL_DARKGRAY = (23,22,26)
COL_LIGHTGRAY = (34,32,38)


pygame.init()
pygame.display.set_caption("Pygment example")
window = pygame.display.set_mode((500, 600), flags=pygame.RESIZABLE)
clock = pygame.time.Clock()

header = BlockComponent("header", (0, 0, "100sw", 50))
header.style.color = COL_DARKGRAY

button_style = {
    "color": COL_DARKGRAY, 
    "border_thickness": 2, 
    "border_radius": 10, 
    "border_color": COL_LIGHTGRAY
    }

section = Div("section", ("15sw", 100, "70sw", 270), color=(30,20,60), border_radius=20)
section.add(BlockComponent("button1", ("10pw", 50, "80pw", 70), style=button_style))
section.add(BlockComponent("button2", ("10pw", 150, "80pw", 70), style=button_style))

section.button1.on_mouse_enter = lambda obj: setattr(obj.style, "color", COL_LIGHTGRAY)
section.button1.on_mouse_leave = lambda obj: setattr(obj.style, "color", COL_DARKGRAY)
section.button2.on_mouse_click = lambda obj: print("click!")

layout = (header, section)
renderer = pygment.ViewRenderer(window.get_size(), layout)


finished = False
while not finished:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
            
        if event.type == pygame.VIDEORESIZE:
            renderer.size = event.size
            
    dt = clock.tick(60)
    renderer.update(dt)

    window.fill(COL_BLACK)
    renderer.render(window, (0, 0))
    pygame.display.flip()
    