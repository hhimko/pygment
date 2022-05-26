from __future__ import annotations

import pygment.editor.unit 

        
_UnitRect = tuple[float | str | pygment.editor.unit.SizeUnitType, float | str | pygment.editor.unit.SizeUnitType, float | str | pygment.editor.unit.SizeUnitType, float | str | pygment.editor.unit.SizeUnitType]
_ColorValue = int | str | tuple[int, int, int, int] | tuple[int, int, int]
