import pygame
import pygment


class Renderable(pygment.component.BaseComponent):
    def update(self, dt):
        pass
    
    def render(self, surface):
        surface.fill(self.style.get("color", 0xFF00000))


pygame.init()
window = pygame.display.set_mode((400, 600), flags=pygame.RESIZABLE)

renderer = pygment.ViewRenderer(window)
layout = [
    Renderable("component1", ("25sw","25sh","50sw","50sh"), color=0xFFFF00)
]

finished = False
while not finished:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
            
    window.fill(0xFFFFFF)
    renderer.render(layout)
    pygame.display.flip()