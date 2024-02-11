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

    # Time complexity: O(1)
    @staticmethod
    def calculate_slope(point1: QPointF, point2: QPointF):
        return (point2.y() - point1.y()) / (point2.x() - point1.x())

    # Time complexity: O(1)
    def sort_points_clockwise(self, points, hull_size):
        if hull_size == 2:
            return points  # the points are already sorted in clockwise order
        elif hull_size == 3:
            # sort points in clockwise order
            slope_12 = self.calculate_slope(points[0], points[1])
            slope_13 = self.calculate_slope(points[0], points[2])

            if slope_12 > slope_13:
                return points
            return [points[0], points[2], points[1]]

    # Time complexity: O(|hull|)
    @staticmethod
    def get_rightmost_index(hull: [QPointF]):
        highest_x = -1.1
        highest_index = -1
        for i, point in enumerate(hull):
            if point.x() >= highest_x:
                highest_x = point.x()
                highest_index = i

        return highest_index

    # Time complexity: O(1)
    @staticmethod
    def wrap_next_index(index, length):
        return (index + 1) % length

    # Time complexity: O(1)
    @staticmethod
    def wrap_prev_index(index, length):
        return (index - 1) % length

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
        hull = self._generate_hull(points)

        # generate the outline for the GUI
        polygon = []
        for i, point in enumerate(hull[1:]):
            polygon.append(QLineF(hull[i], point))
        polygon.append(QLineF(hull[-1], hull[0]))
        return polygon


    # Time Complexity O(|points| * log(|points|)
    def _generate_hull(self, points: [QPointF]):
        # Time complexity: O(1)
        hull_size = len(points)
        if hull_size in (2, 3):
            return self.sort_points_clockwise(points, hull_size)

        # Time complexity: O(points)
        midpoint = hull_size // 2
        left_hull = points[:midpoint]
        right_hull = points[midpoint:]

        # Time complexity: O(log(points))
        left_hull = self._generate_hull(left_hull)
        right_hull = self._generate_hull(right_hull)

        # Time complexity: O(|points|)
        return self.combine_hulls(left_hull, right_hull)

    # Time Complexity: O(|left_hull| + |right_hull|)
    def combine_hulls(self, left_hull, right_hull):
        # Time complexity: O(|left_hull|)
        index_l = self.get_rightmost_index(left_hull) # starting index for the left hull
        index_r = 0 # starting index for the right hull (it's always zero)

        # these are used when we need to wrap around to the start of a list
        len_left = len(left_hull)
        len_right = len(right_hull)

        # find the indexes of the points that make up the upper tangent
        upper_left_i, upper_right_i = self.upper_tangent(left_hull, right_hull, index_l, index_r, len_left, len_right)

        # find the indexes of the points that make up the lower tangent
        lower_left_i, lower_right_i = self.lower_tangent(left_hull, right_hull, index_l, index_r, len_left, len_right)


        return self.remove_inner_points(left_hull, right_hull, upper_left_i, upper_right_i, lower_left_i, lower_right_i)

    # Time complexity: O(|left_hull| + |right_hull|)
    def upper_tangent(self, left_hull, right_hull, left_index, right_index, mod_l, mod_r):
        current_slope = self.calculate_slope(left_hull[left_index], right_hull[right_index])

        done = False
        while not done:
            done = True

            # the right side
            while True:
                next_right_index = self.wrap_next_index(right_index, mod_r)
                new_slope = self.calculate_slope(left_hull[left_index], right_hull[next_right_index])
                if new_slope < current_slope:
                    break
                current_slope = new_slope
                right_index = self.wrap_next_index(right_index, mod_r)
                done = False

            # the left side
            while True:
                next_left_index = self.wrap_prev_index(left_index, mod_l)
                new_slope = self.calculate_slope(left_hull[next_left_index], right_hull[right_index])
                if new_slope > current_slope:
                    break
                current_slope = new_slope
                left_index = self.wrap_prev_index(left_index, mod_l)
                done = False

        return left_index, right_index

    # Time complexity: O(|left_hull| + |right_hull|)
    def lower_tangent(self, left_hull, right_hull, left_index, right_index, mod_l, mod_r):
        current_slope = self.calculate_slope(left_hull[left_index], right_hull[right_index])
        # Time complexity: O()
        done = False
        while not done:
            done = True

            # the left side
            while True:
                next_left_index = self.wrap_next_index(left_index, mod_l)
                new_slope = self.calculate_slope(left_hull[next_left_index], right_hull[right_index])
                if new_slope < current_slope:
                    break
                current_slope = new_slope
                left_index = self.wrap_next_index(left_index, mod_l)
                done = False

            # the right side
            while True:
                next_right_index = self.wrap_prev_index(right_index, mod_r)
                new_slope = self.calculate_slope(left_hull[left_index], right_hull[next_right_index])
                if new_slope > current_slope:
                    break
                current_slope = new_slope
                right_index = self.wrap_prev_index(right_index, mod_r)
                done = False

        return left_index, right_index

    # Time complexity: O(|left_hull| + |right_hull|)
    @staticmethod
    def remove_inner_points(left_hull, right_hull, upper_left_i, upper_right_i, lower_left_i, lower_right_i):
        first = left_hull[:upper_left_i + 1]

        if lower_right_i > upper_right_i:
            second = right_hull[upper_right_i: lower_right_i + 1]
        elif lower_right_i == upper_right_i:
            second = [right_hull[upper_right_i]]
        else:
            second = right_hull[upper_right_i:] + right_hull[:lower_right_i + 1]

        if lower_left_i == 0:
            return first + second

        third = left_hull[lower_left_i:]

        return first + second + third
