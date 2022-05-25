from __future__ import annotations
from typing import Callable
import re

import pygame

import pygment
from pygment.editor.type import SizeUnitType

__all__ = ["sw", "sh", "pw", "ph", "str_to_unit"]


class sw(SizeUnitType):
    """ Graphic unit representing a 1% of the renderer surface width. """
    __slots__ = ("_value")
    def evaluate(self, obj: pygment.component.BaseComponent, surface: pygame.surface.Surface) -> int:
        return round(surface.get_width() * self._value)
    



class sh(SizeUnitType):
    """ Graphic unit representing a 1% of the renderer surface height. """
    __slots__ = ("_value")
    def evaluate(self, obj: pygment.component.BaseComponent, surface: pygame.surface.Surface) -> int:
        return round(surface.get_height() * self._value)
    
    
    

class pw(SizeUnitType):
    """ Graphic unit representing a 1% of the object's parent width. """
    __slots__ = ("_value")
    def evaluate(self, obj: pygment.component.BaseComponent, surface: pygame.surface.Surface) -> int:
        if not obj.parent:
            return round(surface.get_width() * self._value)
        
        parent_width = obj.parent.get_width(surface)
        return round(parent_width * self._value)
    
    
    
    
class ph(SizeUnitType):
    """ Graphic unit representing a 1% of the object's parent height. """
    __slots__ = ("_value")
    def evaluate(self, obj: pygment.component.BaseComponent, surface: pygame.surface.Surface) -> int:
        if not obj.parent:
            return round(surface.get_height() * self._value)

        parent_height = obj.parent.get_height(surface)
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
