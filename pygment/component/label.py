import pygame

from pygment.core.layoutnode import LayoutNode
from pygment.editor.type import _ColorValue


class Label(LayoutNode):
    """ Renderable component class. """
    def render(self, surface: pygame.surface.Surface) -> None:
        if not self.style.get("hidden", False, expected_type=bool):
            text = self.style.get("text", "", str)
            if text:
                rect = self.client_rect(surface)
                text_color = self.style.get("text_color", (255,255,255), expected_type=_ColorValue)
                text_size = self.style.get("text_size", -1, expected_type=int | float)
                if text_size < 0:
                    text_size = round(self.client_height(surface))
                
                font = pygame.font.Font(None, round(text_size * 1.3))
                mask = rect.move((-rect.x, -rect.y))
                surface.blit(font.render(text, True, text_color), rect, mask)
                
                
    def update(self, dt: int) -> bool:
        dirty = bool(self.style.poll_changes())
        for component in self:
            dirty |= component.update(dt)
            
        return dirty | self._dirty
    