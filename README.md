python geometry module
======================

Currently has module for generating the points and line segments of the platonic solids, in 3 and more dimensions.

The modules are expected to live in a subdirectory named `geometry`.

USAGE
=====

Each shape has a method for generating points, and one for generating linesegments.

Most modules when executed as a script, will run some unittests:

    PYTHONPATH=. python geometry/base.py


qtcube
======

`qtcube.py` is a tool which demonstrates how to draw 3d objects using several drawing libraries:

| commandline | action
| ----------- | -------------
| --matlib | draw a 3d scene using matplotlib
| --cube   | draw a 3d scene using the PySide Qt library
| --pygame | draw a 3d scene using the PyGame library

The qt and pygame versions use a simple Slider and Checkbox which might not look like
Slider and checkbox... It's the dashed lines, and the square box.


AUTHOR
======

Willem Hengeveld <itsme@xs4all.nl>
