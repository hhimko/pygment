from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Callable
import re

import pygame

import pygment.core.layoutnode as layoutnode


__all__ = ["sw", "sh", "pw", "ph"]


class SizeUnitType(ABC):
    """ Abstract class representing a computable size unit. """
    __slots__ = ("_value")
    def __init__(self, value: float):
        self._value = value / 100
        
        
    @property 
    def value(self) -> float:
        return self._value * 100
    
    
    @value.setter
    def value(self, val: float) -> None:
        self._value = val / 100
        
        
    @abstractmethod
    def evaluate(self, obj: layoutnode.LayoutNode, surface: pygame.surface.Surface) -> int:
        """ Compute this unit's value for a given component and renderer. """
        pass
    
    
    @classmethod
    def parse(cls, value: str) -> SizeUnitType:
        """ Parse a string to a size unit object. 
    
            To successfully parse a str object it should consist of a parsable float value followed by this class's name.
            
            Args:
                value: the str object to parse
                
            Raises:
                ValueError when the string could not be parsed
        """
        value = value.rstrip()
        if not value.endswith(cls.__name__):
            raise ValueError(f"could not convert string to unit: '{value}'. value expected to end with '{cls.__name__}' identifier")
        
        try:
            return cls(float(value[:-2]))
        except ValueError:
            raise ValueError(f"could not convert string to unit: '{value}'. '{value[:-2]}' is not a parsable float value")

    
    def __repr__(self) -> str:
        return f"{self.value}{type(self).__name__}"




class sw(SizeUnitType):
    """ Graphic unit representing a 1% of the renderer surface width. """
    __slots__ = ("_value")
    def evaluate(self, obj: layoutnode.LayoutNode, surface: pygame.surface.Surface) -> int:
        return round(surface.get_width() * self._value)
    



class sh(SizeUnitType):
    """ Graphic unit representing a 1% of the renderer surface height. """
    __slots__ = ("_value")
    def evaluate(self, obj: layoutnode.LayoutNode, surface: pygame.surface.Surface) -> int:
        return round(surface.get_height() * self._value)
    
    
    

class pw(SizeUnitType):
    """ Graphic unit representing a 1% of the object's parent width. """
    __slots__ = ("_value")
    def evaluate(self, obj: layoutnode.LayoutNode, surface: pygame.surface.Surface) -> int:
        if not obj.parent:
            return round(surface.get_width() * self._value)
        
        parent_width = obj.parent.client_width(surface)
        return round(parent_width * self._value)
    
    
    
    
class ph(SizeUnitType):
    """ Graphic unit representing a 1% of the object's parent height. """
    __slots__ = ("_value")
    def evaluate(self, obj: layoutnode.LayoutNode, surface: pygame.surface.Surface) -> int:
        if not obj.parent:
            return round(surface.get_height() * self._value)

        parent_height = obj.parent.client_height(surface)
        return round(parent_height * self._value)
    
    
   

def str_to_unit(value: str) -> SizeUnitType | float:
    """ Parse a str object to a size unit.
    
        The supported format is `\\s+<float value>\\s+<unit identifier>\\s+` where `\\s+` means an optional sequence with arbitrary length 
        of white characters and `<unit identifier>` is either a name of any SizeUnitType subclass, 'px' or an empty string. 
        For the last two `<unit identifier>` value cases an unchanged float value parsed from `<float value>` is returned.
        
        Args:
            value: the string to be parsed
        
        Raises:
            ValueError when the string contents could not be parsed
    """
    unit_name_mapping: dict[str, type[SizeUnitType] | Callable[[float], float]] = {
        unit.__name__: unit  for unit in SizeUnitType.__subclasses__()
    }
    identity = lambda x: x # identity pipe for strings without unit identifiers and 'px' units 
    unit_name_mapping.update(
        {'': identity, "px": identity}
    ) 
    
    unit = re.sub(r"\A[\s\d\.-]+|\s+$", '', value)
    unit_wrapper = unit_name_mapping.get(unit)
    if not unit_wrapper:
        raise ValueError(f"could not convert string '{value}' to unit. invalid size unit identifier '{unit}'") 
    
    try:
        val = float(re.sub(r"[a-zA-Z_]+", '', value))
    except ValueError as e:
        raise ValueError(f"could not convert string '{value}' to unit. {e}")
    
    return unit_wrapper(val)
