from typing import TypeVar
from abc import ABC


_T = TypeVar('_T', bound=ABC) 
def make_concrete(abctype: type[_T]) -> type[_T]:
    """ Factory method for creating concrete types from abstract types.
    
        All abstract methods in the new type are overwritten with a NO-OP function. 
    """
    new_dict = dict(abctype.__dict__)
    for abstractmethod in getattr(abctype, "__abstractmethods__"):
        new_dict[abstractmethod] = lambda *args, **kwargs: None
        
    return type(abctype.__name__, (abctype,), new_dict) # type: ignore