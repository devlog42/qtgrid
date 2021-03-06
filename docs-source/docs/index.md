# qtgrid

[1]: https://www.riverbankcomputing.com/software/pyqt/ "PyQt"
[2]: https://www.qt.io/qt-for-python                   "PySide6"
[3]: https://pypi.org                                  "PyPi"
[4]: https://github.com/devlog42/qtgrid/blob/main/.github/CONTRIBUTING.md    "Contributing"
[5]: https://github.com/devlog42/qtgrid/blob/main/.github/CODE_OF_CONDUCT.md "Code of Conduct"
[6]: https://github.com/devlog42/qtgrid/blob/main/LICENSE  "License"

The python **qtgrid** package is for [PyQt][1], or [PySide][2] developers. It helps to build *QGridLayout's* dynamically and with visual help during implementation time. Note that **qtgrid** works in the same way for PyQt6, PyQt5, and PySide6.

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

Get the current development source from GitHub

- git clone https://github.com/devlog42/qtgrid

When importing **qtgrid**, for an installation of PyQt6, PyQt5, or PySide6 is tested in that order.
If none of these are found, a corresponding error message is issued.

## Contribution

Every contribution that advances this project is very welcome.

If you want to report a bug or ask about a new feature, please visit the dedicated [issues][3] page. There you'll find suitable templates for your request, including one that is esspecially intended for mistakes in the documentations.

However, if you want to get involved in development, please check out the [Contribution][4] page first.

When you write posts, it goes without saying that you use a friendly language. Of course there is also a separate page on the topic called [Code of Conduct][5].

## License

The [License][6] of this package comes in terms of *GNU LGPLv3*.
