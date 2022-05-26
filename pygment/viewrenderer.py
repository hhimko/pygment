from weakref import WeakKeyDictionary
from typing import Sequence
import uuid

from pygment.component.bases import BaseComponent
import pygame


class ViewRenderer:
    def __init__(self, surface: pygame.surface.Surface) -> None:
        self._surface = surface
        self._surface_size = (0, 0) 
        self._surf_cache = WeakKeyDictionary[uuid.UUID, tuple[pygame.surface.Surface, pygame.Rect]]()

        
    @property
    def surface(self) -> pygame.surface.Surface:
        """ Get and set the surface on which the ViewRenderer will render. """
        return self._surface
    
    
    @surface.setter
    def surface(self, surface: pygame.surface.Surface) -> None:
        self._surface = surface
        
        
    def render(self, layout: Sequence[BaseComponent]) -> None:
        surf_size = self.surface.get_size()
        if self._surface_size != surf_size:
            self._surf_cache.clear()
            self._surface_size = surf_size
        
        for component in layout: 
            cached = self._surf_cache.get(component.uuid)
            if not cached or component.is_dirty:
                overlay = pygame.surface.Surface(surf_size)
                mask = component.get_rect(self.surface)
                
                component.render(overlay)
                component.is_dirty = False
                   
                self._surf_cache[component.uuid] = (overlay, mask)
            else:    
                overlay, mask = cached
                
            
            self.surface.blit(overlay, mask, mask)
                
            