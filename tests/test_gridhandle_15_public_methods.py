import pytest
from qtgrid.qtgrid import _Cell, _Gap, REMIND_TO_FINISH, GREY, BLUE, CYAN, YELLOW, ORANGE, MAGENTA

############################
# Check Qt package to import
import importlib

if importlib.util.find_spec("PyQt6") is not None:
    from PyQt6.QtWidgets import QLabel
    from PyQt6.QtGui     import QPalette, QColor
elif importlib.util.find_spec("PyQt5") is not None:
    from PyQt5.QtWidgets import QLabel
    from PyQt5.QtGui     import QPalette, QColor
elif importlib.util.find_spec("PySide6") is not None:
    from PySide6.QtWidgets import QLabel
    from PySide6.QtGui     import QPalette, QColor
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

def test_finish(grid):
    """
    Always call the finish method after cells are added.

    Apply from all `_Cell` objects their holding *QWidget* objects to the resulting *QGridLayout*.
    Also add the expander and gaps and mark unused cells in **work_up** mode.
    """
    qgrey    = QColor( GREY[0], GREY[1], GREY[2] )
    qblue    = QColor( BLUE[0], BLUE[1], BLUE[2] )
    qcyan    = QColor( CYAN[0], CYAN[1], CYAN[2] )
    qyellow  = QColor( YELLOW[0], YELLOW[1], YELLOW[2] )
    qorange  = QColor( ORANGE[0], ORANGE[1], ORANGE[2] )
    qmagenta = QColor( MAGENTA[0], MAGENTA[1], MAGENTA[2] )

    # Set Options
    grid.set_expand_left( False )
    grid.set_expand_right( False )
    grid.set_content_columns( 3 )
    grid.set_work_up( True )

    # If finish was not called, a reminder message (label) must appear at item index 0.
    # This is independent of whether the left or right expander is used, because they
    # are only included after the reminder has been removed.
    item = grid.layout.itemAt(0)
    assert item is not None
    lbl = item.widget()
    assert ( lbl is not None
             and isinstance(lbl, QLabel)
             and lbl.text() == REMIND_TO_FINISH )

    # Add label and finish
    grid.add_label("default", "one")
    grid.finish()

    # The reminder is gone
    item = grid.layout.itemAt(0)
    assert item is not None
    lbl = item.widget()
    assert ( lbl is not None
             and isinstance(lbl, QLabel)
             and lbl.text() == "one" )

    # Clear and change settings
    grid.clear()

    ##########
    # Settings
    grid.set_content_columns( 7 )
    grid.set_expand_left( True )
    grid.set_expand_right( True )
    grid.set_work_up( True )
    grid.set_column_gaps([
        (2, 20),  # (column_index, width)
    ])

    ############
    # Add Wdgets
    # The QGridLayout item indices are different from displayed ones.

    #######
    # (0,0) Blue Left Expander
    grid.add_label("default", "One")    # (0,1) Label One
    grid.add_gap()                      # (0,2) Grey
    grid.add_gap(20)                    # (0,3) Yellow Gap
    # (0,4) Yellow Column Gap (see settings above)
    grid.add_gap("expand")              # (0,5) Blue horiz. expander
    grid.add_empty_row()                # (0,6) Grey / Fill remaining cells explicitly empty
    # (0,7) Grey
    # (0,8) Blue Right Expander

    #######
    # (1,0) Blue Left Expander
    # (1,1) Grey empty row (with column span)
    # (1,8) Blue Right Expander

    #######
    # (2,0) Blue Left Expander
    grid.add_empty_row(20)  # (2,1) Orange empty row (with column span)
    # (2,8) Blue Right Expander

    #######
    # (3,0) Blue Left Expander
    grid.add_empty_row("expand")    # (3,1) Cyan empty row (with column span)
    # (3,8) Blue Right Expander

    #######
    # (4,0) Blue Left Expander
    grid.add_label("default", "Two")    # (4,1) Label Two
    # (4,2) Magenta unused cell
    # (4,3) Yellow Column Gap
    # (4,4) Magenta
    # (4,5) Magenta
    # (4,6) Magenta
    # (4,7) Magenta
    # (4,8) Blue Right Expander

    ########
    # Finish
    grid.finish()

    # Each item is a label
    for y in (0, 4):
        for x in range(9):
            item = grid.layout.itemAtPosition(y, x)
            assert item is not None
            assert isinstance(item.widget(), QLabel)
    for y in (1, 2, 3):
        # The empty rows
        for x in range(3):
            item = grid.layout.itemAtPosition(y, x)
            assert item is not None
            assert isinstance(item.widget(), QLabel)

    # ROW 0
    # (0,0) Blue Left Expander
    assert qblue   == grid.layout.itemAtPosition(0, 0).widget().palette().color( QPalette.ColorRole.Window )
    # (0,1) Label One
    assert "One"   == grid.layout.itemAtPosition(0, 1).widget().text()
    # (0,2) Grey
    assert qgrey   == grid.layout.itemAtPosition(0, 2).widget().palette().color( QPalette.ColorRole.Window )
    # (0,3) Yellow Gap
    assert qyellow == grid.layout.itemAtPosition(0, 3).widget().palette().color( QPalette.ColorRole.Window )
    # (0,4) Yellow Column Gap
    assert qyellow == grid.layout.itemAtPosition(0, 4).widget().palette().color( QPalette.ColorRole.Window )
    # (0,5) Blue horiz. expander
    assert qblue   == grid.layout.itemAtPosition(0, 5).widget().palette().color( QPalette.ColorRole.Window )
    # (0,6) Grey / Fill remaining cell explicitly empty
    assert qgrey   == grid.layout.itemAtPosition(0, 6).widget().palette().color( QPalette.ColorRole.Window )
    # (0,7) Grey
    assert qgrey   == grid.layout.itemAtPosition(0, 7).widget().palette().color( QPalette.ColorRole.Window )
    # (0,8) Blue Right Expander
    assert qblue   == grid.layout.itemAtPosition(0, 8).widget().palette().color( QPalette.ColorRole.Window )

    # ROW 1
    # (1,0) Blue Left Expander
    assert qblue == grid.layout.itemAtPosition(1, 0).widget().palette().color( QPalette.ColorRole.Window )
    # (1,1) Grey empty row (with column span)
    assert qgrey == grid.layout.itemAtPosition(1, 1).widget().palette().color( QPalette.ColorRole.Window )
    # (1,2) Blue Right Expander
    assert qblue == grid.layout.itemAtPosition(1, 8).widget().palette().color( QPalette.ColorRole.Window )

    # ROW 2
    # (2,0) Blue Left Expander
    assert qblue   == grid.layout.itemAtPosition(2, 0).widget().palette().color( QPalette.ColorRole.Window )
    # (2,1) Orange empty row (with column span)
    assert qorange == grid.layout.itemAtPosition(2, 1).widget().palette().color( QPalette.ColorRole.Window )
    # (2,2) Blue Right Expander
    assert qblue   == grid.layout.itemAtPosition(2, 8).widget().palette().color( QPalette.ColorRole.Window )

    # ROW 3
    # (3,0) Blue Left Expander
    assert qblue == grid.layout.itemAtPosition(3, 0).widget().palette().color( QPalette.ColorRole.Window )
    # (3,1) Cyan empty row (with column span)
    assert qcyan == grid.layout.itemAtPosition(3, 1).widget().palette().color( QPalette.ColorRole.Window )
    # (3,2) Blue Right Expander
    assert qblue == grid.layout.itemAtPosition(3, 8).widget().palette().color( QPalette.ColorRole.Window )

    # ROW 4
    # (4,0) Blue Left Expander
    assert qblue    == grid.layout.itemAtPosition(4, 0).widget().palette().color( QPalette.ColorRole.Window )
    # (4,1) Label Two
    assert "Two"    == grid.layout.itemAtPosition(4, 1).widget().text()
    # (4,2) Magenta unused cell
    assert qmagenta == grid.layout.itemAtPosition(4, 2).widget().palette().color( QPalette.ColorRole.Window )
    # (4,3) Yellow Column Gap
    assert qyellow  == grid.layout.itemAtPosition(4, 3).widget().palette().color( QPalette.ColorRole.Window )
    # (4,4) Magenta
    assert qmagenta == grid.layout.itemAtPosition(4, 4).widget().palette().color( QPalette.ColorRole.Window )
    # (4,5) Magenta
    assert qmagenta == grid.layout.itemAtPosition(4, 5).widget().palette().color( QPalette.ColorRole.Window )
    # (4,6) Magenta
    assert qmagenta == grid.layout.itemAtPosition(4, 6).widget().palette().color( QPalette.ColorRole.Window )
    # (4,7) Magenta
    assert qmagenta == grid.layout.itemAtPosition(4, 7).widget().palette().color( QPalette.ColorRole.Window )
    # (4,8) Blue Right Expander
    assert qblue    == grid.layout.itemAtPosition(4, 8).widget().palette().color( QPalette.ColorRole.Window )


