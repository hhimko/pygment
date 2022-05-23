from typing import Generic, TypeVar
import weakref

from pygment.component.basecomponent import BaseComponent
from pygment.editor.type import _UnitRect


T = TypeVar('T', bound=BaseComponent)
class BaseContainer(BaseComponent, Generic[T]):
    def __init__(self, name: str, rect: _UnitRect, *elements: T):
        super().__init__(name, rect)
        self.elements: dict[str, T] = {} # built-in dict has the ability to remember insertion order since python3.7
        
        for element in elements:
            self.add(element)
    
    def add(self, component: T) -> None:
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
            raise AttributeError(f"container '{self}' already contains an object with the same name '{component.name}'")
        component._parent = weakref.ref(self)