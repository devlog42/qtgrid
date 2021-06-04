import pytest, sys
from qtgrid import Grid

############################
# Check Qt package to import
import importlib

if importlib.util.find_spec("PyQt6") is not None:
    from PyQt6.QtWidgets import QApplication, QLabel
elif importlib.util.find_spec("PyQt5") is not None:
    from PyQt5.QtWidgets import QApplication, QLabel
elif importlib.util.find_spec("PySide6") is not None:
    from PySide6.QtWidgets import QApplication, QLabel
else:
    raise Exception("Cannot find package PySide6, PyQt6, or PyQt5")

# A singleton QApplication objects must be created.
qapp = QApplication(sys.argv)

@pytest.fixture
def grid():
   return Grid()

@pytest.fixture
def some_label():
    label = QLabel("test")
    return label
