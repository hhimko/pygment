import pygame

from pygment.core.layoutnode import LayoutNode
from pygment.editor.type import _ColorValue


class Button(LayoutNode):
    """ Renderable component class. """
    def render(self, surface: pygame.surface.Surface) -> None:
        if not self.style.get("hidden", False, expected_type=bool):
            rect = self.client_rect(surface)
            color = self.style.get("color", (255,255,255), expected_type=_ColorValue)
            
            border_radius = round(max(self.style.get("border_radius", 10, expected_type=int | float), 0))
            border_thickness = round(max(self.style.get("border_thickness", 0, expected_type=int | float), 0))
            
            pygame.draw.rect(surface, color, rect, border_radius=border_radius)
            
            if border_thickness > 0:
                border_color = self.style.get("border_color", 0, expected_type=_ColorValue)
                pygame.draw.rect(surface, border_color, rect, border_thickness, border_radius)
                
                
    def update(self, dt: int) -> bool:
        dirty = bool(self.style.poll_changes())
        for component in self:
            dirty |= component.update(dt)
            
        return dirty | self._dirty
    