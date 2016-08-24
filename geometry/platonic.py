"""
Generate the platonic solids.

Copyright (C) 2016 Willem Hengeveld <itsme@xs4all.nl>
"""
from __future__ import division, print_function
import math
from geometry.base import Point


class Tetraeder(object):
    """
    Generate n-tetraeder points and line segments.

    Alternative names:
      2d: triangle
      4d: simplex

    See https://en.wikipedia.org/wiki/Simplex
    """
    def __init__(self, p0):
        """ construct n-tetraeder starting from point p0 """
        self.points = []
        self.p0 = p0
        for p in self.generatePoints(p0.dim()):
            self.points.append(p+p0)

    def dim(self):
        """ return dimension of our space """
        return self.p0.dim()

    @staticmethod
    def generatePoints(dim):
        """ generate base points for n-tetraeder """

        CENTER = (1.0+dim+math.sqrt(1.0+dim))/((1.0+dim)*dim)

        p0= Point(CENTER for _ in range(dim))

        # first points along axis
        for i in range(dim):
            yield Point(1 if i==j else 0 for j in range(dim))-p0
        # and a single point at equal distance from others
        yield Point((1+math.sqrt(dim+1))/dim  for j in range(dim))-p0

    def generateLines(self):
        """
        Enumerate the line segments for the n-tetraeder.
        The line segments of a tetraeder form a complete graph,
        so all combinations of points make a line segment.
        """
        for a in range(0, self.dim()+1):
            for b in range(a):
                yield a, b


class Cube(object):
    """
    Generate n-cube points and line segments

    Alternative names:
      2d cube: square
      4d cube: tesseract, hypercube.

    See https://en.wikipedia.org/wiki/Hypercube
    """
    def __init__(self, p0):
        """ construct n-cube starting from point p0 """
        self.points = []
        self.p0 = p0
        for p in self.generatePoints(p0.dim()):
            self.points.append(p+p0)

    def dim(self):
        """ return dimension of our space """
        return self.p0.dim()

    @staticmethod
    def generatePoints(dim):
        """
        Generate base points for n-cube.

        Each point is assigned a binary number,
        the bits form the coordinates.
        """
        def bit(x,i):
            return -1.0 if x&(1<<i) else 1.0
        for i in range(1<<dim):
            yield Point(bit(i,j)*0.5 for j in range(dim))

    def generateLines(self):
        """ 
        Enumerate the line segments for the n-cube.
        Each line is yielded as a pair of point indices.

        Each point has a binary number assigned to it,
        Each linesegment is between two points differing by only 1 bit.

        """
        for a in range(1, 1<<self.dim()):
            for b in range(a):
                if Cube.areConnected(a, b):
                    yield a, b

    @staticmethod
    def areConnected(a, b):
        """ determine if 2 points are connected based on index """
        x = a^b
        if x==0:
            return False

        # this test ( x & (x-1) ==0 ) is true when x == 2^n

        x &= x-1
        return x==0


class Octaeder(object):
    """
    Generate n-octaeder points and line segments.

    Alternative names:
      4d : cross polytope

    See https://en.wikipedia.org/wiki/Cross-polytope
    """
    def __init__(self, p0):
        """ construct n-octaeder starting from point p0 """
        self.points = []
        self.p0 = p0
        for p in self.generatePoints(p0.dim()):
            self.points.append(p+p0)

    def dim(self):
        """ return dimension of our space """
        return self.p0.dim()

    @staticmethod
    def generatePoints(dim):
        """
        Generate base points for n-octaeder

        The points are the set of +1, -1  points on each axis.

        Points are yielded such that p[2*i] and p[2*i+1] are on the
        same axis.
        """
        for i in range(dim):
            yield Point(1 if i==j else 0 for j in range(dim))
            yield Point(-1 if i==j else 0 for j in range(dim))

    def generateLines(self):
        """ 
        Enumerate the line segments for the n-octaeder.

        points are connected when they are not on the same axis.

        """
        for a in range(0, 2*self.dim()-1):
            for b in range(a+1, 2*self.dim()):
                # skip pair on same axis.
                if a^b!=1:
                    yield a, b


class Dodecaeder(object):
    """
    Generate dodecaeder points and line segments

    This object exists only in three dimensions.


    See https://en.wikipedia.org/wiki/Dodecahedron
    """
    def __init__(self, p0):
        """ construct dodecaeder starting from point p0 """
        assert(p0.dim()==3)
        self.points = []
        self.p0 = p0
        for p in self.generatePoints(p0.dim()):
            self.points.append(p+p0)

    def dim(self):
        """ return dimension of our space """
        return self.p0.dim()

    @staticmethod
    def generatePoints(dim):
        """ generate base points for dodecaeder """
        pm = (-1, 1)
        PHI=(1+math.sqrt(5))/2
        phi = [0, 1/PHI, PHI]

        for i in range(8):
            yield Point(pm[(i>>j)&1] for j in range(3))
        for j in range(3):
            for i in range(4):
                yield Point(pm[(i>>((k+j-1)%3))&1]*phi[(k+j)%3] for k in range(3))

    def generateLines(self):
        """ Enumerate the line segments for the dodecaeder """
        EDGELEN = 4/(1+math.sqrt(5))

        # basically brute forcing lines, as those points which are
        # EDGELEN distant from each other.
        for a in range(1, 20):
            for b in range(0, a):
                if abs(self.points[a].distance(self.points[b]) - EDGELEN) < 0.001:
                    yield a, b


class Icosaeder(object):
    """
    Generate icosaeder points and line segments.
     
    This object exists only in three dimensions.

    See https://en.wikipedia.org/wiki/Icosahedron
    """
    def __init__(self, p0):
        """ construct icosaeder starting from point p0 """
        assert(p0.dim()==3)
        self.points = []
        self.p0 = p0
        for p in self.generatePoints(p0.dim()):
            self.points.append(p+p0)

    def dim(self):
        """ return dimension of our space """
        return self.p0.dim()

    @staticmethod
    def generatePoints(dim):
        """ generate base points for icosaeder """
        pm = (-0.5, 0.5)
        PHI=(1+math.sqrt(5))/2
        phi = [0, 1.0, PHI]

        for j in range(3):
            for i in range(4):
                yield Point(pm[(i>>((k+j-1)%3))&1]*phi[(k+j)%3] for k in range(3))

    def generateLines(self):
        """ Enumerate the line segments for the icosaeder """
        EDGELEN = 1.0

        # basically brute forcing lines, as those points which are
        # EDGELEN distant from each other.
        for a in range(1, 12):
            for b in range(0, a):
                if abs(self.points[a].distance(self.points[b]) - EDGELEN) < 0.001:
                    yield a, b


class Cell24(object):
    """

    See https://en.wikipedia.org/wiki/24-cell
    """
    def __init__(self, p0):
        """ construct 24-cell starting from point p0 """
        assert(p0.dim()==4)
        self.points = []
        self.p0 = p0
        for p in self.generatePoints(p0.dim()):
            self.points.append(p+p0)

    def dim(self):
        """ return dimension of our space """
        return self.p0.dim()


    @staticmethod
    def generatePoints1(dim):
        assert(dim==4)
        def bit(x,i):
            return -1.0 if x&(1<<i) else 1.0

        # (0,0,0,1)                -> 4 * 2
        for i in range(4):
            for b in range(2):
                yield Point(bit(b,0) if i==j else 0 for j in range(4))

        # (0.5,0.5,0.5,0.5)        -> 1 * 16
        for i in range(16):
            yield Point(0.5*bit(i,j) for j in range(4))

    @staticmethod
    def generatePoints(dim):
        assert(dim==4)
        def bit(x,i):
            return -1.0 if x&(1<<i) else 1.0

        # (1,1,0,0)                -> 4 * 6
        for a in range(1,4):
            for b in range(a):
                for i in range(4):
                    p= [0 for _ in range(4)]
                    p[a]= bit(i,0)/math.sqrt(2.0)
                    p[b]= bit(i,1)/math.sqrt(2.0)
                    yield Point(p)

    def generateLines(self):
        """ Enumerate the line segments for the 24-cell """
        EDGELEN = 1.0

        # basically brute forcing lines, as those points which are
        # EDGELEN distant from each other.
        for a in range(1, 24):
            for b in range(0, a):
                if abs(self.points[a].distance(self.points[b]) - EDGELEN) < 0.001:
                    yield a, b



class Cell120(object):
    """


    See https://en.wikipedia.org/wiki/120-cell
    """
    def __init__(self, p0):
        """ construct 120-cell starting from point p0 """
        assert(p0.dim()==4)
        self.points = []
        self.p0 = p0
        for p in self.generatePoints(p0.dim()):
            self.points.append(p+p0)

    def dim(self):
        """ return dimension of our space """
        return self.p0.dim()


    @staticmethod
    def generatePoints(dim):
        assert(dim==4)
        SQ5 = math.sqrt(5.0)
        PHI = (1.0+SQ5)/2.0

        def bit(x,i):
            return -1.0 if x&(1<<i) else 1.0

        # perms of:
        #  0022 0202 0220 2020 2200 2002
        # (0,0,2, 2)             -> 4*6
        for a in range(1,4):
            for b in range(a):
                for i in range(4):
                    p= [0 for _ in range(4)]
                    p[a]= 2.0*bit(i,0)
                    p[b]= 2.0*bit(i,1)
                    yield Point(p)

        #  0001 0010 0100 1000
        # (1,1,1,SQ5)            -> 16*4
        # (PHI**-2, PHI,PHI,PHI) -> 16*4
        # (PHI**-1, PHI**-1,PHI**-1, PHI**2)  -> 16*4
        for a in range(16):
            for i in range(4):
                yield Point(bit(a,j)*(SQ5 if i==j else 1.0) for j in range(4))
                yield Point(bit(a,j)*(PHI**-2 if i==j else PHI) for j in range(4))
                yield Point(bit(a,j)*(PHI**2 if i==j else PHI**-1) for j in range(4))

        # even perms of:
        # 0123 0231 0312 1032 1203 1320 2013 2130 2301 3021 3102 3210
        # (0, PHI**-2, 1, PHI**2)  -> 12*8
        # (0, PHI**-1, PHI, SQ5)   -> 12*8
        # (PHI**-1, 1, PHI, 2)     -> 12*16
        for a in range(16):
            p0= (0, bit(a,2)*PHI**-2, bit(a,1), bit(a,0)*PHI**2)
            p1= (0, bit(a,2)*PHI**-1, bit(a,1)*PHI, bit(a,0)*SQ5)
            p2= (bit(a,3)*PHI**-1, bit(a,2), bit(a,1)*PHI, bit(a,0)*2.0)
            for perm in ( (0,1,2,3), (0,2,3,1), (0,3,1,2), (1,0,3,2), (1,2,0,3), (1,3,2,0), (2,0,1,3), (2,1,3,0), (2,3,0,1), (3,0,2,1), (3,1,0,2), (3,2,1,0)):
                if a<8:
                    yield Point(p0[perm[0]], p0[perm[1]], p0[perm[2]], p0[perm[3]])
                    yield Point(p1[perm[0]], p1[perm[1]], p1[perm[2]], p1[perm[3]])
                yield Point(p2[perm[0]], p2[perm[1]], p2[perm[2]], p2[perm[3]])


    def generateLines(self):
        """ Enumerate the line segments for the 120-cell """
        EDGELEN = 3.0-math.sqrt(5.0)

        # basically brute forcing lines, as those points which are
        # EDGELEN distant from each other.
        for a in range(1, 600):
            for b in range(0, a):
                if abs(self.points[a].distance(self.points[b]) - EDGELEN) < 0.001:
                    yield a, b


class Cell600(object):
    """
    See https://en.wikipedia.org/wiki/600-cell
    """
    def __init__(self, p0):
        """ construct 600-cell starting from point p0 """
        assert(p0.dim()==4)
        self.points = []
        self.p0 = p0
        for p in self.generatePoints(p0.dim()):
            self.points.append(p+p0)

    def dim(self):
        """ return dimension of our space """
        return self.p0.dim()


    @staticmethod
    def generatePoints(dim):
        assert(dim==4)
        SQ5 = math.sqrt(5.0)
        PHI = (1.0+SQ5)/2.0

        def bit(x,i):
            return -1.0 if x&(1<<i) else 1.0

        # (0.5,0.5,0.5,0.5)        -> 1 * 16
        for i in range(16):
            yield Point(0.5*bit(i,j) for j in range(4))

        # (0,0,0,1)                -> 4 * 2
        for i in range(4):
            for b in range(2):
                yield Point(bit(b,0) if i==j else 0 for j in range(4))

        # even perms of:
        # (PHI, 1, 1/PHI, 0)/2     -> 12 * 8
        for a in range(8):
            p0= (0, bit(a,2)*PHI/2.0, bit(a,1)/2.0, bit(a,0)/2.0/PHI)
            for perm in ( (0,1,2,3), (0,2,3,1), (0,3,1,2), (1,0,3,2), (1,2,0,3), (1,3,2,0), (2,0,1,3), (2,1,3,0), (2,3,0,1), (3,0,2,1), (3,1,0,2), (3,2,1,0)):
                yield Point(p0[perm[0]], p0[perm[1]], p0[perm[2]], p0[perm[3]])

    def generateLines(self):
        """ Enumerate the line segments for the 600-cell """
        PHI = (1.0+math.sqrt(5.0))/2.0
        EDGELEN = 1.0/PHI

        # basically brute forcing lines, as those points which are
        # EDGELEN distant from each other.
        for a in range(1, 120):
            for b in range(0, a):
                if abs(self.points[a].distance(self.points[b]) - EDGELEN) < 0.001:
                    yield a, b




import unittest
class TestShape(unittest.TestCase):
    """ tests shapes """
    def test_all(self):
        """ test properties of all 2,3 and 4d shapes """
        self.doshape(Tetraeder, 3, 4, 6, math.sqrt(2))
        self.doshape(Cube,      3, 8, 12, 1.0)
        self.doshape(Octaeder,  3, 6, 12, math.sqrt(2))

        # dodecaeder and icosaeder only exist in 3-d
        self.doshape(Dodecaeder,3, 20, 30, 4/(1+math.sqrt(5)))
        self.doshape(Icosaeder, 3, 12, 30, 1.0)

        #  dim -> binom(dim+1, 1) points
        #  dim -> binom(dim+1, 2) lines
        self.doshape(Tetraeder, 4, 5, 10, math.sqrt(2))
        self.doshape(Tetraeder, 2, 3, 3, math.sqrt(2))
        self.doshape(Tetraeder, 1, 2, 1, math.sqrt(2))

        self.doshape(Cube, 4, 16, 32, 1.0)
        self.doshape(Cube, 2, 4, 4, 1.0)
        self.doshape(Cube, 1, 2, 1, 1.0)

        self.doshape(Octaeder, 4,  8, 24, math.sqrt(2))
        self.doshape(Octaeder, 2,  4,  4, math.sqrt(2))
        #self.doshape(Octaeder, 1,  2,  1, math.sqrt(2))


        self.doshape(Cell24,  4, 24, 96, 1.0)
        self.doshape(Cell120, 4, 600, 1200, 3.0-math.sqrt(5.0))
        self.doshape(Cell600, 4, 120, 720, 2.0/(1+math.sqrt(5.0)))

    def doshape(self, cls, dim, npoints, nlines, edgelen):
        """ count nr points, lines, edge size for shape """
        t = cls(Point(0 for x in range(dim)))
        self.assertEqual(len(t.points), npoints)
        count = 0
        for a, b in t.generateLines():
            count += 1
            self.assertAlmostEqual(t.points[a].distance(t.points[b]), edgelen)
        self.assertEqual(count, nlines)


if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
