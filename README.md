# Mapping Trainer

Python utility to practice new keyboard mappings.

## Setup

1. Install Python 3.8.3 (probably works with other versions, but not tested)
1. Set up virtual environment if desired:
    1. [path to python]\python -m venv .venv
    1. .venv\scripts\Activate.ps1 (if PowerShell) -OR- call .venv\scripts\activate.bat (if cmd)
    1. Make sure you see (.venv) prepending your command prompt
1. pip install --upgrade pip
1. pip install PyQt5
1. pip install pyqt5-tools~=5.15
1. pip install qasync
1. pip install debugPy
1. pip install hid

Will need hidapi.dll in the root folder of the Python source:
https://github.com/libusb/hidapi/releases/latest

## TODO

- When restoring to word practice mode on startup, it loads too many lines
- Keep working on state persistence
    - Make options for advancing on enter/space or not
    - Keep testing
- Allow selection between indentation styles in case auto-detection doesn't work
- Update to PySide6
- DeprecationWarning: sipPyTypeDict() is deprecated, the extension module should use sipPyTypeDictRef() instead
- Add an options dialog
- Save stats in a database of some kind (DuckDB or Polars/Parquet). Do maximum potential WPM including all chars and navigation (backspace, del, arrows, etc.). Do an accuracy based correct / a total of chars (but not nav here). Do WPM as it's done now (net WPM to type the correct promp).
- Better visualizations of speed and accuracy
- Plots and analysis of stats in some form
- Make an installer
- Interface directly with project Gutenberg?
- Ebook formats?
- Dark mode
- Make forward/back and font up/down buttons prettier
- Update code_info from a dictionary to a bespoke object

