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


shapegraphs
===========

Tool for generating a `.dot` graph showing how the points, edges, faces, 3d-volumes, etc are interdependent
for Cubes, Tetrahedrons and Octahedrons of any dimension.

Each graph generator has:
 * a method `partname` for generating sensible labels for the points, edges, faces, etc.
 * a method `makeparts` for generating the parameters needed for `partname` of a given sub dimension.
 * a method `containspart` which tells if a _m_ dimensional part contains the _m-1_ dimensional subpart


AUTHOR
======

Willem Hengeveld <itsme@xs4all.nl>
