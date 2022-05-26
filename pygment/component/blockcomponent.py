import pygame

from .bases import BaseComponent
import pygment.editor.type


_ColorValue = pygment.editor.type._ColorValue


class BlockComponent(BaseComponent):
    """ Renderable component class. """
    def update(self, dt: int) -> None:
        pass
    
    
    def render(self, surface: pygame.surface.Surface) -> None:
        if not self.style.get("hidden", False, expected_type=bool):
            rect = self.get_rect(surface)
            color = self.style.get("color", 0, expected_type=_ColorValue)
            
            border_radius = round(max(self.style.get("border_radius", 0, expected_type=int | float), 0))
            border_thickness = round(max(self.style.get("border_thickness", 0, expected_type=int | float), 0))
            
            pygame.draw.rect(surface, color, rect, border_radius=border_radius)
            
            if border_thickness > 0:
                border_color = self.style.get("border_color", 0, expected_type=_ColorValue)
                pygame.draw.rect(surface, border_color, rect, border_thickness, border_radius)
            
            
