from __future__ import annotations
from typing import Iterator
import weakref

import pygame

from pygment.editor.unit import SizeUnitType, str_to_unit
from pygment.editor.type import _UnitRect


class LayoutNode:
    """ Represents a linked node that can store a number of ordered children. """
    def __init__(self, name: str, rect: _UnitRect):
        self.__dict__["_elements"] = {} # built-in dict has the ability to remember insertion order since python3.7
        self._elements: dict[str, LayoutNode]
        self._parent: weakref.ReferenceType[LayoutNode] | None = None
        
        self.x, self.y, self.width, self.height = rect
        self._name = name
        
    
    @property
    def name(self) -> str:
        return self._name
        
        
    @property
    def parent(self) -> LayoutNode | None:
        """ Get this component's parent element. 
            
            If this object doesn't have a parent, None is returned. 
        """
        if not self._parent:
            return None
        return self._parent()
    
    
    @property
    def children(self) -> tuple[LayoutNode]:
        return tuple(self._elements.values())
    
    
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
        x = self._x.evaluate(self, surface) if isinstance(self._x, SizeUnitType) else self._x
        if self.parent:
            x += self.parent.client_x(surface)
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
        
        
    def client_y(self, surface: pygame.surface.Surface) -> float:
        """ Compute this component's y position based on a passed surface's dimensions. 
        
            Getting the y position value with this method guarantees a float return type.

            Args:
                surface: pygame `Surface` object
        """
        y = self._y.evaluate(self, surface) if isinstance(self._y, SizeUnitType) else self._y
        if self.parent:
            y += self.parent.client_y(surface)
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
    
    
    def add(self, child: LayoutNode) -> None:
        """ Add a new component to this container in order to make it inherit this object's position and size. 
            Alernatively you can call `component.join(container)`.
        
            Args:
                child: the element to add
                
            Raises:
                `ValueError` when the component is already assigned to a different parent or this container
                already contains a child with the same name. 
        """
        if child.parent and child.parent != self:
            raise ValueError(f"component '{child}' already has a parent assigned as '{child.parent}'")
        if child.name in self._elements:
            raise ValueError(f"container '{self}' already contains a child with the same name '{child.name}'")
        
        self._elements[child.name] = child
        child._parent = weakref.ref(self)
        
        
    def join(self, parent: LayoutNode) -> None:
        """ Join a container component as a child in order to inherit its position and size.
            Alernative way of calling `container.add(component)`.

            Args:
                parent: the container to join
                
            Raises:
                `ValueError` when the component is already assigned to a different parent or the container
                already contains a child with the same name
        """
        parent.add(self)
        
        
    def __getattr__(self, attr: str) -> LayoutNode:
        element = self._elements.get(attr) 
        if element is None:
            raise AttributeError(f"container '{self.name}' does not contain element with name '{attr}'")
        
        return element
    
    
    def __len__(self) -> int:
        return len(self._elements)
        
        
    def __iter__(self) -> Iterator[LayoutNode]:
        return iter(self._elements.values())
    