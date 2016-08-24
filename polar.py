"""
functions for converting between cartesian and spherical coordinates

 * 2d : Polar
 * 3d : Spherical
 * n-d: NSpherical

Copyright (C) 2016 Willem Hengeveld <itsme@xs4all.nl>

"""


from __future__ import division, print_function
import math
import random

#############################################################################


def torad(deg):
    """ convert degrees to radians """
    return math.pi/180.0*deg


def todeg(rad):
    """ convert radians to degrees """
    return 180.0/math.pi*rad


#############################################################################
#  2d: https://en.wikipedia.org/wiki/Polar_coordinate_system
#  (r, phi) = ( sqrt(x^2+y^2), atan2(y,x) ), phi=-pi .. pi
#  (x,y)    = ( r*cos(phi), r*sin(phi) )
def fromPolar(r, phi):
    """ convert polar coordinates to 2-d cartesian coordinates """
    return r*math.cos(phi), r*math.sin(phi)


def toPolar(p):
    """ convert 2-d cartesian coordinates to polar coordinates """
    x, y = p
    return math.sqrt(x**2+y**2), math.atan2(y, x)


import unittest
class TestPolar(unittest.TestCase):
    """ test cases for polar coordinate conversion """
    def assertAngleEqual(self, a, b):
        """ angles compare equal modulo 2*PI """
        x = abs(a-b)
        x -= 360.0 * int((x+180)/360)
        self.assertAlmostEqual(x, 0)

    def test_step(self):
        """ test angles with step of 30 degrees """
        for phi in range(-180, 180, 30):
            self._test(phi)

    def test_random(self):
        """ test with random values """
        for _ in range(100):
            phi = random.uniform(-180, 180)
            self._test(phi)

    def _test(self, phi0):
        """ handle the actual test """
        p = fromPolar(1.0, torad(phi0))
        r, phi = toPolar(p)
        self.assertAlmostEqual(r, 1.0)
        self.assertAlmostEqual(todeg(phi), phi0)


#############################################################################
#  3d: https://en.wikipedia.org/wiki/Spherical_coordinate_system
#  (r,theta(inclination),phi(azimuth)) = ( sqrt(x^2+y^2+z^2), arccos(z/r), atan2(y,x) )
#  (x,y,z) = ( r*sin(theta)*cos(phi), r*sin(theta)*sin(phi), r*cos(theta) )
def fromSpherical(r, theta, phi):
    """ convert spherical coordinates to 3-d cartesian coordinates """
    return r*math.sin(theta)*math.cos(phi), r*math.sin(theta)*math.sin(phi), r*math.cos(theta)


def toSpherical(p):
    """ convert 3-d cartesian coordinates to spherical coordinates """
    x, y, z = p
    r = math.sqrt(x**2+y**2+z**2)
    if r:
        return r, math.acos(z/r), math.atan2(y, x)
    else:
        return 0, 0, 0


class TestSpherical(unittest.TestCase):
    """ test cases for spherical coordinate conversion """
    def assertAngleEqual(self, a, b):
        """ angles compare equal modulo 2*PI """
        x = abs(a-b)
        x -= 360.0 * int((x+180)/360)
        self.assertAlmostEqual(x, 0)

    def test_step(self):
        """ test angles with step of 30 degrees """
        for the in range(0, 180, 30):
            for phi in range(-180, 180, 30):
                self._test(the, phi)

    def test_random(self):
        """ test with random values """
        for _ in range(100):
            the = random.uniform(0, 180)
            phi = random.uniform(-180, 180)
            self._test(the, phi)

    def _test(self, the0, phi0):
        """ handle the actual test """
        p = fromSpherical(1.0, torad(the0), torad(phi0))
        r, theta, phi = toSpherical(p)
        self.assertAlmostEqual(r, 1.0)
        self.assertAngleEqual(todeg(theta), the0)
        if theta:
            self.assertAngleEqual(todeg(phi), phi0)


#############################################################################
#  n-d: https://en.wikipedia.org/wiki/N-sphere#Spherical_coordinates
#
#  r_j = sqrt(sum(x_i^2), i=j..n)
#  (r,phi1, phi...) = ( r_1, arccos(x1/r_1), arccos(x2/r_2), ...)  =  ( r_1, arccot(x1/r_2), arccot(x2/r_3), ...)
#  (x,...) = (r * cos(phi_1), r*sin(phi_1)* [....] )
#
# x1= r*cos(phi1)
# x2= r*sin(phi1)*cos(phi2)
# x3= r*sin(phi1)*sin(phi2)*cos(phi3)
# ...
# x[n-2] = r*sin(phi1)* ... sin(phi[n-3])*cos(phi[n-2])
# x[n-1] = r*sin(phi1)* ... sin(phi[n-3])*sin(phi[n-2])*cos(phi[n-1])
# x[n]   = r*sin(phi1)* ... sin(phi[n-3])*sin(phi[n-2])*sin(phi[n-1])
def fromNSpherical(r, *phi):
    """ convert n-spherical coordinates to n-d cartesian coordinates """
    theta = phi[0]
    if len(phi) == 1:
        return (r*math.cos(theta), r*math.sin(theta))

    return (r*math.cos(theta), ) + tuple(r*math.sin(theta)*x for x in fromNSpherical(1.0, *phi[1:]))

# phi1 = arccos(x1/r)
# phi2 = arccos(x2/(r*sin(phi1))) = arccos(x2/sqrt(r^2-x1^2))
# phi3 = arccos(x3/(r*sin(phi1)*sin(phi2)))
# ...
# phi[n-1] = atan2(x[n], x[n-1])


# .. x[n-1]/x[n-2] = tan(phi[n-2]) * cos(phi[n-1])
def toNSpherical(p):
    """ convert n-d cartesian coordinates to n-spherical coordinates """
    def invNSpherical(p):
        """ recursively convert to spherical """
        if len(p) == 2:
            return (math.atan2(p[1], p[0]), )
        r = math.sqrt(sum(x**2 for x in p))
        return (0 if r==0 else math.acos(p[0]/r), ) + invNSpherical(p[1:])
    r = math.sqrt(sum(x**2 for x in p))
    return (r, ) + invNSpherical(p)


def getNformula(r, n):
    """ generate string representation of fromNSperical formula """
    rr = "" if r==1 else "r*"
    if n <= 1:
        return (rr+"cos(p0)", rr+"sin(p0)")

    return (rr+"cos(p%d)" % (n-1), ) + tuple(rr+"sin(p%d)*%s" % (n-1, x) for x in getNformula(1.0, n-1))


class TestNSpherical(unittest.TestCase):
    """ test cases for n-spherical coordinate conversion """
    def assertAngleEqual(self, a, b):
        """ angles compare equal modulo 2*PI """
        x = abs(a-b)
        x -= 360.0 * int((x+180)/360)
        self.assertAlmostEqual(x, 0, places=6)

    def test_step(self):
        """ test with all 4-d angles in 30 degree steps """
        for a in range(30, 180, 30):
            for b in range(30, 180, 30):
                for c in range(0, 360, 30):
                    self._test(a, b, c)

    def test_random(self):
        """ test with random 4d points values """
        for _ in range(100):
            self._test(*tuple(random.uniform(0, 180) for x in range(3)) + (random.uniform(-180, 180), ))

    def test_random_n(self):
        """ test with random dimensions values """
        for i in range(200):
            self._test(*tuple(random.uniform(0, 180) for x in range(2+int(i/10))) + (random.uniform(-180, 180), ))

    def _test(self, *phi):
        """ handle the actual test """
        p = fromNSpherical(1.0, *(torad(x) for x in phi))
        r_phi = toNSpherical(p)
        self.assertAlmostEqual(r_phi[0], 1.0)
        for phi1, phi0 in zip(r_phi[1:], phi):
            self.assertAngleEqual(todeg(phi1), phi0)


class TestConversions(unittest.TestCase):
    """ unit tests comparing n-spherical to polar and (3)spherical """
    def assertAngleEqual(self, a, b):
        """ angles compare equal modulo 2*PI """
        x = abs(a-b)
        x -= 360.0 * int((x+180)/360)
        self.assertAlmostEqual(x, 0)

    def testPolarNSp(self):
        """ polar and nsphere are encoded identically """
        for phi in range(-180, 180, 30):
            r, phi1 = toNSpherical(fromPolar(1.0, torad(phi)))
            self.assertAlmostEqual(todeg(phi1), phi)
            self.assertAlmostEqual(r, 1.0)

    def testSphereNSp(self):
        """ nsphere and sphere coord need a swap """
        def aaa(sp):
            """ convert between (normal-3) spherical and n-spherical """
            r, the, phi = sp
            return r, the, math.pi/2-phi

        def xyz(p):
            """ coordinate swap to convert between n and 3 spherical """
            return p[2], p[1], p[0]

        for the in range(0, 180, 30):
            for phi in range(-180, 180, 30) if the else (0,):
                r, the1, phi1 = aaa(toNSpherical(xyz(fromSpherical(1.0, torad(the), torad(phi)))))
                self.assertAngleEqual(todeg(the1), the)
                self.assertAlmostEqual(r, 1.0)
                if the:
                    self.assertAngleEqual(todeg(phi1), phi)


if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
