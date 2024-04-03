import numpy as np
import heapq

from TSPClasses import City
class Matrix:
    def __init__(self, dimension=1, cities=[], matrix=np.array([])):
        # create the matrix
        if matrix.any():
            self.matrix = matrix
        else:
            self.matrix: np.array = np.full((dimension, dimension), np.inf)

            # set the initial costs
            for i, city_src in enumerate(cities):
                for j, city_dest in enumerate(cities):
                    if i != j:
                        cost_to = city_src.costTo(city_dest)
                        if cost_to < np.inf:
                            self.matrix[i][j] = cost_to

    def update_cost(self, src_index, dest_index, new_cost):
        self.matrix[src_index][dest_index] = new_cost

    def reduce_row(self):
        min_values = np.min(self.matrix, axis=1, keepdims=1)
        min_values[np.isinf(min_values)] = 0  # Replace np.inf with 0
        self.matrix = self.matrix - min_values
        return np.sum(min_values)

    def reduce_column(self):
        min_values = np.min(self.matrix, axis=0, keepdims=1)
        min_values[np.isinf(min_values)] = 0  # Replace np.inf with 0
        self.matrix = self.matrix - min_values
        return np.sum(min_values)

    def get_cost(self, city_src: int, city_dest: int):
        return self.matrix[city_src][city_dest]

    def reduce_matrix(self):
        return self.reduce_row() + self.reduce_column()

    def update(self, row_index, column_index):
        # gets the cost from one city to another before setting the corresponding row and column to infinity
        cost = self.matrix[row_index][column_index]
        self.set_row_to_infinity(row_index)
        self.set_column_to_infinity(column_index)
        self.matrix[column_index][row_index] = np.inf
        return cost

    def set_row_to_infinity(self, row_index):
        self.matrix[row_index, :] = np.inf

    def set_column_to_infinity(self, column_index):
        self.matrix[:, column_index] = np.inf

    def copy(self):
        return Matrix(matrix=self.matrix.copy())

    def __repr__(self):
        return str(self.matrix)



#
# arr = np.array([[np.inf, 10, 15, 20],
#                 [10, np.inf, 35, 25],
#                 [15, 35, np.inf, 30],
#                 [20, 25, 30, np.inf]])
#
#
# best_cost = 90
# num_cities = 4
# matrix = Matrix(matrix=arr)
#
# # first reduce
# lower_bound = matrix.reduce_matrix()
#
# # pick a start node and set the cost to the lower bound
# priority_queue = []
# heapq.heappush(priority_queue, ([0], lower_bound, matrix))
#
# num_solutions = 0
# while priority_queue:
#     route = heapq.heappop(priority_queue)
#     current_path, current_cost, matrix = route
#
#     if len(current_path) == num_cities:
#         num_solutions += 1
#         if current_cost < best_cost:
#             best_path = current_path
#             best_cost = current_cost
#     else:
#         for next_city in range(num_cities):
#             if next_city not in current_path:
#                 matrix_copy = matrix.copy()
#
#                 next_cost = matrix_copy.update(current_path[-1], next_city)
#
#                 reduced_cost = matrix_copy.reduce_matrix()
#
#                 updated_path_cost = next_cost + reduced_cost + current_cost
#
#                 if updated_path_cost <= best_cost:
#                     heapq.heappush(priority_queue, (current_path + [next_city], updated_path_cost, matrix_copy))
#
# print(best_cost, best_path, num_solutions)


# for each node that you can go out of the current node
    # set the current node row = inf and next node column = inf
    # set the position at matrix[next_node][current] = inf
    # reduce the matrix again
    # the cost from current node to next node is current cost + reduction cost + distance from current to next







