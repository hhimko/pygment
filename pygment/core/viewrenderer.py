from __future__ import annotations
from typing import Callable

import pygame

from pygment.core.layoutnode import LayoutNode
from pygment.core.uielement import UIElement


class ViewRenderer:
    def __init__(self, size: tuple[int, int], layout: tuple[LayoutNode, ...]):
        self._surface = pygame.surface.Surface(size).convert_alpha()
        self._surface.fill((0,0,0,0))
        
        self._dirty: set[LayoutNode] = set(layout)
        self._pressed: set[UIElement] = set()
        self._hovered: set[UIElement] = set()
        self._layout = layout
        
        
    @property
    def surface(self) -> pygame.surface.Surface:
        """ Get the renderer's cached surface. """
        return self._surface
    
    
    @property
    def layout(self) -> tuple[LayoutNode, ...]:
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
        lmb_pressed = pygame.mouse.get_pressed()[0]
        
        for component in self._layout:
            self._update_mouse_hover(component, mouse_pos)
            self._update_mouse_click(component, lmb_pressed)
               
            if component.update(dt):
                self._dirty.add(component)
            
        
    def render(self, dest_surface: pygame.surface.Surface, dest: tuple[int, int]) -> None:
        """ Render this renderer's contents to a desired `pygame.Surface` object.
        
            Args:
                dest_surface: the destination surface to render to
                dest: the destination (x, y) cordinates 
        """
        for component in self._dirty:
            self._surface.fill((0,0,0,0), component.client_rect(self._surface))
            self._cascade_action(component, lambda component: component.render(self._surface))
            component._dirty = False
            
        self._dirty.clear()
        dest_surface.blit(self._surface, dest)
        
        
    def _update_mouse_click(self, component: LayoutNode, mouse_pressed: bool) -> None:
        was_pressed = component in self._pressed
        is_pressed  =  mouse_pressed and component in self._hovered
        if is_pressed: component.on_mouse_down()
        
        if was_pressed != is_pressed:
            if is_pressed:
                component.on_mouse_click()
                self._pressed.add(component)
            else:
                component.on_mouse_up()
                self._pressed.remove(component)
        
        for child in component.children:
            self._update_mouse_click(child, mouse_pressed)
        
        
    def _update_mouse_hover(self, component: LayoutNode, mouse_pos: tuple[int, int]) -> None:
        was_hover = component in self._hovered
        is_hover  = component.client_rect(self._surface).collidepoint(mouse_pos)
        if is_hover: component.on_mouse_over()
        
        if was_hover != is_hover:
            if is_hover: 
                component.on_mouse_enter()
                self._hovered.add(component)
            else: 
                component.on_mouse_leave()
                self._hovered.remove(component)
        
        for child in component.children:
            self._update_mouse_hover(child, mouse_pos)
            
            
    def _get_element_by_id(self, name: str) -> UIElement: # TODO: exctract to Body object
        def _recget(component: LayoutNode) -> UIElement | None:
            if component.name == name: return component
            
            for child in component:
                return _recget(child)
            
        for element in self._layout:
            out = _recget(element)
            if out: return out
            
        raise KeyError(f"element with name {name} is missing from view body")
    
    
    @classmethod
    def _cascade_action(cls, component: LayoutNode, action: Callable[[LayoutNode], None]) -> None:
        action(component)
        for child in component:
            cls._cascade_action(child, action)
            