from functools import partial
from typing import Any, Callable


class callback_property(property):
    """ Descriptor class for callable properties. 

        callback_property makes sure a property is always callable, giving it 
        a NO_OP method callback by default. 

        A callbackproperty instance can be set to either a callable method or
        `None`, which works the same way as deleting the propetry with the `del`
        keyword and resets the callback to NO_OP.

        When setting a callbackproperty to a callable, it's automatically injected
        with a `self`-like argument.
    """
    def __init__(self):
        """ Make a new descriptor property for callable types. """
        super().__init__(self._getter, self._setter, self._deleter)


    @staticmethod
    def NO_OP(*args, **kwargs) -> None:
        pass
    
    
    def __set_name__(self, obj: type, name: str) -> None:
        self.callback_accessor = f"_{name}"
        setattr(obj, self.callback_accessor, self.NO_OP)


    def _getter(self, obj: Any) -> Callable[[None], None]:
        return getattr(obj, self.callback_accessor)
    
    
    def _setter(self, obj: Any, callback: Callable[[None], None] | Callable[[], None] | None) -> None:
        if callback is None:
            return self._deleter(obj)
        
        if not callable(callback):
            raise ValueError(f"callback property {self.callback_accessor[1:]} expected a callable, got {type(callback)} instead")

        if callback.__code__.co_argcount == 1:
            callback = partial(callback, obj)
        setattr(obj, self.callback_accessor, callback)
            
        
    def _deleter(self, obj: Any) -> None: # type: ignore
        setattr(obj, self.callback_accessor, self.NO_OP)