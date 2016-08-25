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



class graphbase:
    """
    Baseclass for the graph generators.
    each subclass must implement the following methods:
     * makeparts(m)
        - generator which yields the part parameters for parts of dimension `m`
          points have m=0, lines have m=1, faces have m=2, etc.

     * partname(m, part) 
        - generate a sensible name for the part.
     * containspart(part, subpart)
         - returns true when the m dimensional part contains the m-1
           dimensional subpart
     * name
         - a class property
    """

    def __init__(self, n):
        """ init the shape with the dimension of the space """
        self.n = n

    def writedot(self):
        print("graph %s {" % self.name)
        print("{ node[shape=plaintext];")
        print("%s;" % "--".join(itemname(x)+"s" for x in range(self.n+1)))
        print("}")
        print("node[shape=box];")

        # first put points, lines, etc in their respective rank
        for m in range(self.n+1):
            print("{ rank=same; %s;" % (itemname(m)+"s"))
            # emit points, lines, ...
            for part in self.makeparts(m):
                print("%s;" % self.partname(m, part), end="")
            print("}")

        # now emit dependencies
        for m in range(0, self.n+1):
            for part in self.makeparts(m+1):
                deps = []
                for subpart in self.makeparts(m):
                    if self.containspart(part, subpart):
                        deps.append(self.partname(m, subpart))
                print("%s -- %s;" % ( self.partname(m+1, part), ",".join(deps)))
            
        print("}")




class ncubegraph(graphbase):
    name = "NCube"
    # 2^(n-m) * binom(n, m)  m-dimensional parts in n-dimensional cube
    def makeparts(self, m):
        # return m dimensional sub part of n-cube
        #  m==0 -> point,  m==1 -> line, ...
        for bits in itertools.combinations(range(self.n), m):
            mask = sum(1<<x for x in bits) ^ (2**self.n-1)

            for i in range(2**(self.n-m)):
                value = 0
                for j in range(self.n):
                    if mask&(1<<j):
                        if i&1:
                            value |= 1<<j
                        i >>= 1
                yield mask, value
    def partname(self, m, part):
        mask, value = part
        suffix = ""
        for i in range(self.n):
            if mask&1:
                suffix += str(value&1)
            else:
                suffix += 'x'
            mask >>= 1
            value >>= 1
        return itemname(m)+suffix[::-1]
    def containspart(self, part, subpart):
        mask,value = part
        submask,subvalue = subpart
        return submask&mask == mask and subvalue&mask == value


class ntetragraph(graphbase):
    name = "NTetra"
    # binom(n+1, m+1)  m-dimensional parts in n-dimensional tetraeder
    def makeparts(self, m):
        # return m dimensional sub part of n-tetra
        #  m==0 -> point,  m==1 -> line, ...
        for part in itertools.combinations(range(self.n+1), m+1):
            yield sum(1<<x for x in part)
    def partname(self, m, part):
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
        for i in range(self.n+1):
            if part&(1<<i):
                suffix += xxx(i)
        return itemname(m)+suffix
    def containspart(self, part, subpart):
        return part&subpart==subpart


class noctagraph(graphbase):
    name = "NOcta"
    # 2^(m+1) * binom(n, m+1)  m-dimensional parts in n-dimensional tetraeder
    def makeparts(self, m):
        # return m dimensional sub part of n-octa
        #  m==0 -> point,  m==1 -> line, ...
        if m==self.n:
            yield 0, 0
            return
        for bits in itertools.combinations(range(self.n), m+1):
            for i in range(2**(m+1)):
                value = 0
                mask = 0
                for bit in bits:
                    mask |= 1<<bit
                    if i&1:
                        value |= 1<<bit
                    i>>=1
                yield mask, value
    def partname(self, m, part):
        mask, value = part
        def xxx(x, b):
            if x<26:
                if b:
                    return chr(65+x)
                else:
                    return chr(97+x)
            x -= 26
            return "?"
        suffix = ""
        for i in range(self.n):
            if mask&(1<<i):
                suffix += xxx(i, value&(1<<i))
        return itemname(m)+suffix
    def containspart(self, part, subpart):
        mask,value = part
        submask,subvalue = subpart
        return mask==value==0 or (submask&mask == submask and value&submask == subvalue)


parser = argparse.ArgumentParser(description='Draw shape dependency graphs: which face contains on which lines, etc.')
parser.add_argument('--dim', type=int)
parser.add_argument('--cube', action='store_true')
parser.add_argument('--tetra', action='store_true')
parser.add_argument('--octa', action='store_true')
args = parser.parse_args()

if args.dim is None:
    args.dim = 3

if args.cube:
    ncubegraph(args.dim).writedot()
elif args.tetra:
    ntetragraph(args.dim).writedot()
elif args.octa:
    noctagraph(args.dim).writedot()
