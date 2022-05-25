from typing import Any, TypeVar


_VT = TypeVar("_VT", bound=Any)
class Style(dict[str, Any]):
    """ Dictionary based class for defining component visual style. """
    def get(self, key: str, /, default: _VT) -> _VT:
        return super().get(key, default)
    
    
    def __getattr__(self, name: str) -> Any:
        return super().__getitem__(name)
    
    
    def __setattr__(self, name: str, value: Any) -> None:
        if name in dir(self):
            raise AttributeError(f"attribute '{name}' is read-only")
        return super().__setitem__(name, value)
    