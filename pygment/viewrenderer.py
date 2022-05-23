import pygame


class ViewRenderer:
    def __init__(self, surface: pygame.surface.Surface):
        self.surface = surface
        
        
    def render(self, layout) -> None:
        for element in layout:
            element.render()
            