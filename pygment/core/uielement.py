from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any

import pygame

from pygment.core import callback_property
from pygment.core.eventtarget import EventTarget

from pygment.editor.unit import SizeUnitType, str_to_unit
from pygment.editor.type import _UnitRect
from pygment.editor import Style
        

class UIElement(EventTarget, ABC):
    """ Base class defining a renderable visual component. """
    on_mouse_over = callback_property()
    on_mouse_enter = callback_property()
    on_mouse_click = callback_property()
    on_mouse_down = callback_property()
    on_mouse_up = callback_property()
    on_mouse_leave = callback_property()
    
    
    def __init__(self, rect: _UnitRect, style: Style | dict[str, Any] = {}, **kwargs: Any):
        self.x, self.y, self.width, self.height = rect
        self.style = style | kwargs
        self._hovered = False
        
    
    @property 
    def x(self) -> float | SizeUnitType:
        """ Get or set this component's x position.
        
            Setting this property to a str object will automatically parse it to a size unit object. 
            
            Raises:
                ValueError when setting the value to a string that could not be parsed to any size unit.
        """
        return self._x
    
    
    @x.setter
    def x(self, value: float | str | SizeUnitType) -> None:
        if isinstance(value, str):
            value = str_to_unit(value) 
        self._x = value
        
        
    def client_x(self, surface: pygame.surface.Surface) -> float:
        """ Compute this component's x position based on a passed surface's dimensions. 
        
            Getting the x position value with this method guarantees a float return type.

            Args:
                surface: pygame `Surface` object
        """
        return self._x.evaluate(self, surface) if isinstance(self._x, SizeUnitType) else self._x
        
        
    @property 
    def y(self) -> float | SizeUnitType:
        """ Get or set this component's y position.
        
            Setting this property to a str object will automatically parse it to a size unit object. 
            
            Raises:
                ValueError when setting the value to a string that could not be parsed to any size unit.
        """
        return self._y
    
    
    @y.setter
    def y(self, value: float | str | SizeUnitType) -> None:
        if isinstance(value, str):
            value = str_to_unit(value) 
        self._y = value
        
        
    def client_y(self, surface: pygame.surface.Surface) -> float:
        """ Compute this component's y position based on a passed surface's dimensions. 
        
            Getting the y position value with this method guarantees a float return type.

            Args:
                surface: pygame `Surface` object
        """
        return self._y.evaluate(self, surface) if isinstance(self._y, SizeUnitType) else self._y

        
    @property 
    def width(self) -> float | SizeUnitType:
        """ Get or set this component's width.
        
            Setting this property to a str object will automatically parse it to a size unit object. 
            
            Raises:
                ValueError when setting the value to a string that could not be parsed to any size unit.
        """
        return self._width
    
    
    @width.setter
    def width(self, value: float | str | SizeUnitType) -> None:
        if isinstance(value, str):
            value = str_to_unit(value) 
        self._width = value
        

    def client_width(self, surface: pygame.surface.Surface) -> float:
        """ Compute this component's width based on a passed surface's dimensions. 
        
            Getting the width value with this method guarantees a float return type.

            Args:
                surface: pygame `Surface` object
        """
        if isinstance(self._width, SizeUnitType):
            return self._width.evaluate(self, surface)
        return self._width
    
    
    @property 
    def height(self) -> float | SizeUnitType:
        """ Get or set this component's height.
        
            Setting this property to a str object will automatically parse it to a size unit object. 
            
            Raises:
                ValueError when setting the value to a string that could not be parsed to any size unit.
        """
        return self._height
    
    
    @height.setter
    def height(self, value: float | str | SizeUnitType) -> None:
        if isinstance(value, str):
            value = str_to_unit(value) 
        self._height = value


    def client_height(self, surface: pygame.surface.Surface) -> float:
        """ Compute this component's height based on a passed surface's dimensions. 
        
            Getting the height value with this method guarantees a float return type.

            Args:
                surface: pygame `Surface` object
        """
        if isinstance(self._height, SizeUnitType):
            return self._height.evaluate(self, surface)
        return self._height
    
    
    def client_rect(self, surface: pygame.surface.Surface) -> pygame.Rect:
        """ Return a new `pygame.Rect` object from this component's position and size based on a passed surface's dimensions. 
        
            Args:
                surface: pygame `Surface` object
        """
        x, y = self.client_x(surface), self.client_y(surface)
        w, h = self.client_width(surface), self.client_height(surface)
        return pygame.Rect(x, y, w, h)
    
    
    @property 
    def style(self) -> Style:
        return self._style


    @style.setter
    def style(self, value: Style | dict[str, Any]) -> None:
        self._style = Style(value)
        
    
    @abstractmethod
    def update(self, dt: int) -> bool:
        """ Update the component state. 
        
            Args:
                dt: elapsed time is ms since the last frame
                
            Returns:
                `True` or `False` whether the component is dirty and should be rerendered
        """
        pass


    @abstractmethod
    def render(self, surface: pygame.surface.Surface) -> None:
        """ Draw the component on screen. 
        
            Args:
                surface: pygame `Surface` object
        """
        pass    
        