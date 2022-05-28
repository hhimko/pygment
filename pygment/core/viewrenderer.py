from __future__ import annotations

import pygame

from pygment.component.bases import BaseComponent


class ViewRenderer:
    def __init__(self, size: tuple[int, int], layout: tuple[BaseComponent, ...]):
        self._surface = pygame.surface.Surface(size).convert_alpha()
        self._surface.fill((0,0,0,0))
        
        self._dirty: set[BaseComponent] = set(layout)
        self._layout = layout

        
    @property
    def surface(self) -> pygame.surface.Surface:
        """ Get the renderer's cached surface. """
        return self._surface
    
    
    @property
    def layout(self) -> tuple[BaseComponent, ...]:
        """ Get this renderer's layout. """
        return self._layout
    
    
    @property
    def size(self) -> tuple[int, int]:
        """ Get or set this renderer's surface size. """
        return self._surface.get_size()
    
    
    @size.setter
    def size(self, size: tuple[int, int]) -> None:
        self._surface = pygame.surface.Surface(size).convert_alpha()
        self._surface.fill((0,0,0,0))
        
        self._dirty = set(self._layout)
        
        
    def update(self, dt: int) -> None:
        """ Update the state of this renderer's layout by `dt` ticks. """
        mouse_pos = pygame.mouse.get_pos()
        
        for component in self._layout:
            component.hovered = component.get_rect(self._surface).collidepoint(mouse_pos)
               
            if component.update(dt):
                self._dirty.add(component)
            
        
    def render(self, dest_surface: pygame.surface.Surface, dest: tuple[int, int]) -> None:
        """ Render this renderer's contents to a desired `pygame.Surface` object.
        
            Args:
                dest_surface: the destination surface to render to
                dest: the destination (x, y) cordinates 
        """
        for component in self._dirty:
            self._surface.fill((0,0,0,0), component.get_rect(self._surface))
            component.render(self._surface)
            
        self._dirty.clear()
        dest_surface.blit(self._surface, dest)
            