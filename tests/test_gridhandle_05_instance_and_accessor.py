import pytest
from qtgrid.qtgrid import _WriteHead, _ColumnGaps, _Spans, _Cells

############################
# Check Qt package to import
import importlib

if importlib.util.find_spec("PyQt6") is not None:
    from PyQt6.QtWidgets import QGridLayout, QLabel
elif importlib.util.find_spec("PyQt5") is not None:
    from PyQt5.QtWidgets import QGridLayout, QLabel
elif importlib.util.find_spec("PySide6") is not None:
    from PySide6.QtWidgets import QGridLayout, QLabel
else:
    raise Exception("Cannot find package PySide6, PyQt6, or PyQt5")

def test_grid_defaults(grid):
    # Composed objects
    assert isinstance(grid.layout, QGridLayout)
    assert isinstance(grid.wh, _WriteHead)
    assert isinstance(grid.colgaps, _ColumnGaps)
    assert isinstance(grid.spans, _Spans)
    assert isinstance(grid.cells, _Cells)
    # Properties
    assert isinstance(grid.label_sources, dict)
    assert isinstance(grid.custom_lists, dict)
    assert grid.content_columns == 1
    assert grid.expand_left  is False
    assert grid.expand_right is False
    assert grid.work_up      is False
    # Default labels has been set at init time with "_set_default_label_sources"
    assert True if "default"        in grid.label_sources else False
    assert True if "default-header" in grid.label_sources else False
    assert isinstance(grid.label_sources[ "default" ], QLabel)
    assert isinstance(grid.label_sources[ "default-header" ], QLabel)


def test_setget_list(grid):
    # Set list of list names
    names = ["list1", "list2"]
    grid.set_list_names( names )

    # Get all list names as list
    NAMES = grid.get_list_names()
    assert isinstance(NAMES, list)
    for n in NAMES:
        # Are all items from 'NAMES' in 'names'
        assert True if n in names else False
        # Get curtain list named 'n'
        L = grid.get_list( n )
        assert isinstance(L, list)

def test_set_expand_left_right(grid):
    # The left expanding column influence the internal index count.
    # Due to that, the "set_expand_left" method also calls
    #   self.wh.measures()
    #   self.colgaps.measure()
    # both setting values to test here.

    # Set for the following assertions
    grid.set_content_columns( 3 )
    assert grid.content_columns == 3

    # General type tests
    assert isinstance(grid.wh.content_range, tuple)
    (a, b) = grid.wh.content_range
    assert isinstance(a, int)
    assert isinstance(b, int)
    assert isinstance(grid.wh.max_x, int)

    #########################
    # Left False, Right False
    grid.set_expand_left( False )
    grid.set_expand_right( False )
    assert grid.expand_left           == False
    assert grid.expand_right          == False
    assert grid.wh.expand_left_index  == -1
    assert grid.wh.expand_right_index == -1
    # content_range
    (a, b) = grid.wh.content_range
    assert a == 0
    assert b == 2
    # max_x
    assert grid.wh.max_x == 2

    #########################
    # Left False, Right True
    grid.set_expand_left( False )
    grid.set_expand_right( True )
    assert grid.expand_left           == False
    assert grid.expand_right          == True
    assert grid.wh.expand_left_index  == -1
    assert grid.wh.expand_right_index == 3
    # content_range
    (a, b) = grid.wh.content_range
    assert a == 0
    assert b == 2
    # max_x
    assert grid.wh.max_x == 3

    #########################
    # Left True, Right False
    grid.set_expand_left( True )
    grid.set_expand_right( False )
    assert grid.expand_left           == True
    assert grid.expand_right          == False
    assert grid.wh.expand_left_index  == 0
    assert grid.wh.expand_right_index == -1
    # content_range
    (a, b) = grid.wh.content_range
    assert a == 1
    assert b == 3
    # max_x
    assert grid.wh.max_x == 3

    #########################
    # Left True, Right True
    grid.set_expand_left( True )
    grid.set_expand_right( True )
    assert grid.expand_left           == True
    assert grid.expand_right          == True
    assert grid.wh.expand_left_index  == 0
    assert grid.wh.expand_right_index == 4
    # content_range
    (a, b) = grid.wh.content_range
    assert a == 1
    assert b == 3
    # max_x
    assert grid.wh.max_x == 4

def test_setget_content_columns(grid):
    # The left expanding column influence the internal index count.
    # Due to that, the "set_content_columns" method also calls:
    #   self.wh.measures()

    # type test
    assert isinstance(grid.content_columns, int)

    # Set 4 content columns
    grid.set_content_columns( 4 )
    assert grid.get_content_columns() == 4

    ############
    # Left False
    grid.set_expand_left( False )
    assert grid.wh.expand_left_index == -1
    # content_range
    (a, b) = grid.wh.content_range
    assert a == 0
    assert b == 3

    ###########
    # Left True
    grid.set_expand_left( True )
    assert grid.wh.expand_left_index == 0
    # content_range
    (a, b) = grid.wh.content_range
    assert a == 1
    assert b == 4

def test_set_work_up(grid):
    # default
    assert grid.work_up == False
    # False
    grid.set_work_up( False )
    assert grid.work_up == False
    # True
    grid.set_work_up( True )
    assert grid.work_up == True

def test_setget_label(grid, some_label):
    # Set
    grid.set_label_source( name_id="test_label", label=some_label )
    assert isinstance(grid.label_sources["test_label"], QLabel)
    # Get
    label = grid.get_label("test_label")
    assert isinstance(label, QLabel)

