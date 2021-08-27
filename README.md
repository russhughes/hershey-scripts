# hershey-scripts: Hershey font file conversion scripts

Here are the python scripts and data files I used to convert Hershey font files for use in my projects. The Hershey data is public domain and my scripts are MIT Licensed.

## Directories

### fonts directory
The `fonts` directory contains the results of running the `map_to_fnt.py` script. The `fnt` files are a compact binary representation of each of the Hershey fonts for use in my [TurtlePlotBot](https://github.com/russhughes/turtleplotbot3) series of projects.


### hershey directory
The `hershey` directory contains the hershey font data in the original USENET shell archive as well as the de-archived files.


### images directory
The `images` directory contains SVG images of the `fnt` files created using the `fnt_to_svg.py` script.


### pyfont directory
The `pyfont` directory contains the results of running the `map_to_py.py` script. The `py` files are python modules representing each of the Hershey fonts used in my [TurtlePlotBot](https://github.com/russhughes/turtleplotbot3) series of projects as well as my forks of the [st7789](https://github.com/russhughes/st7789_mpy), [ili9342c](https://github.com/russhughes/ili9342c_mpy) and [gc9a01](https://github.com/russhughes/gc9a01py) MicroPython display drivers.

## Python Scripts

### map-to-fnt.py
Python script used to read Hershey data and hmp files to create DrawBot fnt files.


### map-to-py.py
Python script used to read Hershey data and hmp files to create python font modules.


### fnt_to_svg.py
Python script to create SVG images from DrawBot fnt files

