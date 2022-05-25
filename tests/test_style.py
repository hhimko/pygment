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
