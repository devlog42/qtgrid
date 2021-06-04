import pytest
from qtgrid.qtgrid import _Cell, _Gap

############################
# Check Qt package to import
import importlib

if importlib.util.find_spec("PyQt6") is not None:
    from PyQt6.QtWidgets import QLabel
elif importlib.util.find_spec("PyQt5") is not None:
    from PyQt5.QtWidgets import QLabel
elif importlib.util.find_spec("PySide6") is not None:
    from PySide6.QtWidgets import QLabel
else:
    raise Exception("Cannot find package PySide6, PyQt6, or PyQt5")

def test_add(grid, some_label):
    # Preapre
    grid.set_list_names( ["test_list"] )
    grid.set_content_columns( 4 )

    # Simple add
    grid.add( some_label )
    assert grid.wh.y == 0
    assert grid.wh.x == 0

    # Add with span and to_list
    label = grid._copy_label( some_label )
    grid.add( label, y_span=2, x_span=2, to_list="test_list" )
    assert grid.wh.y == 0
    assert grid.wh.x == 1
    assert not grid.spans.has( 0,0 ) # y,x
    assert grid.spans.has( 0,1 ) # y,x
    assert grid.spans.has( 0,2 ) # y,x
    assert grid.spans.has( 1,1 ) # y,x
    assert grid.spans.has( 1,2 ) # y,x
    # Check list
    widgets_list = grid.get_list("test_list")
    assert len(widgets_list) == 1
    assert isinstance(widgets_list[0], QLabel)

    # Simple add
    label = grid._copy_label( some_label )
    grid.add( label )
    assert grid.wh.y == 0
    assert grid.wh.x == 3

    # Simnple add / Next row
    label = grid._copy_label( some_label )
    grid.add( label )
    assert grid.wh.y == 1
    assert grid.wh.x == 0

    # Simple add / Skip reserved span area
    label = grid._copy_label( some_label )
    grid.add( label )
    assert grid.wh.y == 1
    assert grid.wh.x == 3

def test_add_label(grid, some_label):
    # Preapre
    grid.set_list_names( ["test_list"] )
    grid.set_content_columns( 4 )
    grid.set_label_source("test_label", some_label)

    # Simple add
    grid.add_label(name_id="test_label", text="foo1")
    assert grid.wh.y == 0
    assert grid.wh.x == 0

    # Add with span and to_list
    grid.add_label("test_label", "foo2", y_span=2, x_span=2, to_list="test_list" )
    assert grid.wh.y == 0
    assert grid.wh.x == 1
    assert not grid.spans.has( 0,0 ) # y,x
    assert grid.spans.has( 0,1 ) # y,x
    assert grid.spans.has( 0,2 ) # y,x
    assert grid.spans.has( 1,1 ) # y,x
    assert grid.spans.has( 1,2 ) # y,x
    # Check list
    widgets_list = grid.get_list("test_list")
    assert len(widgets_list) == 1
    assert isinstance(widgets_list[0], QLabel)

    # Simple add
    grid.add_label("test_label", "foo3")
    assert grid.wh.y == 0
    assert grid.wh.x == 3

    # Simnple add / Next row
    grid.add_label("test_label", "foo4")
    assert grid.wh.y == 1
    assert grid.wh.x == 0

    # Simple add / Skip reserved span area
    grid.add_label("test_label", "foo5")
    assert grid.wh.y == 1
    assert grid.wh.x == 3

def test_add_gap(grid):
    # Preapre
    grid.set_content_columns( 5 )

    # grid.add_gap( direction=None, length=None, y_span=1, x_span=1 )

    # horizontal - in first row
    # ----------
    # like None
    cell = grid.add_gap( direction="H" )
    assert isinstance(cell.item, _Gap)
    gap  = cell.item
    assert gap.item is None
    assert grid.wh.y == cell.y == 0
    assert grid.wh.x == cell.x == 0

    # like None
    cell = grid.add_gap( direction="H", length=0 )
    assert isinstance(cell.item, _Gap)
    assert grid.wh.y == cell.y == 0
    assert grid.wh.x == cell.x == 1

    # None
    cell = grid.add_gap("H", None)
    assert isinstance(cell.item, _Gap)
    assert grid.wh.y == cell.y == 0
    assert grid.wh.x == cell.x == 2

    # fixed size
    cell = grid.add_gap("H", 20)
    assert isinstance(cell.item, _Gap)
    assert grid.wh.y == cell.y == 0
    assert grid.wh.x == cell.x == 3

    # expand
    cell = grid.add_gap("H", "expand")
    assert isinstance(cell.item, _Gap)
    assert grid.wh.y == cell.y == 0
    assert grid.wh.x == cell.x == 4


    # horizontal is default - in second row
    # ---------------------
    # like None
    cell = grid.add_gap()
    assert isinstance(cell.item, _Gap)
    assert grid.wh.y == cell.y == 1
    assert grid.wh.x == cell.x == 0

    # like None
    cell = grid.add_gap( length=0 )
    assert isinstance(cell.item, _Gap)
    assert grid.wh.y == cell.y == 1
    assert grid.wh.x == cell.x == 1

    # None
    cell = grid.add_gap(None)
    assert isinstance(cell.item, _Gap)
    assert grid.wh.y == cell.y == 1
    assert grid.wh.x == cell.x == 2

    # fixed size
    cell = grid.add_gap(20)
    assert isinstance(cell.item, _Gap)
    assert grid.wh.y == cell.y == 1
    assert grid.wh.x == cell.x == 3

    # expand
    cell = grid.add_gap("expand")
    assert isinstance(cell.item, _Gap)
    assert grid.wh.y == cell.y == 1
    assert grid.wh.x == cell.x == 4


    # vertical - in third row
    # --------
    # like None
    cell = grid.add_gap("V")
    assert isinstance(cell.item, _Gap)
    assert grid.wh.y == cell.y == 2
    assert grid.wh.x == cell.x == 0

    # like None
    cell = grid.add_gap( direction="V", length=0 )
    assert isinstance(cell.item, _Gap)
    assert grid.wh.y == cell.y == 2
    assert grid.wh.x == cell.x == 1

    # None
    cell = grid.add_gap("V", None)
    assert isinstance(cell.item, _Gap)
    assert grid.wh.y == cell.y == 2
    assert grid.wh.x == cell.x == 2

    # fixed size
    cell = grid.add_gap("V", 20)
    assert isinstance(cell.item, _Gap)
    assert grid.wh.y == cell.y == 2
    assert grid.wh.x == cell.x == 3

    # expand
    cell = grid.add_gap("V", "expand")
    assert isinstance(cell.item, _Gap)
    assert grid.wh.y == cell.y == 2
    assert grid.wh.x == cell.x == 4


    # (3,0) add H, 2x2 span - fourth row
    cell = grid.add_gap()
    assert grid.wh.y == cell.y == 3
    assert grid.wh.x == cell.x == 0
    # (3,1) Span
    cell = grid.add_gap( y_span=2, x_span=2 )
    assert grid.wh.y == cell.y == 3
    assert grid.wh.x == cell.x == 1
    # (3,2)
    cell = grid.add_gap()
    assert grid.wh.y == cell.y == 3
    assert grid.wh.x == cell.x == 3
    # (3,3)
    cell = grid.add_gap()
    assert grid.wh.y == cell.y == 3
    assert grid.wh.x == cell.x == 4

    # (4,0) fifth row
    cell = grid.add_gap()
    assert grid.wh.y == cell.y == 4
    assert grid.wh.x == cell.x == 0
    # (4,3)
    cell = grid.add_gap()
    assert grid.wh.y == cell.y == 4
    assert grid.wh.x == cell.x == 3
    # (4,4)
    cell = grid.add_gap()
    assert grid.wh.y == cell.y == 4
    assert grid.wh.x == cell.x == 4


    # (5,0) add V, 2x2 span - sixth row
    cell = grid.add_gap("V")
    assert grid.wh.y == cell.y == 5
    assert grid.wh.x == cell.x == 0
    # (5,1)
    cell = grid.add_gap( direction="V", y_span=2, x_span=2)
    assert grid.wh.y == cell.y == 5
    assert grid.wh.x == cell.x == 1
    # (5,3)
    cell = grid.add_gap("V")
    assert grid.wh.y == cell.y == 5
    assert grid.wh.x == cell.x == 3
    # (5,4)
    cell = grid.add_gap("V")
    assert grid.wh.y == cell.y == 5
    assert grid.wh.x == cell.x == 4

    # (6,0) seventh row
    cell = grid.add_gap("V")
    assert grid.wh.y == cell.y == 6
    assert grid.wh.x == cell.x == 0
    # (6,3)
    cell = grid.add_gap("V")
    assert grid.wh.y == cell.y == 6
    assert grid.wh.x == cell.x == 3
    # (6,4)
    cell = grid.add_gap("V")
    assert grid.wh.y == cell.y == 6
    assert grid.wh.x == cell.x == 4

    # reserved spans
    # H
    assert grid.spans.has(3,1)
    assert grid.spans.has(3,2)
    assert grid.spans.has(4,1)
    assert grid.spans.has(4,2)
    # V
    assert grid.spans.has(5,1)
    assert grid.spans.has(5,2)
    assert grid.spans.has(6,1)
    assert grid.spans.has(6,2)


def test_add_empty_row(grid):
    """
    If not in first cell, fill remaining row with empty cells. </br>
    Apply a vertical gap by adding a single cell spawning the complete row.

    Examples:
    grid.add_empty_row( height=<height> ):

    grid.add_empty_row()
    grid.add_empty_row( None )
    grid.add_empty_row( 20 )
    grid.add_empty_row( "expand" )
    """
    # Preapre
    grid.set_content_columns( 4 )

    # (0,0)
    # -----
    cell = grid.add_label("default", "test")
    assert cell is grid.cells.get_cell(0, 0)
    label = cell.item
    assert isinstance(label, QLabel)

    # Add empty row, means to fill current row with gaps
    # and add spanning cell to next row.
    cell_empty_row = grid.add_empty_row()
    assert isinstance( cell_empty_row.item, _Gap )
    cell_gap1 = grid.cells.get_cell(0, 1) # implicitly added
    cell_gap2 = grid.cells.get_cell(0, 2)
    cell_gap3 = grid.cells.get_cell(0, 3)
    # test coords of implicit gaps
    assert cell_gap1.y == 0 and cell_gap1.x == 1
    assert cell_gap1.y == 0 and cell_gap2.x == 2
    assert cell_gap1.y == 0 and cell_gap3.x == 3
    # test coords of vertical expander
    assert cell_empty_row.y == 1 and cell_empty_row.x == 0

