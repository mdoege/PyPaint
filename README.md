![logo](https://github.com/mdoege/PyPaint/raw/master/logo.png "PyPaint logo")

## PyPaint

A simple Python program for basic drawing and doodling

Requires PyGame and NumPy

### Main features

* Fixed canvas size (1200x800 px)
* Only four drawing tools: pen (dotted and continuous), airbrush, and fill
* Palette of 10 colors (default) or 17 colors (PICO-8 palette + white)
* No undo (but you can overpaint in white)
* No output filename or file format selection

### Usage

    python pypaint.py [input image]

Paint with the mouse. Change active color with the mouse wheel
(see colored square in top left corner).

#### Keys

**P**: Switch to PICO-8 palette

**T**: Switch drawing tools

**Space**: Erase drawing

**Return**: Save as PNG in current directory (Filename is date plus time.)

