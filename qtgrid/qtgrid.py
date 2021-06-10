# -*- coding: utf-8 -*-

"""
Make working with *QGridLayout* easier

| The interface class for this module is `Grid`.
| In this moduele, there are a number of 3-tuples defining some colors.
"""

############################
# Check Qt package to import
import importlib

if importlib.util.find_spec("PyQt6") is not None:
    from PyQt6.QtCore    import Qt, QObject
    from PyQt6.QtWidgets import QLabel, QLayout, QGridLayout, QSpacerItem, QWidget, QSizePolicy
    from PyQt6.QtGui     import QPalette, QBrush, QColor, QFont
elif importlib.util.find_spec("PyQt5") is not None:
    from PyQt5.QtCore    import Qt, QObject
    from PyQt5.QtWidgets import QLabel, QLayout, QGridLayout, QSpacerItem, QWidget, QSizePolicy
    from PyQt5.QtGui     import QPalette, QBrush, QColor, QFont
elif importlib.util.find_spec("PySide6") is not None:
    from PySide6.QtCore    import Qt, QObject
    from PySide6.QtWidgets import QLabel, QLayout, QGridLayout, QSpacerItem, QWidget, QSizePolicy
    from PySide6.QtGui     import QPalette, QBrush, QColor, QFont
else:
    raise Exception("Cannot find package PySide6, PyQt6, or PyQt5")

###############
# Global colors
#   in work-up mode and for default labels
GREY      = (180, 180, 180)
"""RGB-tuple for explicit empty cells"""
BLUE      = (0,   0,   180)
"""RGB-tuple for horizontal expander"""
CYAN      = (0,   180, 180)
"""RGB-tuple for vertical expander"""
YELLOW    = (190, 190, 0)
"""RGB-tuple for horizontal fixed size gaps"""
ORANGE    = (180, 140, 0)
"""RGB-tuple for vertical fixed size gaps"""
MAGENTA   = (180, 0,   180)
"""RGB-tuple for unused cells"""
HEADER_BG = (190, 190, 190)
"""RGB-tuple for headers default background color"""

# Text for reminder
REMIND_TO_FINISH = "Method 'finish' not used"

class Grid(QObject):
    """
    Interface class for this *qtgrid* module
    """
    def __init__(self,
                 # Instantiation options
                 layout      = None,  content_columns = 1,
                 expand_left = False, expand_right    = False,
                 work_up     = False, column_gaps     = [],
                 list_names  = []
                 ) -> None:
        """
        Examples

        .. python::
            grid = Grid()

            grid = Grid(
                layout          = QGridLayout(),
                content_columns = 5,
                expand_left     = False,
                expand_right    = True,
                work_up         = True,

                column_gaps = [ (1, 20), (3, None) ],

                list_names = ["list1", "list2"],
            )

        :param layout:          None (default) or QGridLayout object
        :param content_columns: Max int number of content columns, default 1
        :param expand_left:     boolean, default False
        :param expand_right:    boolean, default False
        :param work_up:         boolean, default False
        :param column_gaps:     list of tuples, default [ ]
        :param list_names:      list of string names pointing to lists, default [ ]
        """
        super(Grid, self).__init__()
        # to be composed
        self.layout  = None
        """Composed QGridLayout object. Will be cleared"""
        self.wh      = None
        """Composed `_WriteHead` object"""
        self.colgaps = None
        """Composed `_ColumnGaps` object"""
        self.spans   = None
        """Composed `_Spans` object"""
        self.cells   = None
        """Composed `_Cells` object"""
        #####
        self.expand_left = False
        """Boolean. If True, a far left column with expanders are applied"""
        self.expand_right = False
        """Boolean. If True, a far right column with expanders are applied"""
        self.content_columns = 1
        """Integer >= 1. Max number of content columns"""
        self.work_up = False
        """Boolean. If True, visual help is applied"""
        self.label_sources = {}
        """Dictionary = { "name_id1": qlabel1, "name_id2": qlabel2, ... }"""
        self.custom_lists = {}
        """Dictionary = { "list_name1": [ ], "list_name2": [ ], ... }"""

        # Compose
        if layout is None:
            layout = QGridLayout()
        if not isinstance(layout, QGridLayout):
            raise Exception("Arg 'layout' must be QGridLayout object")
        self.layout  = layout             # QGridLayout
        self.wh      = _WriteHead(self)   # WriteHead
        self.colgaps = _ColumnGaps(self)  # ColumnGaps
        self.spans   = _Spans(self)       # Spans
        self.cells   = _Cells(self)       # Cells

        # Clear layout
        # This also adds the remainder label with text of global var: REMIND_TO_FINISH
        self.clear()
        # Prepare internal lists
        self.set_list_names( list_names )
        # Expanding far left or right columns
        self.set_expand_left( expand_left )
        self.set_expand_right( expand_right )
        # Set work-up mode
        self.set_work_up( work_up )
        # Max number of content columns and columns gaps
        self.set_content_columns( content_columns )
        self.set_column_gaps( column_gaps )
        # Label sources
        self._set_default_label_sources()
        # WriteHead measures
        self.wh.measures()
        # ColumnGaps measure
        self.colgaps.measure()

    ######################
    # Public set Accessors
    def set_list_names(self, names=[]) -> None:
        """
        Prepare internal lists with given names

        .. python::
            grid.set_list_names("list1", "list2")
            grid.set_list_names()

        | Can only be used before any widget is added or after calling the `clear` method.
        | The internal lists are intended to hold users widgets for later disposal.
        | Add widgets to the lists with `add`, or `add_label` methods.
        | After all, use the `get_list_names`, or `get_list` methods to access the lists in turn.
        | If called without argument, all internal lists will be removed.

        :param names: list of strings, default [ ]
        """
        if self.wh.x != 0 or self.wh.y != 0:
            raise Exception("Cannot set custom list names after adding widgets")
        if not isinstance(names, list):
            raise Exception("Arg 'names' must be a list")
        #####
        self.custom_lists = {}
        for name in names:
            if not isinstance(name, str):
                raise Exception("Elements in 'names' must be strings")
            self.custom_lists[ name ] = []

    def set_expand_left(self, flag=False) -> None:
        """
        Set whether or not to add a far left expanding column, influencing the grid alignment

        Can only be used before any widget is added or after calling the `clear` method.

        :param flag: boolean, default False
        """
        if self.wh.x != 0 or self.wh.y != 0:
            raise Exception("Cannot set 'expand_left' after adding widgets")
        self.expand_left = True if flag else False
        self.wh.measures()
        self.colgaps.measure()

    def set_expand_right(self, flag=False) -> None:
        """
        Set whether or not to add a far right expanding column, influencing the grid alignment

        Can only be used before any widget is added or after calling the `clear` method.

        :param flag: boolean, default False
        """
        if self.wh.x != 0 or self.wh.y != 0:
            raise Exception("Cannot set 'expand_right' after adding widgets")
        self.expand_right = True if flag else False
        self.wh.measures()

    def set_content_columns(self, content_columns=1) -> None:
        """
        Set maximum number of content columns

        .. python::
            grid.set_content_columns( content_columns=1 )
            grid.set_content_columns( 1 )

        | Can only be used before any widget is added or after calling the `clear` method.
        | The possibly far left or right expanding columns are not considered.
        | See also the `set_column_gaps` method.

        :param content_columns: int n with n >= 1 and n > number of `_ColumnGaps.count`, default 1
        """
        if self.wh.x != 0 or self.wh.y != 0:
            raise Exception("Cannot set 'content_columns' after adding widgets")
        if not isinstance(content_columns, int) or content_columns < 1:
            raise Exception("Arg 'content_columns' must be integer >= 1")
        if self.colgaps.count() >= content_columns:
            raise Exception("Arg 'content_columns' must be greater than the number of 'columns_gaps'")
        #####
        self.content_columns = content_columns
        self.wh.measures()

    def set_column_gaps(self, column_gaps=[]) -> None:
        """
        Interface method to `_ColumnGaps.set`
        """
        self.colgaps.set( column_gaps )

    def set_work_up(self, flag=False) -> None:
        """
        Set whether or not to activate the work-up mode

        Can only be used before any widget is added or after calling the `clear` method.

        In work up mode otherwise invisible cells are colored indicating the following meaning:

        - **Magenta** : unused cell
        - **Blue**    : horizontal expander
        - **Cyan**    : vertical expander
        - **Yellow**  : fixed sized horizontal gap
        - **Orange**  : fixed sized vertical gap
        - **Grey**    : explicit empty cell

        :param flag: boolean, default False
        """
        if self.wh.x != 0 or self.wh.y != 0:
            raise Exception("Cannot set 'work_up' after adding widgets")
        self.work_up = True if flag else False

    def set_label_source(self, name_id=None, label=None) -> None:
        """
        Store a given QLabel object as a copy source

        .. python::
            grid.set_label_source( name_id="foo", label=myLabel )
            grid.set_label_source("foo", myLabel)

        The *name_id* is the key to access the label with the `add_label`, or `get_label` methods.

        :param name_id: required str name for the label
        :param label:   required QLabel object to store
        """
        # Checks
        if not isinstance(name_id, str) or not len(name_id):
            raise Exception("Required arg 'name_id' must be string")
        if not isinstance(label, QLabel):
            raise Exception("Required arg 'label' must be QLabel object")
        # Set
        self.label_sources[ name_id ] = label

    ######################
    # Public get Accessors
    def get_list(self, name=None) -> list:
        """
        Get *name* list of widgets as it was prepared with `set_list_names`

        The returned list contains QWidgets object added with the `add` or `add_label` methods.

        .. python::
            for widget in grid.get_list("list1"):
                pass

        :param name: required str name of an internal list

        :return: list of widgets
        """
        if not isinstance(name, str):
            raise Exception("Arg 'name' must be string")
        if name not in self.custom_lists:
            raise Exception(f"List '{ name }' not found")
        return self.custom_lists[ name ]

    def get_list_names(self) -> list:
        """
        Get all custom list names as they were prepared with `set_list_names`

        .. python::
            names = grid.get_list_names()
            for name in names:
                for widget in grid.get_list( name ):
                    pass

        :return: list of list names
        """
        return list( self.custom_lists.keys() )

    def get_content_columns(self) -> int:
        """
        Get max number of content columns

        :return: int
        """
        return self.content_columns

    def get_label(self, name_id=None) -> object:
        """
        Get stored QLabel object by *name_id*

        Labels are stored with `set_label_source`.

        :param name_id: required str id for a stored label
        :return: QLabel object
        """
        if not isinstance(name_id, str):
            raise Exception("Arg 'name_id' must be string")
        if name_id not in self.label_sources:
            raise Exception(f"Label with id '{name_id}' not found")
        return self.label_sources[ name_id ]

    ################
    # Public methods
    def add(self, widget=None, y_span=1, x_span=1, to_list=None) -> object:
        """
        Add a *widget* to the current `_WriteHead` position into the grid

        .. python::
            cell = grid.add( widget=WIDGET, y_span=1, x_span=1, to_list="list_name" )
            cell = grid.add( WIDGET, y_span=2, x_span=2 )
            cell = grid.add( WIDGET, x_span="all" )
            cell = grid.add( WIDGET )

        | The *to_list* argument can be used to not only add the widget to the grid, but also to
        | a prepared internal list for later use. See also the `set_list_names` method.
        |
        | The *y_span* and *x_span* integer arguments spans the cell over the given number of rows
        | and columns. If *x_span* value is **"all"** the cell spans over the remaining row.

        :param widget:  required QWidget object to be added
        :param y_span:  int >= 1, default 1
        :param x_span:  int >= 1, or string "all", default 1
        :param to_list: optional str name of an internal list

        :return: `_Cell` object with *QWidget* object
        """
        # Arguments
        if widget is None:
            raise Exception("missing widget")
        if not (isinstance(y_span, int) and y_span >= 1):
            raise Exception("Arg 'y_span' must be integer >= 1")
        if ( not (isinstance(x_span, int) and x_span >= 1)
             and not (isinstance(x_span, str) and x_span.upper() == "ALL") ):
            raise Exception("Arg 'x_span' must be integer >= 1 or string 'all'")
        if to_list is not None:
            if not isinstance(to_list, str):
                raise Exception("Arg 'to_list' must be string")
            if to_list not in self.custom_lists:
                raise Exception(f"list '{to_list}' does not exist")
        # Calibrate write head
        self.wh.gage()
        # Get current position
        y = self.wh.y
        x = self.wh.x
        # Check x_span
        max_span = self._get_remaining_x_span()
        if isinstance(x_span, str) and x_span.upper() == "ALL":
            x_span = max_span
        else:
            if x_span > max_span:
                x_span = max_span
        # Add to grid cells
        cell = _Cell( widget, y, x, y_span, x_span )
        self.cells.add( cell )
        # Reserve span
        if y_span > 1 or x_span > 1:
            self.spans.reserve( y, x, y_span, x_span )
        # Add to custom list ?
        if to_list is not None:
            self.custom_lists[ to_list ].append( widget )
        # Return
        return cell

    def add_gap(self, direction=None, length=None, y_span=1, x_span=1) -> object:
        """
        Add a `_Cell` object with a `_Gap` object to the `_WriteHead` position into the grid

        .. python::
            cell = add_gap(direction="H", length="20", y_span=2, x_span=2)
            # horizontal direction
            cell = add_gap("H")           # same as None
            cell = add_gap("H", 0)        # same as None
            cell = add_gap("H", None)     # explicitly empty
            cell = add_gap("H", 20)
            cell = add_gap("H", "expand")

            # horizontal direction is default
            cell = add_gap()         # same as None
            cell = add_gap(0)        # same as None
            cell = add_gap(None)     # explicitly empty
            cell = add_gap(20)
            cell = add_gap("expand")

            # vertical direction
            cell = add_gap("V")           # same as None
            cell = add_gap("V", 0)        # same as None
            cell = add_gap("V", None)     # explicitly empty
            cell = add_gap("V", 20)
            cell = add_gap("V", "expand")

        See the `set_work_up` method for a list of displayed colors in **work_up** mode.

        :param direction: None, "H" (default) , "V", "horizontal", or "vertical"
        :param length:    None, int >= 0, or "expand", default None
        :param y_span:    int >= 1, default 1
        :param x_span:    int >= 1, default 1

        :return: `_Cell` object with a `_Gap` object
        """
        # Arg 'direction': None, int, H, HORIZONTAL, V, VERTICAL, EXPAND
        err = "Arg 'direction' must be None, integer, H, horizontal, V, vertical, or expand"
        if direction is None:
            direction = "H"
            length    = 0
        if isinstance(direction, int):
            length    = direction
            direction = "H"
        if ( not isinstance(direction, str)
             or direction.upper() not in ["H", "HORIZONTAL", "V", "VERTICAL", "EXPAND"] ):
            raise Exception( err )
        else:
            D = direction.upper()
            if D in ["H", "HORIZONTAL"]:
                direction = "H"
            elif D in ["V", "VERTICAL"]:
                direction = "V"
            elif D == "EXPAND":
                length    = D
                direction = "H"
            else:
                direction = D
        if direction not in ["H", "V"]:
            raise Exception("Unknown arg 'direction' value:", direction)

        # Arg 'length': None, int >= 0, EXPAND
        err = "Arg 'length' must be None, integer >= 0, or string 'expand'"
        if length is None:
            length = 0
        if not (isinstance(length, str) or isinstance(length, int)):
            raise Exception( err )
        if isinstance(length, int) and length < 0:
            raise Exception( err )
        if isinstance(length, str) and not length.upper() == "EXPAND":
            raise Exception( err )

        # Arg 'y_span': int >= 1
        if not isinstance(y_span, int) or not y_span >= 1:
            raise Exception("Arg 'y_span' must be integer >= 1")

        # Arg 'x_span': int >= 1, ALL
        err = "Arg 'x_span' must be integer >= 1, or 'all'"
        max_span = self._get_remaining_x_span()
        if isinstance(x_span, str) and x_span.upper() == "ALL":
            x_span = max_span
        if not (isinstance(x_span, int) and x_span >= 1):
            raise Exception( err )
        if x_span > max_span:
            x_span = max_span

        # Calibrate write head
        self.wh.gage()
        # Get current position
        y = self.wh.y
        x = self.wh.x
        # Add to grid cells
        gap  = _Gap( self, direction, length )
        cell = _Cell( gap, y, x, y_span, x_span )
        self.cells.add( cell )
        # Reserve span
        if y_span > 1 or x_span > 1:
            self.spans.reserve( y, x, y_span, x_span )
        # Return
        return cell

    def add_empty_row(self, height=None) -> object:
        """
        Add a row gap

        .. python::
            cell = grid.add_empty_row()     # same as None
            cell = grid.add_empty_row(0)    # same as None
            cell = grid.add_empty_row(None) # explicitly empty
            cell = grid.add_empty_row(20)
            cell = grid.add_empty_row("expand")

        | If not in first column: fill the remaining row with explicit empty cells (colored grey), then …
        | In the first column of a row: apply vertical gap by adding a single cell spawning the complete row.
        |
        | The first three calls are all equivalent.
        | When given a integer number, the row gets a fixed height in pixels.
        | If the string “expand” is used, the row expands in vertical direction.
        | See the `set_work_up` method for a list of displayed colors in **work_up** mode.

        :param height: None (default), int >= 0, or "expand"

        :return: `_Cell` object with `_Gap` object
        """
        # Arg 'height': None, int >= 0, or "expand"
        if ( height is not None
             and not (isinstance(height, int) and height >= 0)
             and not (isinstance(height, str) and height.upper() == "EXPAND") ):
            raise Exception("Arg 'height' must be None, int >= 0, or string 'expand'")
        (left_edge, right_edge) = self.wh.content_range
        # Calibrate write head
        self.wh.gage()
        # Get current position
        y = self.wh.y
        x = self.wh.x
        # Fill remaining row cells
        while x != left_edge:
            gap = _Gap( self )
            self.cells.add(
                _Cell( gap, y, x )
            )
            self.wh.gage()
            y = self.wh.y
            x = self.wh.x
        # Apply vertical row gap
        span = self._get_remaining_x_span()
        gap  = _Gap( self, "V", height )
        cell = _Cell( gap, y, x, x_span=span )
        self.cells.add( cell )
        # Reserve span
        if span > 1:
            self.spans.reserve( y, x, 1, span )
        # Return
        return cell

    def add_label(self, name_id=None, text="", y_span=1, x_span=1, to_list=None) -> object:
        """
        Add a `_Cell` object with a *QLabel* object at `_WriteHead` position into the grid

        | The *name_id* argument references to a label preset.
        | If *x_span* value is "all", the added label spans over the remaining row.
        | See also the `set_label_source` method.

        .. python::
            cell = grid.add_label( name_id="foo", text="lorem ipsum", y_span=2, x_span=2, to_list="list1" )
            cell = grid.add_label("foo", "lorem ipsum", y_span=2, x_span=2, to_list="list1")
            cell = grid.add_label("foo", "lorem ipsum", x_span="all")
            cell = grid.add_label("foo", "lorem ipsum")

        There are predefined defaults:

        .. python::
            cell = grid.add_label("default", "lorem ipsum")
            cell = grid.add_label("default-header", "Some Header")

        | For your disposla, you may also add the label to an internal list with the *to_list*
        | argument, or use the `get_label` method.

        | In most cases the user don't need the returned `_Cell` object, since the added label
        | can also be added to an internal list with the *to_list* argument. But you may also
        | access the new label directly:

        .. python::
            cell  = grid.add_label("default", "lorem ipsum")
            label = cell.item

        :param name_id: required string
        :param text:    required string
        :param y_span:  int >= 1, default 1
        :param x_span:  int >= 1, or string "all", default 1
        :param to_list: optional str name of an internal list

        :return: `_Cell` object with *QLabel* object
        """
        if not isinstance(name_id, str) or not len(name_id):
            raise Exception("Required arg 'name_id' must be string")
        if not isinstance(text, str):
            raise Exception("Required arg 'text' must be string")
        #####
        lbl     = self.get_label( name_id )
        mylabel = self._copy_label( lbl )
        mylabel.setText( text )
        return self.add( mylabel, y_span=y_span, x_span=x_span, to_list=to_list )

    def clear(self, _layout=None) -> None:
        """
        Delete all `_Cell` objects and corresponding items in *QGridLayout* recursively

        .. python::
            grid.clear()

        | The *_layout* argument is used for the recursive call only.
        | The `_WriteHead` coordinates are reset.
        | All `custom_lists` and the private list `_Spans._list` are reset.

        :param _layout: None or QGridLayout object
        """
        if _layout is None:
            _layout = self.layout
        # Clear grid items
        item = _layout.takeAt(0)
        while item is not None:
            wgt = item.widget()
            if wgt is not None:
                wgt.deleteLater()
            lyt = item.layout()
            if lyt is not None:
                self.clear( lyt )
            item = _layout.takeAt(0)

        # Reset WriteHead coordinates
        self.wh.y = 0
        self.wh.x = 0
        # Clear custom lists
        for name in self.custom_lists:
            self.custom_lists[ name ] = []
        # Clear spans
        self.spans = _Spans(self)
        # Clear cells
        self.cells = _Cells(self)
        # Add reminder label.
        # This will only be removed in finish method.
        self.layout.addWidget( QLabel( REMIND_TO_FINISH ) )

    def finish(self) -> None:
        """
        Always call this after you added all your cells

        | Apply from all `_Cell` objects their holding *QWidget* objects to the resulting *QGridLayout*.
        | Also add the expander and gaps and mark unused cells in **work_up** mode.
        """

        # Remove reminder label
        item = self.layout.itemAt(0)
        if item is not None:
            lbl = item.widget()
            if ( lbl is not None
                 and isinstance(lbl, QLabel)
                 and lbl.text() == REMIND_TO_FINISH ):
                self.layout.takeAt(0)
                lbl.deleteLater()

        max_y = self.cells.get_current_max_y()

        # 1. Apply far left or right expander
        for y in range( max_y + 1 ):
            # Left
            if self.expand_left:
                gap = _Gap( self, "H", "expand", index=None )
                self.cells.add(
                    _Cell( gap, y, 0 )
                )
            # Right
            if self.expand_right:
                gap = _Gap( self, "H", "expand", index=None )
                self.cells.add(
                    _Cell( gap, y, self.wh.expand_right_index )
                )

        # 2. Add column gaps
        self.colgaps.add_to_cells()

        # 3. Apply user added cells
        self.cells.apply_to_layout()

        # 4. Mark unused cells
        if self.work_up:
            (left_edge, right_edge) = self.wh.content_range
            for y in range( max_y + 1 ):
                for x in range( left_edge, right_edge + 1 ):
                    if not self.cells.has_taken( y, x ):
                        idx = x-1 if self.expand_left else x
                        gap = _Gap( self, "H", "unused", index=idx)
                        self.layout.addWidget( gap.item, y, x )

    #################
    # Private methods
    def _set_default_label_sources(self) -> None:
        """
        Set label sources for "default" and "default-header"

        After calling this method at init time the user can do :

        .. python::
            grid.add_label("default", "my text")
            grid.add_label("default-header", "Some Header")

        """
        ####################
        # Add default header
        lbl = QLabel()
        # margin
        lbl.setMargin( 5 )
        # Background color
        palette = QPalette()
        (r, g, b) = HEADER_BG
        brush     = QBrush( QColor( r, g, b ) )
        brush.setStyle( Qt.BrushStyle.SolidPattern )
        palette.setBrush( QPalette.ColorRole.Window, brush )
        lbl.setAutoFillBackground(True)
        lbl.setPalette( palette )
        # Font
        font = QFont()
        font.setFamily("Sans")
        font.setBold(True)
        font.setPointSize( 10 )
        lbl.setFont( font )
        #####
        self.set_label_source( name_id="default-header", label=lbl )
        ###################
        # Add default label
        lbl = QLabel()
        lbl.setIndent( 5 )
        self.set_label_source( name_id="default", label=lbl )

    def _get_remaining_x_span(self, from_x=None) -> int:
        """
        Get the number of remaining cells in row

        | If *from_x* is None, the current **x** value from `_WriteHead` is taken.
        | The return value is the range *from_x* to the end of all content columns.
        | It is appropiate for layout *span* values counting from 1.

        :param from_x: None (default), or int >= 0
        :return: int >= 0
        """
        (left_edge, right_edge) = self.wh.content_range
        if from_x is None:
            from_x = self.wh.x
        return (1 + right_edge - from_x)

    def _copy_label(self, label) -> object:
        """
        Get a copy of a given *label*

        .. python::
            label2 = grid._copy_label( label1 )

        :param label: required QLabel object
        :return: QLabel object
        """
        lbl = QLabel()
        lbl.setAlignment( label.alignment() )
        lbl.setIndent( label.indent() )
        lbl.setMargin( label.margin() )
        lbl.setOpenExternalLinks( label.openExternalLinks() )
        p = label.pixmap()
        if p:
            lbl.setPixmap( p )
        lbl.setScaledContents( label.hasScaledContents() )
        lbl.setTextFormat( label.textFormat() )
        lbl.setTextInteractionFlags( label.textInteractionFlags() )
        lbl.setWordWrap( label.wordWrap() )
        lbl.setFont( label.font() )

        lbl.setBaseSize( label.baseSize() )
        lbl.setCursor( label.cursor() )
        lbl.setGeometry( label.geometry() )
        lbl.resize( label.height(), label.width() )
        lbl.setLocale( label.locale() )

        lbl.setMaximumHeight( label.maximumHeight() )
        lbl.setMaximumWidth( label.maximumWidth() )
        lbl.setMaximumSize( label.maximumSize() )

        lbl.setMinimumHeight( label.minimumHeight() )
        lbl.setMinimumWidth( label.minimumWidth() )
        lbl.setMinimumSize( label.minimumSize() )

        lbl.setAutoFillBackground( label.autoFillBackground() )
        lbl.setPalette( label.palette() )

        lbl.setSizePolicy( label.sizePolicy() )
        lbl.setStyleSheet( label.styleSheet() )

        lbl.setStatusTip( label.statusTip() )
        lbl.setToolTip( label.toolTip() )
        lbl.setToolTipDuration( label.toolTipDuration() )
        lbl.setWhatsThis( label.whatsThis() )
        return lbl


class _WriteHead():
    """
    The *_WriteHead* keeps track of internal indices counting in 2 dimensions

    - Composed to `Grid.wh` property.
    - The *_WriteHead* property **max_x** value is determined at instantiation time.
    - When calling the `gage` method, the write head is skiped to the next free cell,
      which might be in the next row.
    """
    def __init__(self, grid=None) -> None:
        """
        Example

        .. python::
            grid.wh = _WriteHead()
            grid.wh.measures()
            grid.wh.gage()
            if grid.wh.is_in_content_range(2) : pass

        :param grid: required Grid object
        """
        if not isinstance(grid, Grid):
            raise Exception("Arg 'grid' must be Grid object")
        self.grid = grid
        """Grid object"""
        self.y = 0
        """int y coordinate, init 0"""
        self.x = 0
        """int x coordinate, init 0"""
        self.max_x = 0
        """Max x-index number including far left or right expansions"""
        self.expand_left_index  = -1
        """Index of left expander, -1 if unset"""
        self.expand_right_index = -1
        """Index of right expander, -1 if unset"""
        self.content_range = (0, 0)
        """2-Tuple with left most and right most column indices wrapping the content"""

    def measures(self) -> None:
        """
        Determine the current values for **expand_left_index**, **expand_right_index**,
        **content_range**, and **max_x**
        """
        grid = self.grid
        # expand_left_index
        self.expand_left_index = 0 if grid.expand_left else -1
        # content_range
        left_edge  = 0
        right_edge = 0
        if grid.expand_left:
            left_edge  += 1
            right_edge += 1
        right_edge += (grid.content_columns - 1)
        self.content_range = (left_edge, right_edge)
        # expand_right_index
        if grid.expand_right:
            self.expand_right_index = right_edge + 1
        else:
            self.expand_right_index = -1
        # max_x
        self.max_x = right_edge + 1 if grid.expand_right else right_edge

    def is_in_content_range(self, i=None) -> bool:
        """
        Is a given index number within the content range ?

        :param i: required int index number
        :return: boolean
        """
        if not isinstance(i, int):
            raise Exception("Arg 'i' must be integer")
        (a, b) = self.content_range
        return True if (i >= a and i <= b) else False

    def gage(self) -> None:
        """
        Skip to the next free cell and set the **y** and **x** properties

        | Skip to next cell if the current cell is occupied, or is an expander, or gap, or part of a span.
        | This is called recursively and sets the **y** and **x** properties.
        """
        grid = self.grid
        (dummy, right_edge) = self.content_range
        # print("wh.y, wh.x :",self.y, self.x)
        # print("wh.max_x   :",self.max_x)

        # Expand left ?
        if self.x == self.expand_left_index:
            self.x += 1
            self.gage()
        # Cell is occupied ?
        elif grid.cells.has_taken( self.y, self.x ):
            self.x += 1
            self.gage()
        # Cell is reserved for a span ?
        elif grid.spans.has( self.y, self.x ):
            self.x += 1
            self.gage()
        # Column gap ?
        elif grid.colgaps.has_column( self.x ):
            self.x += 1
            self.gage()
        # Next row ?
        elif self.x > right_edge:
            self.y += 1
            self.x  = 0
            self.gage()


class _ColumnGaps():
    """
    Serve `_Gap`'s for complete columns

    - Composed to `Grid.colgaps` property.
    - The column gaps are represented as a list of 2-tuples of the form: *(column_index, width)*

    """
    def __init__(self, grid=None) -> None:
        """
        Example

        .. python::
            grid.colgaps = _ColumnGaps( grid )

        :param grid: required Grid object
        """
        if not isinstance(grid, Grid):
            raise Exception("Arg 'grid' must be Grid object")
        self.grid = grid
        """Grid object"""
        self._list_orig = []
        """Original list of tuples defining the column gaps, as set with `set` method"""
        self._list = []
        """Copy of the **_list_orig** variable with altered indices depending on `Grid.expand_left`

        Its indices are altered depending on the expanding far left column.
        The values are calculated in `measure`.
        """

    def has_column(self, n=-1) -> bool:
        """
        Does column gap exist at index *n* ?

        .. python::
            if grid.colgaps.has_column( 2 ) : pass

        :param n: int, default -1
        :return:  bool
        """
        for tpl in self._list:
            (idx, width) = tpl
            if idx == n:
                return True
        return False

    def set(self, column_gaps=[]) -> None:
        """
        Set a list of *column_gaps* to private property **_list_orig**

        .. python::
            grid.colgaps.set([
                (0, None),    # 1. column gap
                (1, 0),       # 2.    "
                (2, 20),      # 3.    "
                (3, "expand") # 4.    "
            ])
            grid.colgaps.set()

        | Can only be used before any adds.
        | Based on **_list_orig** the **_list** property is created in method `measure`.
        | If called without arguments, properties **_list_orig** and **_list** are reset.
        | The 2-tuples in list *column_gaps* have the form: (*column_index, width)*

        - **column_index** : int 0 <= n < max number of `Grid.get_content_columns`
        - **width** : None, or int >= 0, or string "expand"

        :param column_gaps: list of tuples, default [ ]
        """
        grid = self.grid
        # Checks
        if grid.wh.x != 0 or grid.wh.y != 0:
            raise Exception("Cannot set 'column_gaps' after adding widgets")
        if not isinstance(column_gaps, list):
            raise Exception("'column_gaps' must be a list")

        # empty ?
        if not len(column_gaps):
            self._list_orig = []
            self._list      = []
            return

        # Check each tuple
        for tpl in column_gaps:
            if not isinstance(tpl, tuple):
                raise Exception("Each item in 'column_gaps' must be a tuple")
            (column_index, gap_width) = tpl
            # first tuple element
            if not isinstance(column_index, int) or column_index < 0 or column_index >= grid.content_columns:
                raise Exception("First tuple element must be int >= 0 and int < content_columns")
            # ... within content range ?
            val = column_index
            if grid.expand_left:
                val += 1
            if not grid.wh.is_in_content_range( val ):
                raise Exception("index in 'column_gaps' is out of range")
            # second tuple element
            if ( gap_width is not None
                 and not (isinstance(gap_width, int) and gap_width >= 0)
                 and not (isinstance(gap_width, str) and gap_width.upper() == "EXPAND") ):
                raise Exception("Second tuple element must be None, int >= 0, or string 'expand'")

        # Constrain (column_gaps < content_columns)
        if len(column_gaps) >= grid.content_columns:
            raise Exception("Number of 'columns_gaps' must be less than 'content_columns'")
        # Set
        self._list_orig = column_gaps
        self.measure()

    def get(self) -> list:
        """
        Get accessor for **_list**

        The **_list** is created in method `measure`.

        :return: list of tuples
        """
        return self._list

    def measure(self) -> None:
        """
        Create property **_list**.

        | If `Grid.expand_left` is true, the **_list_orig** is copied to **_list**, but with incremented x-indices.
        | If `Grid.expand_left` is false, the **_list_orig** is simply copied to **_list**.
        """
        self._list = []
        for tpl in self._list_orig:
            (idx, width) = tpl
            if self.grid.expand_left:
                idx += 1
            self._list.append( (idx, width) )

    def count(self) -> int:
        """
        Return the number of column gaps

        :return: int length of property **_list**
        """
        return len(self._list)

    def add_to_cells(self) -> None:
        """
        Add `_Cell` objects with `_Gap` objects with corresponding coordinates to `Grid.cells`

        | Walk through each tuple in **_list** property, create a `_Gap` object with its coordinates,
        | and put it into a `_Cell` object and aggregate it to `Grid.cells`.
        """
        grid  = self.grid
        cells = grid.cells
        max_y = cells.get_current_max_y()
        ###
        for tpl in self.get():
            (column_index, width) = tpl
            for y in range( max_y + 1 ):
                if not cells.has_taken( y, column_index ):
                    idx = column_index-1 if grid.expand_left else column_index
                    gap = _Gap( grid, "H", width, index=idx )
                    grid.cells.add(
                        _Cell( gap, y, column_index )
                    )


class _Spans():
    """
    Serve a list of 2-tuples (coordinates) which are parts of a span

    - Composed to `Grid.spans` property.
    """
    def __init__(self, grid=None):
        """
        Example

        .. python::
            grid.spans = _Spans( grid )

        :param grid: required Grid object
        """
        if not isinstance(grid, Grid):
            raise Exception("Arg 'grid' must be Grid object")
        self.grid = grid
        """Grid object"""
        self._list = []
        """List of 2-tuple cell coordinates (y,x) which are parts of any span"""

    def has(self, y=0, x=0) -> bool:
        """
        Is coordinate (y,x) part of a span ?

        .. python::
            if grid.spans.has( y=1, x=2 ) : pass
            if grid.spans.has(1, 2)       : pass

        :param y: int y coordinate
        :param x: int x coordinate
        :Return:  boolean
        """
        for tpl in self._list:
            (b, a) = tpl
            if b == y and a == x:
                return True
        return False

    def reserve(self, y=None, x=None, y_span=None, x_span=None):
        """
        Store 2-tuples as coordinates to property **_list**, belonging to a span

        .. python::
            grid.spans.reserve( y=0, x=1, y_span=2, x_span=2 )
            grid.spans.reserve(0,1, y_span=2, x_span=2)

        Mark cells belonging to a span by adding tuples of (y,x) coordinates to property **_list**.

        :param y: int y anchor of span
        :param x: int x anchor of span
        :param y_span: int size to y direction
        :param x_span: int size to x direction
        """
        if not isinstance(y, int):
            raise Exception("Arg 'y' must be integer")
        if not isinstance(x, int):
            raise Exception("Arg 'x' must be integer")
        if not isinstance(y_span, int):
            raise Exception("Arg 'y_span' must be integer")
        if not isinstance(x_span, int):
            raise Exception("Arg 'x_span' must be integer")
        for row_count in range( y_span ):
            for col_count in range( x_span ):
                self._list.append( (y + row_count, x + col_count) )


class _Cells():
    """
    Class *_Cells* aggregates `_Cell` objects in a simple list

    | Composed to `Grid.cells` property.
    | It serves methods for handling aggregated `_Cell` objects and to apply them
    | to the resulting layout. Note that coordinates are saved within `_Cell` objects.
    """
    def __init__(self, grid=None) -> None:
        """
        Example

        .. python::
            grid.cells = _Cells()

        :param grid: required Grid object
        """
        if not isinstance(grid, Grid):
            raise Exception("Arg 'grid' must be GrindHandle object")
        self.grid  = grid
        """Grid object"""
        self._list = []
        """Aggregated list of *_Cell* objects"""

    def get(self) -> list:
        """
        Get accessor for **_list** of `_Cell` objects

        .. python::
            for cell in grid.cells.get():
                print("y,x :", cell.y, cell.x)

        :Return: self._list
        """
        return self._list

    def add(self, cell=None) -> None:
        """
        Add (or aggregate) a `_Cell` object to the **_list**

        .. python::
            grid.cells.add( _Cell(...) )

        :param cell: required `_Cell` object
        """
        if not isinstance(cell, _Cell):
            raise Exception("Arg 'cell' must be _Cell object.")
        self._list.append( cell )

    def get_cell(self, y=-1, x=-1) -> object:
        """
        Return the `_Cell` object from coordinate (y,x)

        .. python::
            cell = grid.cells.get_cell( 0,1 )
            print("y,x :", cell.y, cell.x)

        Raise exception if not found.

        :param y: int >= 0
        :param x: int >= 0

        :Return: `_Cell` object
        """
        if not (isinstance(y, int) and y >= 0):
            raise Exception("Arg 'y' must be int >= 0")
        if not (isinstance(x, int) and x >= 0):
            raise Exception("Arg 'x' must be int >= 0")
        RET = None
        for cell in self.get():
            if cell.y == y and cell.x == x:
                RET = cell
                break
        if RET is None:
            raise Exception(f"Cannot find cell ({y},{x})")
        return RET

    def get_last(self) -> object:
        """
        Return the last inserted `_Cell` object

        .. python::
            cell = grid.cells.get_last()

        :return: `_Cell` object
        """
        return self.get()[-1]

    def has_taken(self, y=-1, x=-1) -> bool:
        """
        Check if a `_Cell` object exists at coordinate (y, x)

        .. python::
            if grid.cells.has_taken( 0,1 ) : pass

        :param y: int
        :param x: int

        :return: bool
        """
        if not (isinstance(y, int) and isinstance(x, int)):
            raise Exception("Arg 'y' and 'x' must be integers")
        grid = self.grid
        # Is cell (y,x) unused ?
        for cell in self._list:
            if cell.y == y and cell.x == x:
                return True
            if grid.spans.has( y, x ):
                return True
        ######
        return False

    def get_current_max_y(self) -> int:
        """
        Get the maximum y-coordinate value out of all aggregated `_Cell` objects

        .. python::
            max_y = grid.cells.get_current_max_y()

        :return: int max y
        """
        max_y = 0
        for cell in self._list:
            if cell.y > max_y:
                max_y = cell.y
        return max_y

    def apply_to_layout(self) -> None:
        """
        Add all `_Cell.item` objects to the resulting QGridLayout

        .. python::
            grid.cells.apply_to_layout()
        """
        layout = self.grid.layout
        ###
        # Methods to use:
        #
        # for Grid objects  : layout.addLayout( obj.layout, y,x, y_span, x_span )
        # for QLayout objects     : layout.addLayout( obj,        y,x, y_span, x_span )
        # for QSpacerItem objects : layout.addItem(   obj,        y,x, y_span, x_span )
        # for QWidget objects     : layout.addWidget( obj,        y,x, y_span, x_span )
        ###
        for cell in self.get():
            if cell.item is None:
                # Cell None
                continue
            elif isinstance(cell.item, _Gap):
                # Cell Gap
                gap = cell.item
                if gap.item is None:
                    # -> Gap None
                    continue
                elif isinstance(gap.item, QSpacerItem):
                    # -> Gap QSpacerItem
                    layout.addItem( gap.item, cell.y, cell.x, cell.y_span, cell.x_span )
                elif isinstance(gap.item, QLabel):
                    # -> Gap QLabel
                    layout.addWidget( gap.item, cell.y, cell.x, cell.y_span, cell.x_span )
                else:
                    raise Exception("unknown gap.item value:", gap.item)
            elif isinstance(cell.item, Grid):
                # Cell Grid
                layout.addLayout( cell.item.layout, cell.y, cell.x, cell.y_span, cell.x_span )
            elif isinstance(cell.item, QSpacerItem):
                # Cell QSpacerItem
                layout.addItem( cell.item, cell.y, cell.x, cell.y_span, cell.x_span )
            elif isinstance(cell.item, QLayout):
                # Cell QLayout
                layout.addLayout( cell.item, cell.y, cell.x, cell.y_span, cell.x_span )
            elif isinstance(cell.item, QWidget):
                # Cell QWidget
                layout.addWidget( cell.item, cell.y, cell.x, cell.y_span, cell.x_span )
            else:
                raise Exception("unknown cell.item value:", cell.item)


class _Cell():
    """
    *_Cell* objects are aggregated to `_Cells._list`, which itself is composed to `Grid.cells`

    A *_Cell* has an **item** property holding an object together with coordinates and span values.
    """
    def __init__(self, item=None, y=None, x=None, y_span=1, x_span=1) -> None:
        """
        Example

        .. python::
            cell = _Cell( item=_Gap(...),   y=0, x=1, y_span=2, x_span=2 )
            cell = _Cell( _Grid(...), 0,1, y_span=2, x_span=2 )
            cell = _Cell( *QSpacerItem*,    0,1, y_span=2, x_span=2 )
            cell = _Cell( *QLayout*, 0,1 )
            cell = _Cell( *QWidget*, 0,1 )
            ####
            grid.cells.add( cell )

        :param item:   None or `_Gap`, or `Grid`, or QSpacerItem, QLayout, QWidget
        :param y:      int y coordinate
        :param x:      int x coordinate
        :param y_span: int y direction span
        :param x_span: int x direction span
        """
        # Arguments
        ok = False
        if item is None:
            ok = True
        if isinstance(item, _Gap):
            ok = True
        if isinstance(item, Grid):
            ok = True
        if isinstance(item, QSpacerItem):
            ok = True
        if isinstance(item, QLayout):
            ok = True
        if isinstance(item, QWidget):
            ok = True
        if not ok:
            msg = f"Arg 'item' ({item}) must be None or object of type _Gap, Grid, QSpacerItem, QLayout, or QWidget"
            raise Exception( msg )
        if not isinstance(y, int):
            raise Exception("Arg 'y' must be integer")
        if not isinstance(x, int):
            raise Exception("Arg 'x' must be integer")
        if not isinstance(y_span, int):
            raise Exception("Arg 'y_span' must be integer")
        if not isinstance(x_span, int):
            raise Exception("Arg 'x_span' must be integer")
        # Set
        self.item = item
        """must be None or `_Gap`, or `Grid`, or QSpacerItem, QLayout, QWidget"""
        self.y = y
        """int y coordinate"""
        self.x = x
        """int x coordinate"""
        self.y_span = y_span
        """int y direction span"""
        self.x_span = x_span
        """int x direction span"""


class _Gap():
    """
    A gap within the layout has a **direction** and a **length**. Objects are hold in `_Cell.item` properties

    - Coordinates of a *_Gap* are not saved in this class, but in
      class *_Cell* as `_Cell.y` and `_Cell.x` properties.
    - It may display a column index number with a label.
    """
    def __init__(self, grid=None, direction=None, length=None, index=-1):
        """
        Examples

        .. python::
            cell = _Cell( _Gap(...), y=0, x=1, y_span=2, x_span=2 )

            # horizontal direction
            _Gap(grid)                                 # H, explicit empty
            _Gap(grid, direction="H", length=None)     # H, explicit empty
            _Gap(grid, direction="H", length=0)        # H, explicit empty
            _Gap(grid, direction="H", length=20)       # H, sized (yellow)
            _Gap(grid, direction="H", length="expand") # H, expand (blue)
            _Gap(grid, direction="H", length="unused") # H, unused (magenta)

            # horizontal direction is default
            _Gap(grid, length=None)     # H, explicit empty
            _Gap(grid, length=0)        # H, explicit empty
            _Gap(grid, length=20)       # H, sized (yellow)
            _Gap(grid, length="expand") # H, expand (blue)
            _Gap(grid, length="unused") # H, unused (magenta)

            # vertical direction
            _Gap(grid, direction="V", length=None)     # V, explicit empty
            _Gap(grid, direction="V", length=0)        # V, explicit empty
            _Gap(grid, direction="V", length=20)       # V, sized (yellow)
            _Gap(grid, direction="V", length="expand") # V, expand (blue)
            _Gap(grid, direction="V", length="unused") # V, unused (magenta)

            # If given, the index argument is displayed
            _Gap(grid, length=20, index=0)
            _Gap(grid, index=20)

        :parameters:
            grid : object
                Grid
            direction : None or str
                "H", "V", "horizontal", "vertical"
            length : None, int, or str
                - If length == "expand", then add expander.
                - If length == None or 0, then leave the cell empty (also add coordinates to `_Spans`).
                - If length >= 1, then add fixed size spacer.
            index : int
                If given, it will be displayed as a label

        """
        if not isinstance(grid, Grid):
            raise Exception("Arg 'grid' must be Grid object")
        self.grid = grid
        """Grid object"""
        self.is_expander = False
        """Do this *gap* expand ?

        .. python::
            if self.is_expander : pass
        """
        self.is_empty    = True
        """Is this *gap* explicitly empty (gap.item == None) ?

        .. python::
            if self.is_empty : pass
        """
        self.item        = None
        """Object as returned from `_gap_item` method : *None*, *QLabel* or *QSpacerItem*"""
        self.label       = None
        """If instance argument **index** is given, display a label with its number"""
        self.direction   = direction
        """Expanding or size direction 'H', 'V', 'vertical', or 'horizontal'"""
        self.length      = length
        """Length or size of this *gap*. Can be None, "expand", or int"""
        self.index       = index
        """If integer is given, it will be displayed as a label"""

        # Arg 'direction', None, H, HORIZONTAL, V, VERTICAL
        err = "Arg 'direction' must be (H|horizontal|V|vertical)"
        if direction is None:
            direction = "H"
            length    = 0
        if ( not isinstance(direction, str)
             or direction.upper() not in ["H", "HORIZONTAL", "V", "VERTICAL"] ):
            raise Exception( err )
        self.direction = "H" if direction.upper() in ["H", "HORIZONTAL"] else "V"

        # Arg 'length', None, int >= 0, "EXPAND", "UNUSED"
        err = "Arg 'length' must be None, integer >= 0, or string 'expand', or string 'unused'"
        ok  = False
        if length is None:
            length = 0
            self.is_empty = True
            ok = True
        if isinstance(length, int):
            if length < 0:
                raise Exception( err )
            if length == 0:
                self.is_empty = True
            ok = True
        if isinstance(length, str):
            length = length.upper()
            if not (length == "EXPAND" or length == "UNUSED"):
                raise Exception( err )
            if length == "EXPAND":
                self.is_expander = True
            ok = True
        if not ok:
            raise Exception( err )
        self.length = length

        # Arg 'index', integer
        if index is not None and not isinstance(index, int):
            raise Exception("Arg 'index' must be None or integer")
        if index is None:
            self.index = ""
        elif index == -1:
            x = self.grid.wh.x
            x = x-1 if self.grid.expand_left else x
            self.index = str(x)
        else:
            self.index = str( index )

        # Item
        self.item = self._gap_item()

    def _gap_item(self) -> QObject:
        """
        Create an object at init time representing this gap: *None*, *QLabel* or *QSpacerItem*

        .. python::
            self.item = self._gap_item()

        | Visualize expander or gaps with a colored QLabel or a QSpacerItem
        | with the corresponding expansion, behaviour, or size.

        :return: None, QLabel, QSpacerItem
        """
        # Label
        label = QLabel()
        label.setAutoFillBackground( True )
        label.setAlignment( Qt.AlignmentFlag.AlignCenter )
        # Label text
        if self.grid.work_up:
            label.setText( self.index )
        else:
            label.setText("")
        # Label palette
        palette = QPalette()
        # Label background color
        (r, g, b) = (0, 0, 0)
        # Label Size policy
        sizePolicy = None
        # Label margin
        margin = 1

        if isinstance(self.length, str) and self.length == "UNUSED":
            # Unused cell
            # ===========
            if self.grid.work_up:
                # Label size policy
                sizePolicy = QSizePolicy( QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum )  # W,H
                # Label margin
                label.setMargin( margin )
                # Label background color
                (r, g, b) = MAGENTA
                # Label text color more bright
                # (apply brush to palette)
                q_color = QColor(210, 210, 210)
                brush   = QBrush( q_color )
                brush.setStyle( Qt.BrushStyle.SolidPattern )
                palette.setBrush( QPalette.ColorRole.WindowText, brush )
            else:
                return None

        elif self.length == 0:
            # Explicit empty cell
            # ===================
            # Label size policy
            if self.grid.work_up:
                # Label size policy
                sizePolicy = QSizePolicy( QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum )  # W,H
                # Label margin
                label.setMargin( margin )
                # Label background color
                (r, g, b) = GREY
            else:
                return None

        elif self.is_expander:
            # Expander
            # ========
            if self.direction == "H":
                # Horizontal expander
                # -------------------
                if self.grid.work_up:
                    # Label size policy
                    sizePolicy = QSizePolicy( QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum )  # W,H
                    # Label background color
                    (r, g, b) = BLUE
                    # Label text color more bright
                    # (apply brush to palette)
                    q_color = QColor(210, 210, 210)
                    brush   = QBrush( q_color )
                    brush.setStyle( Qt.BrushStyle.SolidPattern )
                    palette.setBrush( QPalette.ColorRole.WindowText, brush )
                else:
                    # Return QSpacerItem
                    (width, height) = (1, 1)
                    v_size = QSizePolicy.Policy.Minimum
                    h_size = QSizePolicy.Policy.Expanding
                    return QSpacerItem( width, height, h_size, v_size )
            else:
                # Vertical expander
                # -----------------
                if self.grid.work_up:
                    # Label size policy
                    sizePolicy = QSizePolicy( QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding )  # W,H
                    # Label background color
                    (r, g, b) = CYAN
                else:
                    # Return QSpacerItem
                    (width, height) = (1, 1)
                    v_size = QSizePolicy.Policy.Expanding
                    h_size = QSizePolicy.Policy.Minimum
                    return QSpacerItem( width, height, h_size, v_size )
        else:
            # Fixed sized gaps
            # ================
            if self.direction == "H":
                # Horizontal gap
                # --------------
                # Label size policy
                sizePolicy = QSizePolicy( QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum )  # W,H
                # Label margin
                label.setMargin( margin )
                # Label background color
                (r, g, b) = YELLOW
                # Label fixed width
                label.setFixedWidth( self.length )
            else:
                # Vertical gap
                # ------------
                # Label size policy
                sizePolicy = QSizePolicy( QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed )  # W,H
                # Label margin
                label.setMargin( margin )
                # Label background color
                (r, g, b) = ORANGE
                # Label fixed height
                label.setFixedHeight( self.length )

        # Apply brush (label background) to palette
        if self.grid.work_up:
            q_color = QColor( r, g, b )
            brush   = QBrush( q_color )
            brush.setStyle( Qt.BrushStyle.SolidPattern )
            palette.setBrush( QPalette.ColorRole.Window, brush )
            label.setPalette( palette )

        # Return label
        label.setSizePolicy( sizePolicy )
        return label

