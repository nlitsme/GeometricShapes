polar
=====

A python module for converting between cartesian and polar/spherical coordinates in any number of dimensions.

There are several conventions to choose from:

| dimension  | name  | parameters |
| ---------- | ----- | ---------- |
|    2-d     | polar | r, phi     |
|    3-d     | spherical | r, theta, phi |
|    n-d     | n-spherical | r, phi1, phi2 .. phi[n-1] |

Two dimensions
==============

    r == 0 -> by convention use phi == 0
    r != 0 -> 0 <= phi < 2\*PI

    x = r * cos(phi)
    y = r * sin(phi)

    r = sqrt(x^2 + y^2)
    phi = atan2(y,x)

Three dimensions
================

    r==0 -> by convention: phi == theta == 0
    r!=0 -> 0<=theta<2\*PI, 0<=phi<=PI

    x = r * sin(phi) * cos(theta)
    y = r * sin(phi) * sin(theta)
    z = r * cos(phi)

    r = sqrt(x^2+y^2+z^2)
    phi = arccos(z/r)
    theta = atan2(y,x)

More dimensions
===============

    x1 = r * cos(phi1)
    x2 = r * sin(phi1) * cos(phi2)
    x3 = r * sin(phi1) * sin(phi2) * cos(phi3)
    ...
    x[i] = r * prod(sin(phi[j]), j=1..i-1) * cos(phi[i])
    ...
    x[n-1] = r * prod(sin(phi[j]), j=1..n-2) * cos(phi[n-1])
    x[n] = r * prod(sin(phi[j]), j=1..n-1)

note: when we add a dummy variable phi[n+1] == 0, the formula's become even more uniform.


(helper function)

    r[i] = sqrt(sum(x[j]^2, j=i..n))

    r = r[1]
    phi1 = arccos(x1/r[1])
    phi2 = arccos(x2/r[2])
    ...
    phi[i] = arccos(x[i]/r[i])
    ...
    phi[n-1] = arccos(x[n-1]/r[n-1]) for x[n]>=0
             = 2*PI - arccos(x[n-1]/r[n-1])  for x[n] < 0

