from __future__ import annotations
from abc import ABC, abstractmethod

import pygment

__all__ = ["SizeUnitType"]


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
    def evaluate(self, obj: pygment.component.BaseComponent, renderer: pygment.ViewRenderer) -> int:
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
    
    
_UnitRect = tuple[float | str | SizeUnitType, float | str | SizeUnitType, float | str | SizeUnitType, float | str | SizeUnitType]
