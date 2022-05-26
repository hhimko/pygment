import pygame
import pygment


pygame.init()
window = pygame.display.set_mode((400, 600), flags=pygame.RESIZABLE)

renderer = pygment.ViewRenderer(window)
layout = [
    pygment.component.BlockComponent("elem", ("25sw", 100, "50sw", 100))
]

layout[0].style = {"color": 0xFFCCFF, "border_thickness": 6, "border_radius": 30, "border_color": 0xBB66BB}

finished = False
while not finished:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
            
    window.fill(0xFFFFFF)
    renderer.render(layout)
    pygame.display.flip()