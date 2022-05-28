from __future__ import annotations
from abc import ABC, abstractmethod
from weakref import ReferenceType
from typing import Any

import pygame
from pygment.core import callback_property

from pygment.editor.unit import SizeUnitType, str_to_unit
from pygment.editor.type import _UnitRect
from pygment.editor import Style
import pygment.component.bases
        

class BaseComponent(ABC):
    """ Base class defining a renderable UI element. """
    on_mouse_over = callback_property()
    on_mouse_enter = callback_property()
    on_mouse_leave = callback_property()
    
    def __init__(self, name: str, rect: _UnitRect, style: Style | dict[str, Any] = {}, **kwargs):
        self._name = name
        self._parent: ReferenceType[BaseComponent] | None = None
        self._hovered = False
        
        self.x, self.y, self.width, self.height = rect
        
        self.style = style | kwargs
        
    
    @property
    def name(self) -> str:
        """ Get this component's name. """
        return self._name
    
    
    @property
    def parent(self) -> BaseComponent | None:
        """ Get this component's parent element. 
            
            If this object doesn't have a parent, None is returned. 
        """
        if not self._parent:
            return None
        return self._parent()
    
    
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
        
        
    def get_x(self, surface: pygame.surface.Surface) -> float:
        """ Compute this component's x position based on a passed surface's dimensions. 
        
            Getting the x position value with this method guarantees a float return type.

            Args:
                surface: pygame `Surface` object
        """
        x = self._x.evaluate(self, surface) if isinstance(self._x, SizeUnitType) else self._x
        if self.parent:
            x += self.parent.get_x(surface)
        return x
        
        
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
        
        
    def get_y(self, surface: pygame.surface.Surface) -> float:
        """ Compute this component's y position based on a passed surface's dimensions. 
        
            Getting the y position value with this method guarantees a float return type.

            Args:
                surface: pygame `Surface` object
        """
        y = self._y.evaluate(self, surface) if isinstance(self._y, SizeUnitType) else self._y
        if self.parent:
            y += self.parent.get_y(surface)
        return y

        
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
        

    def get_width(self, surface: pygame.surface.Surface) -> float:
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


    def get_height(self, surface: pygame.surface.Surface) -> float:
        """ Compute this component's height based on a passed surface's dimensions. 
        
            Getting the height value with this method guarantees a float return type.

            Args:
                surface: pygame `Surface` object
        """
        if isinstance(self._height, SizeUnitType):
            return self._height.evaluate(self, surface)
        return self._height
    
    
    def get_rect(self, surface: pygame.surface.Surface) -> pygame.Rect:
        """ Return a new `pygame.Rect` object from this component's position and size based on a passed surface's dimensions. 
        
            Args:
                surface: pygame `Surface` object
        """
        x, y = self.get_x(surface), self.get_y(surface)
        w, h = self.get_width(surface), self.get_height(surface)
        return pygame.Rect(x, y, w, h)
    
    
    @property
    def hovered(self) -> bool:
        """ Get or set this components hover state. """
        return self._hovered
    
    
    @hovered.setter
    def hovered(self, state: bool) -> None:
        if state != self._hovered:
            if state:
                self.on_mouse_enter()
            else:
                self.on_mouse_leave()
        self._hovered = state
    
    
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
        if self._hovered:
            self.on_mouse_over()
        
        return self.style.poll_changes()


    @abstractmethod
    def render(self, surface: pygame.surface.Surface) -> None:
        """ Draw the component on screen. 
        
            Args:
                surface: pygame `Surface` object
        """
        pass    
    
    
    def join(self, container: pygment.component.bases.BaseContainer) -> None:
        """ Join a container component as a child in order to inherit its style.
            Alernative way of calling `container.add(component)`.

            Args:
                container: the container to join
                
            Raises:
                `ValueError` when the component is already assigned to a different parent or the container
                already contains an component with the same name
        """
        container.add(self)
        