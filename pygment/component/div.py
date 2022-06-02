import pygame
from .blockcomponent import BlockComponent


class Div(BlockComponent): 
    def render(self, surface: pygame.surface.Surface) -> None:
        super().render(surface)
        for component in self:
            component.render(surface)
            