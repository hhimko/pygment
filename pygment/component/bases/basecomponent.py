from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any

import pygame

from pygment.core.layoutnode import LayoutNode
from pygment.core import callback_property

from pygment.editor.type import _UnitRect
from pygment.editor import Style
        

class BaseComponent(LayoutNode, ABC):
    """ Base class defining a renderable UI element. """
    on_mouse_over = callback_property()
    on_mouse_enter = callback_property()
    on_mouse_click = callback_property()
    on_mouse_down = callback_property()
    on_mouse_up = callback_property()
    on_mouse_leave = callback_property()
    
    
    def __init__(self, name: str, rect: _UnitRect, style: Style | dict[str, Any] = {}, **kwargs):
        super().__init__(name, rect)
        self._hovered = False
        
        self.style = style | kwargs
    
    
    @property 
    def style(self) -> Style:
        return self._style


    @style.setter
    def style(self, value: Style | dict[str, Any]) -> None:
        self._style = Style(value)
        
    
    def update(self, dt: int) -> bool:
        """ Update the component state. 
        
            Args:
                dt: elapsed time is ms since the last frame
                
            Returns:
                `True` or `False` whether the component is dirty and should be rerendered
        """
        dirty = bool(self.style.poll_changes())
    
        for component in self.children:
            dirty |= component.update(dt)
            
        return dirty


    @abstractmethod
    def render(self, surface: pygame.surface.Surface) -> None:
        """ Draw the component on screen. 
        
            Args:
                surface: pygame `Surface` object
        """
        pass    
        