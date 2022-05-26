import pytest

from typing import Any

from pygment.editor import Style


@pytest.fixture
def style() -> Style:
    return Style(
                 color = 0xDEADBEEF, 
                 text_size = 20,
                 text_color = (255, 0, 0),
                 hidden = False
                )
    

@pytest.mark.parametrize("attr, value", [
    ("color",        0xDEADBEEF),
    ("text_size",            20),
    ("text_color",  (255, 0, 0)),
    ("hidden",            False)
])
def test_style_getattr(style: Style, attr: str, value: Any):
    assert getattr(style, attr) == value
    
    
def test_style_setattr(style: Style):
    style.custom = "custom"
    assert style["custom"] == "custom"
    
    
def test_style_overwrite_raises(style: Style):
    with pytest.raises(AttributeError):
        style.get = lambda *_, **__: None
        
        
@pytest.mark.parametrize("attr, ret_type", [
    ("color",  tuple[int, int, int] | int),
    ("text_size",             int | float),
    ("text_color",        tuple[int, ...]),
    ("hidden",                 int | bool)
])      
def test_style_type_checking_passes(style: Style, attr: str, ret_type: type):
    style.get(attr, "dummy_default", expected_type=ret_type)


@pytest.mark.parametrize("attr, ret_type", [
    ("color",  tuple[str | bool, ...]),
    ("text_size",        list | tuple),
    ("text_color",    tuple[str, ...]),
    ("hidden",                complex)
])      
def test_style_type_checking_raises(style: Style, attr: str, ret_type: type):
    with pytest.raises(TypeError):
        style.get(attr, "dummy_default", expected_type=ret_type)
        