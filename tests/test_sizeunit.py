import pytest

from pygment.editor.type import SizeUnitType
from pygment.editor.unit import sw, sh, pw, ph, str_to_unit


@pytest.mark.parametrize("unit_spec, expected", [
        ("0",           float),
        (".10px",       float),
        ("0sw",            sw),
        ("2.sh",           sh),
        ("5  ph",          ph),
        (" -1.2pw",        pw)
])
def test_str_to_unit_returns_expected_type(unit_spec: str, expected: type):
    unit = str_to_unit(unit_spec)
    assert isinstance(unit, expected)
    
    
@pytest.mark.parametrize("unit_spec, expected", [
        ("1",               1),
        (".0px",          0.0),
        ("12 sh",          12),
        ("-98.76pw",   -98.76)
])
def test_str_to_unit_returns_expected_value(unit_spec: str, expected: float):
    unit = str_to_unit(unit_spec)
    value = unit.value if isinstance(unit, SizeUnitType) else unit
    assert value == expected
    
        
@pytest.mark.parametrize("unit_spec", [
        "",
        " ",
        ".",
        ".sw",
        "_ph",
        "abc",
        "100p x",
        "1 . 1sh",
        " 25 pw ."
])
def test_str_to_unit_fails(unit_spec: str):
    with pytest.raises(ValueError):
        str_to_unit(unit_spec)
        