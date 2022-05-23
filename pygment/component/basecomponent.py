from __future__ import annotations
from abc import ABC, abstractmethod
from weakref import ReferenceType

import pygment
from pygment.editor.type import SizeUnitType, _UnitRect
from pygment.editor.unit import str_to_unit
        
_TupleI3 = tuple[int,int,int]     
_TupleI4 = tuple[int,int,int,int]


class BaseComponent(ABC):
    """ Base class defining a renderable UI element. """
    def __init__(self, name: str, rect: _UnitRect):
        self._name = name
        self._parent: ReferenceType[BaseComponent] | None = None
        
        self.x, self.y, self.width, self.height = rect
        
        self._dirty = True # forces the element to be redrawn on first render
        
    
    @property
    def name(self) -> str:
        return self._name
    
    
    @property
    def parent(self) -> BaseComponent | None:
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
        
        
    def get_x(self, renderer: pygment.ViewRenderer) -> float:
        """ Compute this component's x position for a passed renderer screen.
        
            Getting the x position value with this method guarantees a float return type.

            Args:
                renderer: `ViewRenderer` object from where to get the surface dimensions
        """
        if isinstance(self._x, SizeUnitType):
            return self._x.evaluate(self, renderer)
        return self._x
        
        
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
        
        
    def get_y(self, renderer: pygment.ViewRenderer) -> float:
        """ Compute this component's y position for a passed renderer screen.
        
            Getting the y position value with this method guarantees a float return type.

            Args:
                renderer: `ViewRenderer` object from where to get the surface dimensions
        """
        if isinstance(self._y, SizeUnitType):
            return self._y.evaluate(self, renderer)
        return self._y

        
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
        

    def get_width(self, renderer: pygment.ViewRenderer) -> float:
        """ Compute this component's width for a passed renderer screen.
        
            Getting the width value with this method guarantees a float return type.

            Args:
                renderer: `ViewRenderer` object from where to get the surface dimensions
        """
        if isinstance(self._width, SizeUnitType):
            return self._width.evaluate(self, renderer)
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


    def get_height(self, renderer: pygment.ViewRenderer) -> float:
        """ Compute this component's height for a passed renderer screen.
        
            Getting the height value with this method guarantees a float return type.

            Args:
                renderer: `ViewRenderer` object from where to get the surface dimensions
        """
        if isinstance(self._height, SizeUnitType):
            return self._height.evaluate(self, renderer)
        return self._height
    
    
    def join(self, container: pygment.component.BaseContainer[BaseComponent]) -> None:
        """ Join a container component as a child in order to inherit its style.
            Alernatively you can call `container.add(component)`.

            Args:
                container: the container to join
                
            Raises:
                `ValueError` when the component is already assigned to a different parent or the container
                already contains an component with the same name
        """
        container.add(self)
    
    
    @abstractmethod
    def update(self, dt: int) -> None:
        """ Update the component state. 
        
            Args:
                dt: elapsed time is ms since the last frame
        """
        pass


    @abstractmethod
    def render(self, renderer: pygment.ViewRenderer) -> None:
        """ Draw the component on screen. 
        
            Args:
                renderer: `ViewRenderer` object
        """
        pass
        