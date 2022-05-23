from __future__ import annotations
from typing import Generic, TypeVar, Iterator
import weakref

from pygment.component.basecomponent import BaseComponent
from pygment.editor.type import _UnitRect


_T = TypeVar('_T', bound=BaseComponent)
class BaseContainer(BaseComponent, Generic[_T]):
    def __init__(self, name: str, rect: _UnitRect, *elements: _T, **kwargs):
        super().__init__(name, rect, **kwargs)
        self.elements: dict[str, _T] = {} # built-in dict has the ability to remember insertion order since python3.7
        
        for element in elements:
            self.add(element)
            
    
    def add(self, component: _T) -> None:
        """ Add a new component to this container in order to make it inherit this object's style. 
            Alernatively you can call `component.join(container)`.
        
            Args:
                component: the element to be added 
                
            Raises:
                `ValueError` when the component is already assigned to a different parent or this container
                already contains an component with the same name. 
        """
        if component.parent and component.parent != self:
            raise ValueError(f"component '{component}' already has a parent assigned as '{component.parent}'")
        if component.name in self.elements:
            raise ValueError(f"container '{self}' already contains an object with the same name '{component.name}'")
        
        self.elements[component.name] = component
        component._parent = weakref.ref(self)
        
        
    def __getattr__(self, attr: str) -> _T:
        if not "elements" in dir(self):
            raise KeyError(f"Container '{self.name}' is missing 'self.elements'")
        
        element = self.elements.get(attr) 
        if element is None:
            raise AttributeError(f"container '{self.name}' does not contain element with name '{attr}'")
        
        return element
    
    
    def __len__(self) -> int:
        return len(self.elements)
        
        
    def __iter__(self) -> Iterator[_T]:
        return iter(self.elements.values())