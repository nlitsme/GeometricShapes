""" display platonic shapes using various python graphics libraries """
from __future__ import division, print_function
import math

from geometry.base import *
from geometry.platonic import *
from geometry.other import *
from geometry.polar import *

################# controls for use with qt #######################

class Toggle:
    def __init__(self, pt):
        self.pt = pt
        self.state = False
    def rect(self):
        return (self.pt-(7.5,7.5)).coord+(15,15)
    def contains(self, pt):
        return self.pt.distance(pt)<8

class Slider:
    def __init__(self, p1, p2):
        self.line = Line(p1, p2)
        self.cur = 0.5
    def current(self):
        return self.line.pointForParams(self.cur)
    def update(self, pt):
        self.cur = self.line.paramsForPoint(pt)


class Sphere(object):
    def __init__(self, origin, radius):
        self.origin = origin
        self.radius = radius

    def dim(self):
        return self.origin.dim()


class Axis(object):
    def __init__(self, dim):
        self.points = []
        self._dim = dim
        for i in range(dim):
            self.points.append(Point(-10 if j==i else 0 for j in range(dim)))
            self.points.append(Point(10 if j==i else 0 for j in range(dim)))

    def dim(self):
        return self._dim

    def generateLines(self):
        for i in range(self.dim()):
            yield 2*i, 2*i+1

################# 3d display using qt #######################

def runqt3d():
    from PySide import QtGui, QtCore
    class CubeView(QtGui.QWidget):
        def __init__(self):
            super(CubeView, self).__init__()

            self.captured = None
            
            self.defineObjects()

            self.setGeometry(300, 300, 640, 480)
            self.setWindowTitle('cube')
            self.show()
            self.raise_()

        def defineObjects(self):
            self.cube = Cube(Point(0,0,1))
            self.tetra = Tetraeder(Point(0,1,0))
            self.octa = Octaeder(Point(1,0,0))
            self.dode = Dodecaeder(Point(1,1,1))
            self.ico = Icosaeder(Point(2,2,2))
            self.axis = Axis(3)

            # set in drawItems
            self.viewport = None
            self.viewpoint = None

            self.toggle = Toggle(Point(100,100))
            self.sl1 = Slider(Point(100, 10), Point(200, 10))  # viewpoint distance
            self.sl2 = Slider(Point(100, 20), Point(200, 20))  # viewport distance
            self.sl3 = Slider(Point(100, 30), Point(200, 30))  # viewpoint rho
            self.sl4 = Slider(Point(100, 40), Point(200, 40))  # viewpoint phi

        def mouseReleaseEvent(self, e):
            if self.captured:
                self.captured.update(Point(e.x(), e.y()))
                self.update()
                self.captured = None
                return
            if self.toggle.contains(Point(e.x(), e.y())):
                self.toggle.state = not self.toggle.state
                self.update()
        def mousePressEvent(self, e):
            self.captured = None
            for o in [self.sl1, self.sl2, self.sl3, self.sl4]:
                if o.current().distance(Point(e.x(), e.y()))<5:
                    self.captured = o
                    return
        def mouseMoveEvent(self, e):
            if self.captured:
                self.captured.update(Point(e.x(), e.y()))
                self.update()
            

        def paintEvent(self, e):
            qp = QtGui.QPainter()
            qp.begin(self)
            self.drawItems(qp)
            qp.end()

        @staticmethod
        def qpt(*arg):
            if len(arg)==1 and isinstance(arg[0], Point):
                return CubeView.qpt(arg[0].x, arg[0].y)
            if len(arg)==2:
                if abs(arg[0])<100000 and abs(arg[1])<100000:
                    return QtCore.QPoint(100+arg[0]*50,400-arg[1]*50)
                return QtCore.QPoint(0,0)

        @staticmethod
        def pt(*arg):
            if len(arg)==1 and isinstance(arg[0], Point):
                return CubeView.pt(arg[0].x, arg[0].y)
            if len(arg)==2:
                return QtCore.QPoint(arg[0],arg[1])

        def drawItems(self, qp):
            vp = self.viewpoint = Point.PointFromNSpherical(5*(1.0+self.sl1.cur), self.sl3.cur, self.sl4.cur)
            p1 = Point(-vp.y,vp.x,0)
            p2 = Point(0,-vp.z,vp.y)
            #p2 = p1.cross(vp)
            self.viewport = Parallelogram.fromPointAndVectors(vp*self.sl2.cur, p1, p2)
            self.drawObject(qp, self.axis, QtCore.Qt.gray)
            self.drawObject(qp, self.cube, QtCore.Qt.red)
            self.drawObject(qp, self.tetra, QtCore.Qt.green)
            self.drawObject(qp, self.octa, QtCore.Qt.blue)
            self.drawObject(qp, self.dode, QtCore.Qt.cyan)
            self.drawObject(qp, self.ico, QtCore.Qt.cyan)

            self.drawToggle(qp, self.toggle)
            self.drawSlider(qp, self.sl1, "vp distance")
            self.drawSlider(qp, self.sl2, "port distance")
            self.drawSlider(qp, self.sl3, "latitude")   # elevation, -90 .. 90
            self.drawSlider(qp, self.sl4, "longitude")  # azimuth, -180 .. 180

        def projectOnView(self, pt):
            if self.toggle.state:
                # todo -- this gives the wrong result
                return Point(self.viewport.projectionParams(pt))
            else:
                return Point(self.viewport.intersectionParams(Line(pt, self.viewpoint)))

        def drawObject(self, qp, obj, color):
            for a,b in obj.generateLines():
                self.drawLine(qp, self.projectOnView(obj.points[a]), self.projectOnView(obj.points[b]), color)

        def drawDot(self, qp, p):
            qp.fillRect(QtCore.QRect(self.qpt(p), QtCore.QSize(2,2)), QtCore.Qt.blue)
        def drawLine(self, qp, p1, p2, color):
            qp.setPen(color)
            qp.drawLine(self.qpt(p1), self.qpt(p2))

        def drawToggle(self, qp, t):
            if t.state:
                qp.fillRect(QtCore.QRect(*t.rect()), QtCore.Qt.black)
            else:
                qp.setPen(QtCore.Qt.black)
                qp.drawRect(QtCore.QRect(*t.rect()))

        def drawSlider(self, qp, s, desc):
            qp.setPen(QtCore.Qt.black)
            qp.drawLine(self.pt(s.line.p1), self.pt(s.line.p2))
            qp.drawText(self.pt(s.line.p2), desc)

            pt = s.current()
            qp.setPen(QtCore.Qt.blue)
            qp.drawLine(self.pt(pt-Point(0,10)), self.pt(pt+Point(0,10)))

    app = QtGui.QApplication([])
    ex = CubeView()
    app.exec_()

################# 2d display using qt #######################

def runqt2d():
    from PySide import QtGui, QtCore
    class LinesView(QtGui.QWidget):
        # 2-d variant of CubeView
        def __init__(self):
            super(LinesView, self).__init__()
            
            self.defineObjects()

            self.setGeometry(300, 300, 640, 480)
            self.setWindowTitle('lines')
            self.show()
            self.raise_()

        def defineObjects(self):
            self.axis = Axis(2)
            self.pgm = Parallelogram(Point(1,1), Point(2,4), Point(5,2))
            self.pt = Point(3,3)

        def paintEvent(self, e):
            qp = QtGui.QPainter()
            qp.begin(self)
            self.drawItems(qp)
            qp.end()

        @staticmethod
        def qpt(*arg):
            if len(arg)==1 and isinstance(arg[0], Point):
                return LinesView.qpt(arg[0].x, arg[0].y)
            if len(arg)==2:
                if abs(arg[0])<100000 and abs(arg[1])<100000:
                    return QtCore.QPoint(100+arg[0]*50,400-arg[1]*50)
                return QtCore.QPoint(0,0)

        def drawItems(self, qp):
            for a,b in self.pgm.generateLines():
                self.drawLine(qp, self.pgm.points[a], self.pgm.points[b], QtCore.Qt.black)

            self.drawDot(qp, self.pt)
            a,b = self.pgm.paramsForPoint(self.pt)
            pab = self.pgm.pointForParams(a,b)

            l1 = Line(self.pgm.p1, self.pgm.p2)
            l2 = Line(self.pgm.p1, self.pgm.p3)

            pa = l1.pointForParams(a)
            pb = l2.pointForParams(b)
            self.drawDot(qp, pa) ; self.drawLine(qp, self.pt, pa, QtCore.Qt.red)
            self.drawDot(qp, pb) ; self.drawLine(qp, self.pt, pb, QtCore.Qt.red)
            self.drawDot(qp, pab)

            a = l1.projectionParams(self.pt)
            b = l2.projectionParams(self.pt)

            pa = l1.pointForParams(a)
            pb = l2.pointForParams(b)
            self.drawDot(qp, pa) ; self.drawLine(qp, self.pt, pa, QtCore.Qt.green)
            self.drawDot(qp, pb) ; self.drawLine(qp, self.pt, pb, QtCore.Qt.green)
            self.drawDot(qp, pab)

            for a,b in self.axis.generateLines():
                self.drawLine(qp, self.axis.points[a], self.axis.points[b], QtCore.Qt.gray)

        def drawDot(self, qp, p):
            qp.fillRect(QtCore.QRect(self.qpt(p), QtCore.QSize(2,2)), QtCore.Qt.blue)
        def drawLine(self, qp, p1, p2, color):
            qp.setPen(color)
            qp.drawLine(self.qpt(p1), self.qpt(p2))

    app = QtGui.QApplication([])
    ex = LinesView()
    app.exec_()

################# display using pygame #######################

def rungame():
    import pygame
    class PygameView:
        BLACK = (  0,   0,   0)
        WHITE = (255, 255, 255)
        BLUE  = (  0,   0, 255)
        GREEN = (  0, 255,   0)
        RED   = (255,   0,   0)
        GRAY  = (128, 128, 128)
        CYAN  = (  0, 255, 255)


        def __init__(self):
            pygame.init()
            pygame.font.init()

            self.defineObjects()

            self.screen = pygame.display.set_mode((640,480), pygame.RESIZABLE)
        def run(self):
            clock = pygame.time.Clock()
            done = False

            grabbed_item = None

            # list of items which can be 'grabbed' - the slider positions.
            grababels = [self.sl1, self.sl2]

            while not done:
                clock.tick(10)

                for event in pygame.event.get(): # User did something
                    if event.type == pygame.KEYUP:
                        if event.dict['key']==113 and event.dict['mod']&0xc00:
                            # Cmd-q
                            done = True
                    if event.type == pygame.QUIT: # If user clicked close
                        done = True # Flag that we are done so we exit this loop
                    elif event.type == pygame.VIDEORESIZE:
                        self.screen = pygame.display.set_mode(event.dict['size'], pygame.RESIZABLE)
                    elif event.type == pygame.MOUSEBUTTONUP:
                        if grabbed_item:
                            grabbed_item.update(Point(event.pos))
                            grabbed_item = None
                        elif self.toggle.contains(event.pos):
                            self.toggle.state = not self.toggle.state
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        for p in grababels:
                            if p.current().distance(Point(event.pos))<3:
                                grabbed_item = p
                                break
                    elif event.type == pygame.MOUSEMOTION:
                        if grabbed_item:
                            grabbed_item.update(Point(event.pos))

                # All drawing code happens after the for loop and but
                # inside the main while done==False loop.

                # Clear the screen and set the screen background
                self.screen.fill(PygameView.WHITE)
                self.drawItems(self.screen)
                pygame.display.flip()

        def defineObjects(self):
            self.cube = Cube(Point(0,0,1))
            self.tetra = Tetraeder(Point(0,0,3))
            self.octa = Octaeder(Point(0,0,5))
            self.dode = Dodecaeder(Point(0,0,8))
            self.ico = Icosaeder(Point(0,4,0))
            self.axis = Axis(3)

            # set in drawItems
            self.viewport = None
            self.viewpoint = None

            # the toggle switches from perspective to non-perspective view.
            self.toggle = Toggle(Point(100,100))
            # the sliders move the viewport and viewpoint
            self.sl1 = Slider(Point(10, 10), Point(110, 10))
            self.sl2 = Slider(Point(10, 20), Point(110, 20))

        @staticmethod
        def qpt(*arg):
            if len(arg)==1 and isinstance(arg[0], Point):
                return PygameView.qpt(arg[0].x, arg[0].y)
            if len(arg)==2:
                if abs(arg[0])<100000 and abs(arg[1])<100000:
                    return (100+arg[0]*50,400-arg[1]*50)
                return (0,0)

        @staticmethod
        def pt(*arg):
            if len(arg)==1 and isinstance(arg[0], Point):
                return arg[0].coord
            return arg

        def drawItems(self, qp):
            self.viewpoint = Point(5,5,5)*(1.0+self.sl1.cur)
            self.viewport = Parallelogram.fromPointAndVectors(Point(4,4,4)*(1.0+self.sl2.cur), Point(-1,-1,1), Point(1,-1,-1))
            self.drawObject(qp, self.axis,  PygameView.GRAY)
            self.drawObject(qp, self.cube,  PygameView.RED)
            self.drawObject(qp, self.tetra, PygameView.GREEN)
            self.drawObject(qp, self.octa,  PygameView.BLUE)
            self.drawObject(qp, self.dode,  PygameView.CYAN)
            self.drawObject(qp, self.ico,   PygameView.CYAN)

            self.drawToggle(qp, self.toggle)
            self.drawSlider(qp, self.sl1)
            self.drawSlider(qp, self.sl2)

        def projectOnView(self, pt):
            # transform 3d coord to 2d
            if self.toggle.state:
                return Point(self.viewport.projectionParams(pt))
            else:
                return Point(self.viewport.intersectionParams(Line(pt, self.viewpoint)))

        def drawObject(self, qp, obj, color):
            for a,b in obj.generateLines():
                self.drawLine(qp, self.projectOnView(obj.points[a]), self.projectOnView(obj.points[b]), color)

        ## primitive drawing functions
        def drawDot(self, qp, p):
            pygame.draw.rect(qp, PygameView.BLUE, [p.x-1, p.y-1,3,3], 0)
        def drawLine(self, qp, p1, p2, color):
            pygame.draw.line(qp, color, self.qpt(p1), self.qpt(p2), 1)

        def drawToggle(self, qp, t):
            if t.state:
                pygame.draw.rect(qp, PygameView.BLUE, t.rect(), 0)
            else:
                pygame.draw.rect(qp, PygameView.BLUE, t.rect(), 2)

        def drawSlider(self, qp, s):
            pygame.draw.line(qp, PygameView.BLACK, self.pt(s.line.p1), self.pt(s.line.p2), 1)

            pt = s.current()
            pygame.draw.line(qp, PygameView.BLUE, self.pt(pt-Point(0,10)), self.pt(pt+Point(0,10)), 1)
    PygameView().run()


################# display using matplotlib #######################

class MatplotView:
    # similar to CubeView, but using matplotlib
    # in this case the 3d view is rendered by matplotlib
    def __init__(self):

        # first define several objects, each with a position at which they are to be displayed.
        self.aa = Axis(3)
        self.c = Cube(Point(0,0,1))
        self.t = Tetraeder(Point(0,0,3))
        self.o = Octaeder(Point(0,0,5))
        self.d = Dodecaeder(Point(0,0,8))
        self.i = Icosaeder(Point(0,4,0))
        self.sphere = Sphere(Point(4,0,0), 2.0)

        # the viewport
        self.cp = Point(4,4,4)
        self.v = Parallelogram.fromPointAndVectors(self.cp, Point(-1,-1,2), Point(1,-1,0))
        # and the view point
        self.vp = Point(8,8,8)


    def drawLine(self, ax, p, q):
        ax.plot((p.x, q.x), (p.y, q.y), (p.z, q.z))
    def drawObject(self, ax, obj):
        for p in obj.points:
            ax.scatter(p.x, p.y, p.z, c='r', marker='o')
        for a,b in obj.generateLines():
            self.drawLine(ax, obj.points[a], obj.points[b])

    def drawSphere(self, ax, s):
        for phi in range(0,180,15):
            lx, ly, lz = [], [], []
            for rho in range(0,360,15):
                # first inner loop var, then outer loop var: meridians are drawn
                p = s.origin+Point.PointFromNSpherical(s.radius, rho*math.pi/180, phi*math.pi/180)
                lx.append(p.x) ; ly.append(p.y) ; lz.append(p.z)

            lx.append(lx[0]) ; ly.append(ly[0]) ; lz.append(lz[0])
            ax.plot(lx, ly, lz)

        for phi in range(0,180,15):
            lx, ly, lz = [], [], []
            for rho in range(0,360,15):
                # first outer loop var, then inner loop var: parallels of sphere are drawn
                p = s.origin+Point.PointFromNSpherical(s.radius, phi*math.pi/180, rho*math.pi/180)
                lx.append(p.x) ; ly.append(p.y) ; lz.append(p.z)

            lx.append(lx[0]) ; ly.append(ly[0]) ; lz.append(lz[0])
            ax.plot(lx, ly, lz)


    def pickevent(self, e):
        print("picked", e.artist)
    def display(self):
        from mpl_toolkits.mplot3d import Axes3D
        import matplotlib.pyplot as plt
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        self.drawObject(ax, self.c)
        self.drawObject(ax, self.v)
        self.drawObject(ax, self.aa)
        self.drawObject(ax, self.t)
        self.drawObject(ax, self.o)
        self.drawObject(ax, self.d)
        self.drawObject(ax, self.i)

        # draw lines from the viewport to two specific points
        # showing how the perspective and non-perspective views are constructed.
        p1 = self.v.pointForParams(*self.v.intersectionParams(Line(Point(0,0,0), self.vp)))
        p2 = self.v.pointForParams(*self.v.intersectionParams(Line(Point(0,1,1), self.vp)))
        self.drawLine(ax, Point(0,0,0), p1)
        self.drawLine(ax, Point(0,1,1), p2)

        q1 = self.v.pointForParams(*self.v.projectionParams(Point(0,0,0)))
        q2 = self.v.pointForParams(*self.v.projectionParams(Point(0,1,1)))
        self.drawLine(ax, Point(0,0,0), q1)
        self.drawLine(ax, Point(0,1,1), q2)

        self.drawSphere(ax, self.sphere)

        for p in [self.vp, self.cp, p1, p2]:
            ax.scatter(p.x, p.y, p.z, c='b', marker='^', picker=5)

        ax.set_xlabel('X Label')
        ax.set_ylabel('Y Label')
        ax.set_zlabel('Z Label')

        fig.canvas.mpl_connect('pick_event', self.pickevent)

        plt.show()


def main():
    import argparse
    parser = argparse.ArgumentParser(description='qtcube')
    parser.add_argument('--test', action='store_true')
    parser.add_argument('--cube', action='store_true')
    parser.add_argument('--lines', action='store_true')
    parser.add_argument('--matlib', action='store_true')
    parser.add_argument('--pygame', action='store_true')
    parser.add_argument('--verbose', '-v', action='count')
 
    args = parser.parse_args()

    if args.test:
        import sys
        del sys.argv[1:]
        import unittest
        unittest.main(verbosity=args.verbose)
    elif args.matlib:
        MatplotView().display()
    elif args.pygame:
        rungame()
    elif args.cube:
        runqt3d()
    elif args.lines:
        runqt2d()


if __name__ == '__main__':
    main()
