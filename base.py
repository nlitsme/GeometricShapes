""" module containing basic geometry shapes: Point and Line """
from __future__ import division, print_function
import math
from types import GeneratorType
import numpy as np
from geometry import polar


class Point(object):
    """ represents a Point """
    @staticmethod
    def PointFromNSpherical(r, *phi):
        """ construct point from spherical coordinates """
        return Point(polar.fromNSpherical(r, *phi))

    def toNSpherical(self):
        """ return spherical coordinates """
        return polar.toNSpherical(self.coord)

    def __init__(self, *args):
        """ construct point from list, tuple, generator, point """
        if len(args)==1 and type(args[0])==list:
            self.coord = tuple(args[0])
        elif len(args)==1 and type(args[0])==tuple:
            self.coord = args[0]
        elif len(args)==1 and isinstance(args[0], Point):
            self.coord = args[0].coord
        elif type(args[0])==GeneratorType:
            self.coord = tuple(args[0])
        else:
            self.coord = args

    def __add__(self, rhs):
        """ calculate vector addition """
        if not isinstance(rhs, Point):
            rhs = Point(rhs)
        return Point(x+y for x, y in zip(self.coord, rhs.coord))

    def __radd__(self, lhs):
        """ calculate vector addition """
        return self.__add__(lhs)

    def __sub__(self, rhs):
        """ calculate vector difference """
        if not isinstance(rhs, Point):
            rhs = Point(rhs)
        return Point(x-y for x, y in zip(self.coord, rhs.coord))

    def __truediv__(self, rhs):
        """ calculate vector / scalar """
        return Point(x/rhs for x in self.coord)

    def __div__(self, rhs):
        """ calculate vector / scalar """
        return self.__truediv__(rhs)

    def __mul__(self, rhs):
        """ calculate vector * scalar """
        if isinstance(rhs, Point):
            return self.inner(rhs)
        return Point(x*rhs for x in self.coord)

    def __rmul__(self, lhs):
        """ calculate scalar * vector """
        return self.__mul__(lhs)

    def __eq__(self, rhs):
        """ equality test """
        if not isinstance(rhs, Point):
            rhs = Point(rhs)
        return all(x==y for x, y in zip(self.coord, rhs.coord))

    def __getattr__(self, name):
        """ add properties x,y,z or x0,x1,x2,x3,... to access coordinates """
        if len(name)==1:
            # x, y, z
            i = ord(name[0])-ord('x')
            if not 0 <= i < self.dim():
                raise AttributeError()
            return self.coord[i]
        elif len(name)>1 and name[0]=='x' and '0'<=name[1]<='9':
            # x0, x1, x2, x3, ...
            i = int(name[1:])
            if not 0 <= i < self.dim():
                raise AttributeError()
            return self.coord[i]
        raise AttributeError()

    def __nonzero__(self):
        """ null vecctor is false, any other is true """
        return any(x!=0 for x in self.coord)

    def dim(self):
        """ return dimension of our space """
        return len(self.coord)

    def length(self):
        """ return length of vector """
        return math.sqrt(sum( x**2 for x in self.coord ))

    def distance(self, rhs):
        """ calculate distance of between two points """
        if not isinstance(rhs, Point):
            rhs = Point(rhs)
        return math.sqrt(sum( (x-y)**2 for x, y in zip(self.coord, rhs.coord) ))

    # movable item
    def set(self, rhs):
        """ set coordinates of point to those of rhs """
        if not isinstance(rhs, Point):
            rhs = Point(rhs)
        self.coord = rhs.coord

    def inner(self, rhs):
        """ calc inner product of two vectors """
        return sum( x*y for x, y in zip(self.coord, rhs.coord) )

    def cross(self, rhs):
        """ calc 3-d cross product of two vectors """
        assert(self.dim()==rhs.dim())
        if self.dim()!=3:
            raise Exception("cross product only in 3D")
        u = self
        v = rhs
        return Point(u.y*v.z-u.z*v.y, u.z*v.x-u.x*v.z, u.x*v.y-u.y*v.x)

    def __repr__(self):
        """ return string representation of point """
        return "Point(%s)" % ",".join("%.1f" % x for x in self.coord)


class Line(object):
    """ represents a Line """

    def __init__(self, p1, p2):
        """ constructs a line segment from two point """
        # a line is defined by two points: line = { p1*(1-a)+p2*a,  a in [0..1] }
        #  .. or a vector and a translation

        # x-p1==(p2-p1)*a

        # 2-d case:
        #   (y-y1)*(x2-x1)=(x-x1)*(y2-y1)
        #  x*(y1-y2) + y*(x2-x1)  = y1*x2-x1*y2
        if not isinstance(p1, Point):
            p1 = Point(p1)
        if not isinstance(p2, Point):
            p2 = Point(p2)
        self.p1 = p1
        self.p2 = p2
        assert(self.p1.dim()==self.p2.dim())

    def dim(self):
        """ returns dimension of the space this line segment lives in """
        return self.p1.dim()

    def length(self):
        """ returns the length of this line segment """
        return self.p1.distance(self.p2)

    def angle(self, line):
        """ calculates the angle of between 2 lines """
        # v1.length * v2.length * cos(phi) = inner(v1, v2)

        v1 = self.p2-self.p1
        v2 = line.p2-line.p1
        return math.acos(v1.inner(v2)/v1.length()/v2.length())

    def pointForParams(self, a):
        """ return a point on the line segment """
        # 0<=a<=1 -> point between p1 and p2
        return self.p1+(self.p2-self.p1)*a

    def paramsForPoint(self, pt):
        """ return params for point on line """
        v = self.p2-self.p1
        u = pt-self.p1
        if v.x:
            return u.x/v.x
        elif v.y:
            return u.y/v.y
        else:
            return None

    def vector(self):
        """ return the direction vector for this line """
        return self.p2 - self.p1

    def projectionParams(self, pt):
        """ projects 'pt' on line, returns param """
        if not isinstance(pt, Point):
            pt = Point(pt)
        # calc projection of p1->pt onto  p1->p2
        p = pt-self.p1
        q = self.p2-self.p1

        if q:
            return p.inner(q)/q.inner(q)
        return None


class Parallelogram(object):
    @staticmethod
    def fromPointAndVectors(pt, v1, v2):
        """ construct parallelogram from point, and two vectors """
        p = pt-v1/2-v2/2
        return Parallelogram(p, p+v1, p+v2)

    @staticmethod
    def generateLines():
        """ enumerate all line segments of the parallelogram """
        for a in range(4):
            yield a, (a+1)%4

    # a parallelogram is defined by three points: { p1+(p2-p1)*a+(p3-p1)*b,  a in [0..1], b in [0..1] }
    #  ... or 2 vectors {p2-p1, p3-p1} and a translation point { p1 }

    # plane equation: in 3d:
    # ( (p2-p1) x (p3-p1) ) * (p-p1) == 0

    def __init__(self, p1, p2, p3):
        """ construct parallelogram from three corners, calculating the fourth """
        self.points = [p1, p2, p2+p3-p1, p3]
        assert(p1.dim()==p2.dim()==p3.dim())

    def __getattr__(self, name):
        """ add properties p0, p1, p2, p3 for the edge points of the parallelogram """
        if len(name)>1 and name[0]=='p' and '0'<=name[1]<='9':
            # p0, p1, p2, p3, ...
            i = int(name[1:])
            if 1<=i<=2:
                return self.points[i-1]
            elif i==3:
                return self.points[3]
        print("don't know how to get attr", name)
        raise AttributeError()

    def dim(self):
        """ return dimension of our space """
        return self.p1.dim()

    def circumfence(self):
        """ calculate circumfence of parallelogram """
        a = self.p1.distance(self.p2)
        b = self.p1.distance(self.p3)
        return 2*(a+b)

    def surfacearea(self):
        """ calculate area encllosed by parallelogram """
        a = self.p1.distance(self.p2)
        b = self.p2.distance(self.p3)
        c = self.p3.distance(self.p1)

        # heron's formula ( double area of triangle )
        s = (a+b+c)/2
        return 2.0*math.sqrt(s*(s-a)*(s-b)*(s-c))

    def pointForParams(self, a, b):
        """ return point on plane of parallelogram for params """
        return self.p1+(self.p2-self.p1)*a+(self.p3-self.p1)*b

    def paramsForPoint(self, pt):
        """ calculate params for point in plane """

        #  { p2-p1,  p3-p1 } * {a,b} = { pt-p1 }
        v1 = self.p2-self.p1
        v2 = self.p3-self.p1
        u = pt-self.p1

        #  this way we define cols of matrix, iso rows.
        A = np.column_stack([ v1.coord, v2.coord ])

        AtA = np.dot(np.ma.transpose(A), A)
        Atu = np.dot(np.ma.transpose(A), u.coord)
        ab = np.linalg.solve(AtA, Atu)

        return ab[0], ab[1]

    def perpendicular(self):
        """
        Calculate vector perpendicular to the plane of the parallelogram.
        Only in 3-d
        """
        return (self.p2-self.p1).cross(self.p3-self.p1)

    def intersectionParams(self, obj):
        """
        Calculate intersection point of object with plane of parallelogram
        Currently only for lines.
        """
        if isinstance(obj, Line):
            if self.dim()==3:
                return self.intersectWithLine(obj)
            # todo: implement dim==4 -> result = line
        if isinstance(obj, Parallelogram):
            if self.dim()==4:
                return self.intersectWithPlane(obj)
            # todo: implement dim==3 -> result = line
        raise Exception("not implemented")

    def intersectWithLine(self, line):
        """ calculate intersection point of line with plane of parallelogram """
        # from the equation
        #    self.p1+(self.p2-self.p1)*a+(self.p3-self.p1)*b == line.p1+(line.p2-line.p1)*c

        # solve a,b,c
        #    { (self.p2-self.p1), (self.p3-self.p1),  -(line.p2-line.p1) } * { a,b,c } == {line.p1 - self.p1}

        A = np.matrix([(self.p2-self.p1).coord, (self.p3-self.p1).coord, (line.p1-line.p2).coord]).transpose()
        b = np.matrix((line.p1-self.p1).coord).transpose()

        At = A.transpose()
        AtA = At * A
        Atb = At * b

        try:
            abc = np.linalg.solve(AtA, Atb)
            return abc[0], abc[1]
        except:
            return 0, 0

    def intersectWithPlane(self, plane):
        """ calculate intersection point of plane with plane of parallelogram """

        # todo
        pass

    def projectionParams(self, obj):
        """ project object onto parallelogram, currently only points """
        if isinstance(obj, Point):
            return self.projectPoint(obj)
        print("don't know how to project", obj)
        raise Exception("not implemented")

    def projectPoint(self, pt):
        """ (3d only) project point on parallelogram """

        return self.intersectWithLine(Line(pt, pt+self.perpendicular()))


# todo: add Parallelopiped

import unittest
class TestPointMethods(unittest.TestCase):
    """ tests for point """
    def test_cross(self):
        """ test 3d cross product """
        self.assertEqual(Point(3,-3,1).cross(Point(4,9,2)), (-15,-2,39))

    def test_inner(self):
        """ test 3d inner product """
        self.assertAlmostEqual(Point(3,-3,1).inner(Point(4,9,2)), -13)

    def test_length(self):
        """ test vector length """
        self.assertAlmostEqual(Point(3,-3,1).length(), math.sqrt(19))

    def test_distance(self):
        """ test point distance """
        self.assertAlmostEqual(Point(3,-3,1).distance(Point(4,9,2)), math.sqrt(146))


class TestLineMethods(unittest.TestCase):
    """ tests for line """
    def test_params(self):
        """ test 2d point to params to point conversion """
        l1 = Line(Point(1,1), Point(1,2))
        p1 = Point(1,3)
        a1 = l1.paramsForPoint(p1)
        self.assertEqual(l1.pointForParams(a1), p1)

        l2 = Line(Point(1,1), Point(3,2))
        p2 = Point(5,3)
        a2 = l2.paramsForPoint(p2)
        self.assertEqual(l2.pointForParams(a2), p2)

    def _test_projection(self):
        """ test projection of point on line in 2d """
        l1 = Line(Point(1,1), Point(3,2))
        a = l1.projectionParams(Point(3,3))
        p = l1.pointForParams(a)
        self.assertEqual(p, Point(3.4, 2.2))


class TestRectMethods(unittest.TestCase):
    """ tests for parallelogram """
    def test_params2d(self):
        """ test 2d point to params to point conversion """
        pgm = Parallelogram(Point(1,1), Point(2,4), Point(5,2))
        p1 = Point(3,3)
        a, b = pgm.paramsForPoint(p1)
        self.assertAlmostEqual(p1.distance(pgm.pointForParams(a, b)), 0)

        pa = Line(pgm.p1, pgm.p2).pointForParams(a)
        pb = Line(pgm.p1, pgm.p2).pointForParams(b)
        #todo - self.assertEqual(p1, pa+pb)

    def test_params3d(self):
        """ test 3d point to params to point conversion """
        pgm = Parallelogram.fromPointAndVectors(Point(4,4,4), Point(-1,-1,2), Point(1,-1,0))
        p1 = Point(4,4,4)
        a, b = pgm.paramsForPoint(p1)
        self.assertAlmostEqual(p1.distance(pgm.pointForParams(a, b)), 0)


if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
