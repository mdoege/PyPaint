## PyPaint

![screenshot](screenshot.png "PyPaint screenshot")

A simple Python painting program for basic drawing and doodling. It is inspired by DeluxePaint and similar 1980s paint software.

Requires PyGame

### Main features

* Fixed canvas size (1200x800 px), but can load pictures in other sizes. (Images larger than the canvas are scaled down to fit.)
* Drawing tools: pen (dotted and continuous), straight lines, quadratic Bézier curves, airbrush, and flood fill
* Several included palettes
* Single-level undo
* Saves files as PNG with automatic filename selection based on the current date (YMD) and time

### Usage

    python pypaint.py [input image]

#### Mouse

* Paint with the left mouse button
* Change active color with the mouse wheel or by clicking on the palette
* Switch to next tool with the right mouse button
* Middle mouse button click toggles brush size between large and small

#### Keyboard

* **P**: Switch to different ***p***alette
* **T**: Switch drawing ***t***ool
* **B**: Toggle ***b***rush size (large/small)
* **M**: Toggle text ***m***arker / highlighter mode: The dotted pen and airbrush tools now only affect background color pixels, effectively drawing behind other colors on the canvas. This mode is also toggled by clicking on the dotted pen/airbrush icons. (This highlighter mode is similar to using a stencil in DeluxePaint.)
* **U**: ***U***ndo last painting operation
* **H**: ***H***ide palette
* **C**: ***C***olor picker: Picks the currently active color from the pixel under the mouse cursor.
If that color is not found in the current palette, it will be appended. Note that these palette changes are not saved permanently. The empty palette is particularly useful for picking colors from an image.
* **Space**: Erase drawing (can be undone)
* **Return**: Save as PNG in current directory (filename based on date and time)

### License

Public Domain / CC0
