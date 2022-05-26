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
                        return type(val) is list and all(isinstance_generic(v, args[0]) for v in val)
                    elif origin is tuple:
                        if args[1] is Ellipsis:
                            return type(val) is tuple and all(isinstance_generic(v, args[0]) for v in val)
                        return type(val) is tuple and len(val) == len(args) and all(isinstance_generic(v, a) for v,a in zip(val, args))
                    else: 
                        return True
                else:
                    return True
        except Exception:
            return True  
    return True
        
        
        
        
_type = type
_VT = TypeVar("_VT", bound=Any)
class Style(dict[str, Any]):
    """ Dictionary based class for defining component visual style. """
    def get(self, key: str, /, default: _VT, type: type[_VT] = Type[_VT]) -> _VT:
        """ Return the value for key if key is in the dictionary, else default. 
        
            The function lets you specify an expected return type to check against the retrieved value.
            This functionality is however python implementation dependant and not guaranteed.
            
            Attr:
                key: the key to lookup in the dictionary
                default: the default return value
                type: optional return type specifier to check at runtime
            
            Raises:
                TypeError when the retrieved value doesn't match against the type parameter 
        """
        attr = super().get(key, default)
        if type and not isinstance_generic(attr, type):
            raise TypeError(f"key '{key}' type expected to be '{type}', got '{_type(attr)}' instead")
        return attr
    
    
    def __getattr__(self, name: str) -> Any:
        return super().__getitem__(name)
    
    
    def __setattr__(self, name: str, value: Any) -> None:
        if name in dir(self):
            raise AttributeError(f"attribute '{name}' is read-only")
        return super().__setitem__(name, value)
    