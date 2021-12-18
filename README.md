![logo](https://github.com/mdoege/PyPaint/raw/master/logo.png "PyPaint logo")

## PyPaint

A simple Python program for basic drawing and doodling

Requires PyGame

### Main features

* Fixed canvas size (1200x800 px)
* Only three drawing tools: pen, airbrush, and fill
* Palette of 10 colors (default) or 16 colors (PICO-8 palette)
* No undo (but you can overpaint in white)
* No output filename or file format selection

### Usage

    python pypaint.py [input image]

Paint with the mouse. Change active color with the mouse wheel
(see colored square in top left corner).

#### Keys

P: Switch to the PICO-8 palette

T: Switch drawing tools

Space: Erase drawing

Return: Save as PNG in current directory (Filename is date plus time.)

