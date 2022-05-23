import pygame
import pygment


pygame.init()
window = pygame.display.set_mode((400, 600))

renderer = pygment.ViewRenderer(window)
layout = [
    
]


finished = False
while not finished:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
            
    renderer.render(layout)
