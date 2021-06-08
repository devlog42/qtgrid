import pytest

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

# Note: Method "_set_default_label_sources" has already been tested.


def test__get_remaining_x_span(grid):
    # The left expanding column counts, but not the right one.
    grid.set_content_columns( 6 )
    grid.set_expand_left( False )
    grid.set_expand_right( False )
    assert grid._get_remaining_x_span()           == 6
    assert grid._get_remaining_x_span( from_x=0 ) == 6
    assert grid._get_remaining_x_span( from_x=2 ) == 4
    grid.set_expand_left( False )
    grid.set_expand_right( True )
    assert grid._get_remaining_x_span()           == 6
    assert grid._get_remaining_x_span( from_x=0 ) == 6
    assert grid._get_remaining_x_span( from_x=2 ) == 4
    grid.set_expand_left( True )
    grid.set_expand_right( False )
    assert grid._get_remaining_x_span()           == 7
    assert grid._get_remaining_x_span( from_x=0 ) == 7
    assert grid._get_remaining_x_span( from_x=2 ) == 5
    grid.set_expand_left( True )
    grid.set_expand_right( True )
    assert grid._get_remaining_x_span()           == 7
    assert grid._get_remaining_x_span( from_x=0 ) == 7
    assert grid._get_remaining_x_span( from_x=2 ) == 5

def test__copy_label(grid, some_label):
    some_label.setIndent( 7 )
    label = grid._copy_label( some_label )
    assert isinstance(label, QLabel)
    assert label.indent() == 7
