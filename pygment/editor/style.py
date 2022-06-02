from typing import Any, TypeVar, Union, Type, no_type_check


__all__ = ["Style"]

_UnionType = type(Union[int, str]) | type(int | str)
_GenericAlias = type(tuple[int])


@no_type_check
def isinstance_generic(val: Any, type_spec: _UnionType | tuple[Type, ...]) -> bool:
    """ Helper function build on the top of builtin `isinstance` with addictional generic type checking functionality. 
        The definition of this function might be python implementation dependant. 
        
        Examples:
            `isinstance_generic((1, '2', 3.0), tuple[int, str, float]) == True` \n
            `isinstance_generic((0.1, 0.2, 0.3), tuple[float, ...]) == True` \n
            `isinstance_generic(['foo', 'bar', [1, 'a']], list[str | list[int | str]]) == True` \n
            `isinstance_generic(['foo', 'bar', [1.0, 'a']], list[str | list[int | str]]) == False`
    """
    try:
        return isinstance(val, type_spec)
    except TypeError: # catch parametrized generics 
        try: # this function might unfortunatelly be implementation dependant
            if isinstance(type_spec, tuple): # cast tuple to _UnionType
                type_spec = Union[type_spec] # type: ignore
                
            if isinstance(type_spec, _UnionType | _GenericAlias):
                if isinstance(type_spec, _GenericAlias): # type_spec is a singular value
                    generics = (type_spec,)
                else: # type_spec is a sequence of types
                    nongenerics = (t for t in type_spec.__args__ if type(t) is not _GenericAlias) # type: ignore
                    generics = (t for t in type_spec.__args__ if type(t) is _GenericAlias) # type: ignore
                    
                    if isinstance(val, tuple(nongenerics)): # try skipping generic checking
                        return True
                
                for t in generics:
                    origin: Type = t.__origin__ # type: ignore
                    args: tuple[Type, ...] = t.__args__ # type: ignore
                    if origin is list:
                        if type(val) is list and all(isinstance_generic(v, args[0]) for v in val): return True
                    elif origin is tuple:
                        if args[1] is Ellipsis:
                            if type(val) is tuple and all(isinstance_generic(v, args[0]) for v in val): return True
                        if type(val) is tuple and len(val) == len(args) and all(isinstance_generic(v, a) for v,a in zip(val, args)): return True
                    else: 
                        return True
                return False
        except Exception:
            return True  
    return True
        
        
        
        
_VT = TypeVar("_VT", bound=Any)
class Style(dict[str, Any]):
    def __init__(self, obj: dict[str, Any] = {}, **kwargs: Any):
        super().__init__(obj | kwargs)
        self.__dict__["_changes"] = {}
        self._changes: dict[str, Any]
    
    
    """ Dictionary based class for defining component visual style. """
    def get(self, key: str, /, default: _VT, expected_type: type[_VT]) -> _VT:
        """ Return the value for key if key is in the dictionary, else default. 
        
            The function lets you specify an expected return type to check against the retrieved value.
            This functionality is however python implementation dependant and not guaranteed.
            
            Attr:
                key: the key to lookup in the dictionary
                default: the default return value
                expected_type: return type specifier checked at runtime
            
            Raises:
                TypeError when the retrieved value doesn't match against the expected_type parameter 
        """
        attr = super().get(key, default)
        if not isinstance_generic(attr, expected_type):
            raise TypeError(f"key '{key}' type expected to be '{expected_type}', got '{attr}' of type '{type(attr)}' instead")
        return attr
    
    
    def poll_changes(self) -> dict[str, Any]:
        """ Returns names of style attribute changes that were made from when this method was last called. """
        changes = self._changes.copy()
        self._changes.clear()
        return changes
    
    
    def __getattr__(self, key: str) -> Any:
        return self.__getitem__(key)
    
    
    def __setattr__(self, key: str, value: Any) -> None:
        if key in dir(self):
            raise AttributeError(f"attribute '{key}' is read-only")
        self.__setitem__(key, value)
    
    
    def __setitem__(self, key: str, value: Any) -> None:
        prev = super().get(key)
        if value != prev:
            self._changes[key] = prev
        super().__setitem__(key, value)
    