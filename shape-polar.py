""" for all platonic shapes, dump coordinates using named constants """
from __future__ import division, print_function
from geometry.base import Point
from geometry.names import namednumber
from geometry.platonic import Tetraeder, Cube, Octaeder, Dodecaeder, Icosaeder, Cell24, Cell120, Cell600


def namedpt(p):
    """ convert point to list of named constants """
    if isinstance(p, Point):
        p = p.coord
    return [namednumber(x) for x in p]


def dumppolar(dim, cls):
    """ dump named points and polar representations of shape """
    center = Point(0 for _ in range(dim))
    count = 0
    for pt in cls.generatePoints(dim):
        center += pt
        count += 1
    center /= count
    print("center = %.16f" % center.coord[0], namedpt(center), cls)
    for pt in cls.generatePoints(dim):
        pt -= center
        print("%-40s -- %-40s" % (namedpt(pt), namedpt(pt.toNSpherical())))

for d in range(2,8):
    dumppolar(d,Tetraeder)

dumppolar(2,Tetraeder)
dumppolar(2,Cube)
dumppolar(2,Octaeder)

dumppolar(3,Tetraeder)
dumppolar(3,Cube)
dumppolar(3,Octaeder)
dumppolar(3,Dodecaeder)
dumppolar(3,Icosaeder)


dumppolar(4,Tetraeder)
dumppolar(4,Cube)
dumppolar(4,Octaeder)
dumppolar(4,Cell24)
dumppolar(4,Cell120)
dumppolar(4,Cell600)
