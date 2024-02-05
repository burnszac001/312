from PyQt6.QtCore import QLineF, QPointF, QObject
import time

# Some global color constants that might be useful
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Global variable that controls the speed of the recursion automation, in seconds
PAUSE = 0.25


#
# This is the class you have to complete.
#
class ConvexHullSolver(QObject):

    # Class constructor
    def __init__(self):
        super().__init__()
        self.view = None
        self.pause = False

    # Some helper methods that make calls to the GUI, allowing us to send updates
    # to be displayed.

    def showTangent(self, line, color):
        self.view.addLines(line, color)
        if self.pause:
            time.sleep(PAUSE)

    def eraseTangent(self, line):
        self.view.clearLines(line)

    def blinkTangent(self, line, color):
        self.showTangent(line, color)
        self.eraseTangent(line)

    def showHull(self, polygon, color):
        self.view.addLines(polygon, color)
        if self.pause:
            time.sleep(PAUSE)

    def eraseHull(self, polygon):
        self.view.clearLines(polygon)

    def showText(self, text):
        self.view.displayStatusText(text)

    # This is the method that gets called by the GUI and actually executes
    # the finding of the hull
    def compute_hull(self, points, pause, view):
        self.pause = pause
        self.view = view
        assert (type(points) is list and type(points[0]) is QPointF)

        t1 = time.time()

        sorted_points = sorted(points, key=lambda point: point.x())  # time complexity: O(nlogn) worst case

        t2 = time.time()

        t3 = time.time()
        
        polygon = self.generate_hull(sorted_points)  # time complexity: O(nlogn) worst case

        t4 = time.time()

        self.showHull(polygon, RED)
        self.showText('Time Elapsed (Convex Hull): {:3.3f} sec'.format(t4 - t3))

    def generate_hull(self, points):
        polygon = []
        self.__generate_hull(points, polygon)
        return polygon

    def __generate_hull(self, points, polygon):
        hull_size = len(points)
        if hull_size in (2, 3):
            if hull_size == 2:
                polygon.extend([QLineF(points[0], points[1])])
            elif hull_size == 3:
                polygon.extend([QLineF(points[0], points[1]), QLineF(points[0], points[2]), QLineF(points[1], points[2])])
            return

        midpoint = hull_size // 2
        left_hull = points[:midpoint]
        right_hull = points[midpoint:]

        self.__generate_hull(left_hull, polygon)
        self.__generate_hull(right_hull, polygon)

        self.combine_hulls(left_hull, right_hull, polygon)

    def combine_hulls(self, left_hull, right_hull, polygon):
        # find upper tangent and add it to the polygon
        self.upper_tangent(left_hull, right_hull, polygon)
        # find lower tangent and add it to the polygon
        self.lower_tangent(left_hull, right_hull, polygon)
        # find all the lines enclosed by upper and lower tangent and remove them from polygon
        self.remove_inner_lines(left_hull, right_hull, polygon)

    def upper_tangent(self, left_hull, right_hull, polygon):
        # The upper tangent is found when a line connecting the two hulls by one point on either side contains all
        # points from both hulls below it.
        # The process for finding this upper tangent is connecting the right most point on the left hull with the left
        # most point on the right hull. If the points on the right side aren't under the line, rotate the point on the
        # right until they are. Same as the left side. Continue until all the points on both side are under the line.

        left_hull_right_point = left_hull[-1]
        right_hull_left_point = right_hull[0]
        temp_line = QLineF(left_hull_right_point, right_hull_left_point)
        done = False

        while not done:
            done = True

    def lower_tangent(self, left_hull, right_hull, polygon):
        pass

    def remove_inner_lines(self, left_hull, right_hull, polygon):
        pass