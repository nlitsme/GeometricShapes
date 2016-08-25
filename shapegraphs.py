""" Generate shape dependency graphs for n-cube, n-tetraeder, n-octaeder """
from __future__ import division, print_function
import argparse
import itertools

def itemname(n):
    """ Return nice name for the different parts of a shape """
    names = ["point", "line", "face", "shape"]
    if n<len(names):
        return names[n]
    return "_%d_" % n

def ncubegraph(n):
    # 2^(n-m) * binom(n,m)  m-dimensional parts in n-dimensional cube
    def cubepart(m):
        # return m dimensional sub part of n-cube
        #  m==0 -> point,  m==1 -> line, ...
        for bits in itertools.combinations(range(n), m):
            mask = sum(1<<x for x in bits) ^ (2**n-1)

            for i in range(2**(n-m)):
                value = 0
                for j in range(n):
                    if mask&(1<<j):
                        if i&1:
                            value |= 1<<j
                        i >>= 1
                yield mask, value
    def partname(m, mask, value):
        suffix = ""
        for i in range(n):
            if mask&1:
                suffix += str(value&1)
            else:
                suffix += 'x'
            mask >>= 1
            value >>= 1
        return itemname(m)+suffix[::-1]
    print("graph NCube {")
    print("{ node[shape=plaintext];")
    print("%s;" % "--".join(itemname(x)+"s" for x in range(n+1)))
    print("}")
    print("node[shape=box];")

    # first put points, lines, etc in their respective rank
    for m in range(n+1):
        print("{ rank=same; %s;" % (itemname(m)+"s"))
        # emit points, lines, ...
        for mask, value in cubepart(m):
            print("%s;"%partname(m, mask, value), end="")
        print("}")

    # now emit dependencies
    for m in range(1,n+1):
        for mask, value in cubepart(m):
            deps = []
            for submask, subvalue in cubepart(m-1):
                if submask&mask == mask and \
                        subvalue&mask == value:
                    deps.append(partname(m-1, submask, subvalue))
            print("%s -- %s;" % ( partname(m, mask, value), ",".join(deps)))
        
    print("}")

def ntetragraph(n):
    # binom(n+1, m+1)  m-dimensional parts in n-dimensional tetraeder
    def tetrapart(m):
        # return m dimensional sub part of n-tetra
        #  m==0 -> point,  m==1 -> line, ...
        for part in itertools.combinations(range(n+1), m+1):
            yield sum(1<<x for x in part)
    def partname(m, mask):
        def xxx(x):
            if x<26:
                return chr(65+x)
            x -= 26
            if x<26:
                return chr(97+x)
            x -= 26
            if x<10:
                return chr(48+x)
            x -= 10

            return "?"
        suffix = ""
        for i in range(n+1):
            if mask&(1<<i):
                suffix += xxx(i)
        return itemname(m)+suffix

    print("graph NTetra {")
    print("{ node[shape=plaintext];")
    print("%s;" % "--".join(itemname(x)+"s" for x in range(n+1)))
    print("}")
    print("node[shape=box];")
    # first put points, lines, etc in their respective rank
    for m in range(n+1):
        print("{ rank=same; %s;" % (itemname(m)+"s"))
        # emit points, lines, ...
        for part in tetrapart(m):
            print("%s;"%partname(m,part), end="")
        print("}")

    # now emit dependencies
    for m in range(0,n+1):
        for mask in tetrapart(m+1):
            deps = []
            for submask in tetrapart(m):
                if mask&submask==submask:
                    deps.append(partname(m, submask))
            print("%s -- %s;" % ( partname(m+1, mask), ",".join(deps)))
        
    print("}")


def noctagraph(n):
    # 2^(m+1) * binom(n, m+1)  m-dimensional parts in n-dimensional tetraeder
    def octapart(m):
        # return m dimensional sub part of n-octa
        #  m==0 -> point,  m==1 -> line, ...
        if m==n:
            yield 0,0
            return
        for bits in itertools.combinations(range(n), m+1):
            for i in range(2**(m+1)):
                value = 0
                mask = 0
                for bit in bits:
                    mask |= 1<<bit
                    if i&1:
                        value |= 1<<bit
                    i>>=1
                yield mask, value
    def partname(m, mask, value):
        def xxx(x, b):
            if x<26:
                if b:
                    return chr(65+x)
                else:
                    return chr(97+x)
            x -= 26
            return "?"
        suffix = ""
        for i in range(n):
            if mask&(1<<i):
                suffix += xxx(i, value&(1<<i))
        return itemname(m)+suffix

    print("graph NOcta {")
    print("{ node[shape=plaintext];")
    print("%s;" % "--".join(itemname(x)+"s" for x in range(n+1)))
    print("}")
    print("node[shape=box];")
    # first put points, lines, etc in their respective rank
    for m in range(n+1):
        print("{ rank=same; %s;" % (itemname(m)+"s"))
        # emit points, lines, ...
        for mask,value in octapart(m):
            print("%s;"%partname(m, mask,value), end="")
        print("}")

    # now emit dependencies
    for m in range(0,n+1):
        for mask,value in octapart(m+1):
            deps = []
            for submask,subvalue in octapart(m):
                if mask==value==0 or (submask&mask == submask and value&submask == subvalue):
                    deps.append(partname(m, submask, subvalue))
            print("%s -- %s;" % ( partname(m+1, mask, value), ",".join(deps)))
        
    print("}")


parser = argparse.ArgumentParser(description='Draw shape dependency graphs: which face contains on which lines, etc.')
parser.add_argument('--dim', type=int)
parser.add_argument('--cube', action='store_true')
parser.add_argument('--tetra', action='store_true')
parser.add_argument('--octa', action='store_true')
args = parser.parse_args()

if args.dim is None:
    args.dim = 3

if args.cube:
    ncubegraph(args.dim)
elif args.tetra:
    ntetragraph(args.dim)
elif args.octa:
    noctagraph(args.dim)
