import random
import time
from PyQt6.QtCore import QLineF, QPointF, QObject

from convex_hull import ConvexHullSolver

random.seed(time.time())

ptlist = []
unique_xvals = {}
max_r = 0.98
WIDTH = 1.0
HEIGHT = 1.0
npoints = 12
while len(ptlist) < npoints:
    x = random.uniform(-1.0, 1.0)
    y = random.uniform(-1.0, 1.0)
    if x ** 2 + y ** 2 <= max_r ** 2:
        xval = WIDTH * x
        yval = HEIGHT * y
        if not xval in unique_xvals:
            ptlist.append(QPointF(xval, yval))
            unique_xvals[xval] = 1

ConvexHullSolver().compute_hull(ptlist, False, None)