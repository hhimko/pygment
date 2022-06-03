import pygame

from pygment.core.layoutnode import LayoutNode


class Image(LayoutNode):
    """ Renderable component class. """
    def render(self, surface: pygame.surface.Surface) -> None:
        if not self.style.get("hidden", False, expected_type=bool):
            source = self.style.get("source", "", str)
            if source:
                rect = self.client_rect(surface)
                
                image = pygame.image.load(source)
                image = pygame.transform.smoothscale(image, rect.size)
                
                mask = rect.move((-rect.x, -rect.y))
                surface.blit(image, rect, mask)
                
                
    def update(self, dt: int) -> bool:
        dirty = bool(self.style.poll_changes())
        for component in self:
            dirty |= component.update(dt)
            
        return dirty | self._dirty
    