# Mapping Trainer

Python utility to practice new keyboard mappings and type-read books.

## Setup

1. Install Python 3.14.2 (probably works with other versions, but not tested)
1. Set up virtual environment if desired:
    1. [path to python]\python -m venv .venv
    1. .venv\scripts\Activate.ps1 (if PowerShell) -OR- call .venv\scripts\activate.bat (if cmd)
    1. Make sure you see (.venv) prepending your command prompt
1. pip install --upgrade pip
1. pip install PySide6
1. pip install qasync
1. pip install debugPy
1. pip install hidapi
1. pip install Pygments
1. pip install detect-indent

## TODO

Bugs:
- Hitting alt-left in word mode needs to be disabled.

Features:
- Add alternate case for ngram highlighting (i.e. " The", " For", and all-caps versions of the rest)
- Highlight simple repeat-key double-letter ngrams
- Allow selection between indentation styles in case auto-detection doesn't work
- Add an options dialog
- Save stats in a database of some kind (DuckDB or Polars/Parquet). Do maximum potential WPM including all chars and navigation (backspace, del, arrows, etc.). Do an accuracy based correct / a total of chars (but not nav here). Do WPM as it's done now (net WPM to type the correct promp).
- Better visualizations of speed and accuracy
- Plots and analysis of stats in some form
- Make an installer
- Interface directly with project Gutenberg?
- Ebook formats?
- Dark mode
- Make forward/back and font up/down buttons prettier
- Graphic representation of keys in key mode
- Add line numbers for code files
- Add tab style and size to status bar for code