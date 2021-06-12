# The qtgrid Reference Manual

[1]: https://devlog42.github.io/qtgrid/api/       "API Documentation"
[2]: https://devlog42.github.io/qtgrid/tutorial/  "qtgrid Tutorial"

Taken for granted, the primary source is the [API documentation][1]. The [qtgrid tutorial][2] gives an in deep explanation, and this reference manual is intended to give an overview for the everyday module usage.

## Instantiation and Usage <a name="instatiation"></a>

The following two instantiations are equivalent:

```python
grid = Grid()
```

```python
grid = Grid(
	layout          = QGridLayout(),
	content_columns = 1,
    expand_left     = False,
    expand_right    = False,
	column_gaps     = [],
	list_names      = [],
    work_up         = False
)
```

<dl>
  <dt>layout</dt>
  <dd>
	Optional <i>QGridLayout</i> object whose items will be cleared. <br/>
	If left out, it will be instantiated within the <i>Grid</i> constructor.
  </dd>
  <dt>content_columns</dt>
  <dd>
	The maximum number of content columns. <br/>
	Optional integer n with n >= 1 and n > max number of <b>column_gaps</b> (see below). Default 1.
  </dd>
  <dt>expand_left</dt>
  <dd>
    Set whether or not a far left expanding column will be added, thus influencing the grid alignment.<br/>
    Optional boolean value. Default False.
  </dd>
  <dt>expand_right</dt>
  <dd>
	Set whether or not a far right expanding column will be added, thus influencing the grid alignment.<br/>
    Optional boolean value. Default False.
  </dd>
  <dt>column_gaps</dt>
  <dd>
	Define gap cells for complete columns.<br/>
	Optional list of tuples. Default [ ].<br/>
	See also the <a href="#set-column-gaps">set_column_gaps()</a> method.
  </dd>
  <dt>list_names</dt>
  <dd>
	Prepare internal lists with given names. <br/>
	Optional list of strings naming internal lists to create. Default [ ]. <br/>
	The lists purpose is to hold added widgets for later disposal. <br/>
	See also the <a href="#set-list-names">set_list_names()</a> method.
  </dd>
  <dt>work_up</dt>
  <dd>
    Set whether or not to activate the <i>work up</i> mode.<br/>
	Optional boolean value. Default is False.<br/>
	In <i>work-up</i> mode a visual feed back is given for otherwise invisible cells. <br/>
	See also the <a href="#set-work-up">set_work_up()</a> method for a list of used colors and their meanings.
  </dd>
</dl>

In most cases the best place for the *Grid* instantiation is within class constructors while the dynamic build process is delegated to another method. You may apply settings for the wrapped *QGridLayout* object directly after the instantiation.

```python
class Example():
    def __init__(self):

	self.grid = Grid(
		layout       = QGridLayout(), # Optional QGridLayout object
		max_x        = 8,             # Maximum number of content columns
	    expand_left  = False,
	    expand_right = True,

		column_gaps  = [
			# Define gaps for complete columns
			(0, 0),        # (column_index, width) / "width" can be ...
			(2, None),     #   - 0 or None := leave cells explicitly empty
			(4, "expand"), #   - "expand"  := add horizontal expander
			(6, 20),       #   - number    := add fixed sized column gaps
		],
	
		# Prepare internal lists to hold widgets for my disposal
		list_names = ["headers", "labels"],

	    # Show visual help
	    work_up = True
	)
	# QGridLayout settings
	self.grid.layout.setSpacing(1)
```

In your methods where the grid is build up you often call the [clear()](#clear) method, otherwise the widgets would be added repeatedly. At the end you need to call the [finish()](#finish) method to actually apply all added widgets, gaps, and expander.

```python
	def build_grid(self):
		grid = self.grid
		grid.clear()
	
		#############
		# Add widgets

		########
		# Finish
		grid.finish()
```

## Set Instantiation Options <a name="after-instatiation"></a>

Use the following methods in case you did not set at construction time.  
**Note:** You can do that only before any widget is added or after calling the [clear()](#clear) method.

```python
grid.clear()
grid.set_content_columns( 8 )
grid.set_expand_left( False )
grid.set_expand_right( True )
grid.set_column_gaps(
    [ (0, 0), (2, None), (4, "expand"), (6, 20) ]
)
grid.set_list_names(
    [ "headers", "labels" ]
)
grid.set_work_up( True )
```

### set\_column\_gaps() <a name="set-column-gaps"></a>

Define gap cells for complete columns. If called without argument, all column gaps will be removed. Can only be used before any widget is added or after calling the [clear()](#clear) method.

`grid.set_column_gaps( column_gaps=[ <tuple>, <tuple>, ... ] )`

```python
grid.set_column_gaps( column_gaps=[ (0,20), (2,None), (4,"expand"), (6,20) ] )
grid.set_column_gaps([
	(0, 0),        # (column_index, width) / "width" can be ...
	(2, None),     #   - 0 or None := leave cells explicitly empty
	(4, "expand"), #   - "expand"  := add horizontal expander
	(6, 20),       #   - number    := add fixed sized column gap
])
grid.set_column_gaps()
```

<dl>
  <dt>column_gaps</dt>
  <dd>
	Optional <i>column_gaps</i> argument is a list of tuples. <br/>
	Each tuple has the form: <b>(column_index, width)</b>.
	<ul>
	 <li><i>column_index</i> <br/>integer n with 0 <= n < <b>content_columns</b> number</li>
	 <li><i>width</i> <br/>keyword None, or string "expand", or int >= 0</li>
	</ul>
  </dd>
</dl>

The overall used tuples, thus the number of column gaps, must be less than *content\_columns* number.
The *width* value can be None, int >= 0, or the string "expand". Here, value *0* and *None* are equivalent.

### set\_expand\_left() <a name="set-expand-left"></a>

Set whether or not a far left expanding column is added, thus influencing the grid alignment. Can only be used before any widget is added or after calling the [clear()](#clear) method.

`grid.set_expand_left( flag=<bool> )`

```python
grid.set_expand_left( flag=False )
grid.set_expand_left( False )
grid.set_expand_left()
```

<dl>
  <dt>flag</dt>
  <dd>
	Optional boolean value. Default False.
  </dd>
</dl>

### set\_expand\_right() <a name="set-expand-right"></a>

Set whether or not a far right expanding column is added, thus influencing the grid alignment. Can only be used before any widget is added or after calling the [clear()](#clear) method.

`grid.set_expand_right( flag=<bool> )`

```python
grid.set_expand_right( flag=False )
grid.set_expand_right( False )
grid.set_expand_right()
```

<dl>
  <dt>flag</dt>
  <dd>
	Optional boolean value. Default False.
  </dd>
</dl>

### set\_list\_names() <a name="set-list-names"></a>

Prepare internal lists with given names. If called without the argument, all internal lists will be removed. Can only be used before any widget is added or after calling the [clear()](#clear) method.

`grid.set_list_names( names=[ <str>, <str>, ... ] )`

```python
grid.set_list_names( names=[ "list1", "list2" ] )
grid.set_list_names( ["list1", "list2"] )
grid.set_list_names()
```

<dl>
  <dt>names</dt>
  <dd>
	Optional list with string names identifying the internal lists to be created.
  </dd>
</dl>

You can add widgets to those prepared lists with the *to_list* argument along with the [add()](#add) or [add\_label()](#add-label) methods. After all, use the [get\_list\_names()](#get-list-names), or [get\_list()](#get-list) methods to access the lists in turn.

### set\_content\_columns() <a name="set-content-columns"></a>

Set the maximum number of content columns. Can only be used before any widget is added or after calling the [clear()](#clear) method.

`grid.set_content_columns( content_columns=<int> )`

```python
grid.set_content_columns( content_columns=1 )
grid.set_content_columns( 1 )
```

<dl>
  <dt>content_columns</dt>
  <dd>
	Optional integer n with n >= 1 and n > number of <b>column_gaps</b>. Default is 1.
  </dd>
</dl>

See also the [set\_column\_gaps()](#set-column-gaps) method.

### set\_work\_up() <a name="set-work-up"></a>

Set whether or not to activate the *work up* mode. Can only be used before any widget is added or after calling the [clear()](#clear) method.

`grid.set_work_up( flag=<bool> )`

```python
grid.set_work_up( flag=False )
grid.set_work_up( False )
grid.set_work_up()
```

<dl>
  <dt>flag</dt>
  <dd>
	Optional boolean value. Default is False.
  </dd>
</dl>

In *work up* mode otherwise invisible cells are colored indicating the following meaning:

<dl>
  <dt>Magenta</dt>
  <dd>
	unused cell
  </dd>
  <dt>Blue</dt>
  <dd>
	horizontal expander
  </dd>
  <dt>Cyan</dt>
  <dd>
	vertical expander
  </dd>
  <dt>Yellow</dt>
  <dd>
	fixed sized horizontal gap
  </dd>
  <dt>Orange</dt>
  <dd>
	fixed sized vertical gap
  </dd>
  <dt>Grey</dt>
  <dd>
	explicit empty cell
  </dd>
</dl>

## Methods <a name="methods"></a>

### add() <a name="add"></a>

Add arbitrary widgets to the *grid*. 

`grid.add( widget=<QWidget>, y_span=<int>, x_span=<int|"all">, to_list=<str> )`

```python
grid.add( widget=WIDGET, y_span=1, x_span=1, to_list="list_name" )
grid.add( WIDGET, y_span=2, x_span=2 )
grid.add( WIDGET, x_span="all" )
grid.add( WIDGET )
```

<dl>
  <dt>widget</dt>
  <dd>
	Required QWidget object to add.
  </dd>
  <dt>y_span</dt>
  <dd>
	Optional int >= 1. Default 1.
  </dd>
  <dt>x_span</dt>
  <dd>
	Optional int >= 1, or string "all". Default 1.
  </dd>
  <dt>to_list</dt>
  <dd>
	Optional string identifying an internal prepared list, or the None keyword. Default None.
  </dd>
</dl>

The *to_list* argument can be used to not only add the widget to the *grid*, but also to a prepared internal list for later use. See also the [set\_list\_names()](#set-list-names) method. 

The *y_span* and *x_span* integer arguments spans the cell over the given number of rows and columns. If *x_span* value is "all" the cell spans over the remaining row.

### add\_empty\_row() <a name="add-empty-row"></a>

`grid.add_empty_row( height=<int|"expand"> )`

```python
grid.add_empty_row()     # same as None
grid.add_empty_row(0)    # same as None
grid.add_empty_row(None) # explicitly empty
grid.add_empty_row(20)
grid.add_empty_row("expand")
```

Add a row gap.

<dl>
  <dt>height</dt>
  <dd>
	Optional keyword None, int >= 0, or string "expand". Default None.
  </dd>
</dl>


If not in the first column: fill the remaining row with explicit empty cells (colored grey), then ... <br/>
In the first column of a row: apply a vertical gap by adding a single cell spawning the complete row.

Above, the first three calls are all equivalent. When given a integer number, the row gets a fixed height in pixels. If the string "expand" is used, the row expands in vertical direction.

See the [set\_work\_up()](#set-work-up) method for a list of displayed colors in *work_up* mode.

### add\_gap() <a name="add-gap"></a>

Add a cell gap.

`grid.add_gap( direction=<str>, length=<int|"expand">, y_span=<int>, x_span=<int> )`

```python
# horizontal direction
grid.add_gap("H")           # same as None
grid.add_gap("H", 0)        # same as None
grid.add_gap("H", None)     # explicitly empty
grid.add_gap("H", 20)
grid.add_gap("H", "expand")

# horizontal direction is default
grid.add_gap()         # same as None
grid.add_gap(0)        # same as None
grid.add_gap(None)     # explicitly empty
grid.add_gap(20)
grid.add_gap("expand")

# vertical direction
grid.add_gap("V")           # same as None
grid.add_gap("V", 0)        # same as None
grid.add_gap("V", None)     # explicitly empty
grid.add_gap("V", 20)
grid.add_gap("V", "expand")
```

<dl>
  <dt>direction</dt>
  <dd>
  	None, "H" (default) , "V", "horizontal", or "vertical"
  </dd>
  <dt>length</dt>
  <dd>
	None, int >= 0, or "expand", default None
  </dd>
  <dt>y_span</dt>
  <dd>
	Optional int >= 1. Default is 1.
  </dd>
  <dt>x_span</dt>
  <dd>
    Optional int >= 1. Default is 1.
  </dd>
</dl>

The *direction* argument comes into account when the gap has a fixed size or should be an expander. It defaults to the horizontal direction. Thus, to add a gap horizontally, you may left out the *direction* argument :

```python
grid.add_gap(20)         # add horizontal fixed size gap
grid.add_gap("expander") # add horizontal expander
```

In order to orient vertically use the "V" or "vertical" value for the *direction* argument :

```python
grid.add_gap("V", 20)
grid.add_gap("V", "expander")
```

See the [set\_work\_up()](#set-work-up) method for a list of displayed colors in *work_up* mode.

### add\_label() <a name="add-label"></a>

Add a new label to the grid. Copy the label configuration from a previously stored label.

`grid.add_label( name_id=<str>, text=<str>, y_span=<int>, x_span=<int|"all">, to_list=<str> )`

```python
grid.add_label(
	name_id = "foo",
	text    = "lorem ipsum",
	y_span  = 2,
	x_span  = 2,
	to_list = "list1"
)
grid.add_label("foo", "lorem ipsum")
grid.add_label("foo", "lorem ipsum", x_span="all")
```

<dl>
  <dt>name_id</dt>
  <dd>
	Required string identifying an internally stored label widget. <br>
	See also the <a href="#set-label-source">set_label_source().</a> <br>
	That label serves as a copy source for its attributes.
  </dd>
  <dt>text</dt>
  <dd>
	Optional text for the new label. Default is ''.
  </dd>
  <dt>y_span</dt>
  <dd>
	Optional integer n with n >= 1. Default is 1.
  </dd>
  <dt>x_span</dt>
  <dd>
	Optional integer n with n >= 1, or string "all". Default is 1.
  </dd>
  <dt>to_list</dt>
  <dd>
	Optional string identifying an internally stored list, or the None keyword. Default is None.
  </dd>
  <dt>x_span_remain</dt>
  <dd>
	Optional boolean value. Default is False.
  </dd>
</dl>

The *name_id* argument references to a label preset. If the *x_span* value is "all" the added label
spans over the remaining row. For your disposla, you may also add the label to an internal list with
the *to_list* argument, or use the [get\_label()](#get-label) method.

There are predefined defaults:

```python
grid.add_label("default", "lorem ipsum")
grid.add_label("default-header", "Some Header")
```

### clear() <a name="clear"></a>

Clear all cells and the underlying *QGridLayout* object. You likely want to call this in your method where the *grid* is build-up dynamically. Otherwise, all widgets are added repeatedly. See [Instantiation and Usage](#instatiation).

`grid.clear()`

This removes each grid cell, resets internal indices, removes all spans and reinitialize all prepared lists.
See also the [set\_list\_names](#set-list-names) method.

### finish() <a name="finish"></a>

Always call this method after you added all your widgets.

`grid.finish()`

It applies all gaps, expander and marks unused cells (colored magenta).
See the [set\_work\_up()](#set-work-up) method for a list of displayed colors in **work\_up** mode.

### get\_list() <a name="get-list"></a>

Get *name* list of widgets as it was prepared with [set\_list\_names](#set-list-names).

`<list of QWidget objects> = grid.get_list( name=<str> )`

```python
for widget in grid.get_list("list1"):
    pass
```

The returned list contains *QWidget* objects added with the [add()](#add) or [add\_label()](#add-label) methods.

<dl>
  <dt>name</dt>
  <dd>
	Required string identifying a stored internal list.
  </dd>
</dl>

### get\_list\_names() <a name="get-list-names"></a>

Get all custom list names as they were prepared with [set\_list\_names()](#set-list-names).

`<list of str> = grid.get_list_names()`

```python
for name in grid.get_list_names():
    for widget in grid.get_list( name ):
        pass
```

### get\_content\_columns() <a name="get-content-columns"></a>

Get the maximum number of content columns.

`<int> = grid.get_content_columns()`

### get\_label() <a name="get-label"></a>

Get stored *QLabel* object by *name_id*.

`<QLabel> = grid.get_label( name_id=<str> )`

```python
label = grid.get_label( name_id="foo" )
label = grid.get_label( "foo" )
```

Labels are stored with [set\_label\_source](#set-label-source).<br>

<dl>
  <dt>name_id</dt>
  <dd>
	Required string identifying a stored QLabel object.
  </dd>
</dl>

### set\_label\_source() <a name="set-label-source"></a>

Store a given QLabel object as a copy source for its attributes.

`grid.set_label_source( name_id="foo", label=myLabel )`

`grid.set_label_source("foo", myLabel)`

The *name\_id* is the key to access the label with the [add\_label()](#add-label), or [get\_label()](#get-label) methods.

<dl>
  <dt>name_id</dt>
  <dd>
	Required string id for the given label to be stored.
  </dd>
  <dt>label</dt>
  <dd>
	Required <i>QLabel</i> object with proper configuration.
  </dd>
</dl>

