# qtgrid

[1]: https://www.riverbankcomputing.com/software/pyqt/ "PyQt"
[2]: https://www.qt.io/qt-for-python                   "PySide6"
[3]: REFERENCE.md                                      "Reference Manual"
[4]: TUTORIAL.md                                       "qtgrid Tutorial"
[5]: https://pypi.org                                  "PyPi"
[6]: FIXME                                             "API Documentation"

The python **qtgrid** package is for [PyQt][1], or [PySide][2] developers. It helps to build *QGridLayout's* dynamically and with visual help during implementation time. Note that **qtgrid** works in the same way for PyQt5, PyQt6, and PySide6.

See also the [tutorial][4], the [reference manual][3], or for the brave the [API Documentation][6].

This package is licensed under *GNU LGPLv3*.

## Example Usage

```python
from qtgrid import Grid

grid = Grid(
    layout          = QGridLayout(), # QGridLayout object (eg. from QtDesigner)
    content_columns = 8,             # Maximum number of columns
    expand_left     = False,         # Apply left side expander
    expand_right    = True,          # Apply right side expander
    column_gaps     = [
        # Define gap's for complete columns
        (0, 0),        # (column_index, width) / width can be ...
        (2, 20),       #  - 0 or None := set cells explicitly empty (as is)
        (4, "expand"), #  - "expand"  := add horizontal expander
        (6, 20),       #  - number    := add horizontal spacer of fixed size
    ],
    # Prepare your own lists, to access your added widgets afterwards.
    # See also layout.add(), and layout.add_label().
    list_names = ["headers", "labels"],

    # Show visual help while development
    work_up = True
)
# QGridLayout settings
grid.layout.setSpacing(1)
```

Add arbitrary widgets to the grid layout. Don't bother about indices.

```python
myLabel = QLabel("add example")
grid.add(
    widget  = myLabel,   # required
    y_span  = 1,         # optional
    x_span  = 1,         # optional
    to_list = "labels"   # optional / add the widget to your prepared list named "labels"
)
# .. or simply ..
grid.add( myLabel )
```

**qtgrid** is mostly about widgets layout. But especially for labels you can use appropriate configured ones as a blueprint for a common design :

```python
# Add a label as a copy source
myLabel = QLabel()
# ... configure your label ...
grid.set_label_source( name_id="foo", label=myLabel )

# Add a new label to the grid and copy its config from "foo"
grid.add_label("foo", "Some Text")
grid.add_label("foo", "Some Text", to_list="labels")
```

Gaps within the grid are quite essential :

```python
# Add horizontal gaps
grid.add_gap(20)         # add fixed size spacer
grid.add_gap("expander") # add expanding spacer

# Add vertical gaps
grid.add_gap("V", 20)
grid.add_gap("V", "expander")

# Add empty row below the current row
grid.add_empty_row(20)
grid.add_empty_row("expand")
```

Always call the following method at the end. This will actually apply all widgets, gaps, and expander to the underlying *QGridLayout* object.

```python
grid.finish()
```

Later on, to access your prepared lists:

```python
headers = grid.get_list("headers")
labels  = grid.get_list("labels")
for i in range( len(headers) ):
    print( headers[i].text() )
    print( labels[i].text() )
```

## Install

Use pip or pipenv

- pip install qtgrid
- pipenv install qtgrid

Get the current project source from GitHub

- git clone https://github.com/devlog42/qtgrid

## Contribution

## Code of Conduct
