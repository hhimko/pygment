from __future__ import annotations
from typing import Any, Iterator
import weakref

import pygame

from pygment.core.uielement import UIElement
from pygment.editor.type import _UnitRect
from pygment.editor import Style


class LayoutNode(UIElement):
    """ Represents a linked node that can store a number of ordered children. """
    def __init__(self, name: str, rect: _UnitRect, style: Style | dict[str, Any] = {}, **kwargs: Any):
        super().__init__(rect, style, **kwargs)
        self.__dict__["_elements"] = {} # built-in dict has the ability to remember insertion order since python3.7
        self._elements: dict[str, LayoutNode]
        self._parent: weakref.ReferenceType[LayoutNode] | None = None

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
    
    
    def client_x(self, surface: pygame.surface.Surface) -> float:
        x = super().client_x(surface)
        if self.parent:
            x += self.parent.client_x(surface)
        return x
    
    
    def client_y(self, surface: pygame.surface.Surface) -> float:
        y = super().client_y(surface)
        if self.parent:
            y += self.parent.client_y(surface)
        return y
    
    
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
    