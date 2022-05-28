import pygame
from .blockcomponent import BlockComponent
from .bases import BaseContainer


class Div(BaseContainer, BlockComponent): 
    def render(self, surface: pygame.surface.Surface) -> None:
        super().render(surface)
        for component in self:
            component.render(surface)
            