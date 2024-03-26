from PyQt6.QtCore import QPointF
import random
import numpy as np
import math


def name_for_int(num):
	if num == 0:
		return ''
	elif num <= 26:
		return chr(ord('A') + num - 1)
	else:
		return nameForInt((num - 1) // 26) + nameForInt((num - 1) % 26 + 1)


class Graph:
    HARD_MODE_FRACTION_TO_REMOVE: float = 0.20  # Remove 20% of the edges

    def __init__(self, locations: [QPointF], difficulty: str, seed: int) -> None:
        self.num_cities: int = len(locations)
        self.difficulty: str = difficulty
        self.seed: int = seed

        self.__cities: dict[str: City] = None
        # self.__edges: set(Edge) = None
        self.__edge_exists_matrix: np.array = (np.ones((self.num_cities, self.num_cities)) - np.diag(
            np.ones((self.num_cities)))) > 0

        self.__create_cities(locations)

        if self.difficulty == "Hard":
            self.__remove_edges()
        elif difficulty == "Hard (Deterministic)":
            self.__remove_edges(deterministic=True)

        self.__create_edges()
    def __create_cities(self, locations: [QPointF]) -> None:
        cities: [City] = None

        if self.difficulty == "Normal" or self.difficulty == "Hard":
            cities = [City(pt.x(), pt.y(), random.uniform(0.0, 1.0)) for pt in locations]
        elif self.difficulty == "Hard (Deterministic)":
            random.seed(self.seed)
            cities = [City(pt.x(), pt.y(), random.uniform(0.0, 1.0)) for pt in locations]
        else:
            cities = [City(pt.x(), pt.y()) for pt in locations]

        for index, city in enumerate(cities):
            city.set_index_and_name(index, name_for_int(index + 1))

        self.__cities = {city.get_name(): city for city in cities}

    def __create_edges(self) -> None:
        for i, row in enumerate(self.__edge_exists_matrix):
            for j, column in enumerate(self.__edge_exists_matrix):
                if self.__edge_exists_matrix[i][j]:
                    src_city = self.__cities.get(name_for_int(i + 1))
                    dest_city = self.__cities.get(name_for_int(j + 1))
                    edge = Edge(src_city, dest_city)

                    # self.__edges.add(edge)
                    src_city.add_outgoing_edge(edge)
                    dest_city.add_incoming_edge(edge)

        # edges: [Edge]
        # for src_city in self.__cities:
        #     for dest_city in self.__cities:
        #         if src_city != dest_city:
        #             edge = Edge(src_city, dest_city)
        #             edges.append(edges)
        #
        # self.__edges = set(edges)

    def __remove_edges(self, deterministic=False):
        edge_count = self.num_cities * (self.num_cities - 1)  # can't have self-edge
        num_to_remove = np.floor(self.HARD_MODE_FRACTION_TO_REMOVE * edge_count)

        can_delete = self.__edge_exists_matrix.copy()

        # Set aside a route to ensure at least one tour exists
        route_keep = np.random.permutation(self.num_cities)
        if deterministic:
            route_keep = self.randperm(self.num_cities)
        for i in range(self.num_cities):
            can_delete[route_keep[i], route_keep[(i + 1) % self.num_cities]] = False

        # Now remove edges until
        while num_to_remove > 0:
            if deterministic:
                src = random.randint(0, self.num_cities - 1)
                dst = random.randint(0, self.num_cities - 1)
            else:
                src = np.random.randint(self.num_cities)
                dst = np.random.randint(self.num_cities)
            if self.__edge_exists_matrix[src, dst] and can_delete[src, dst]:
                self.__edge_exists_matrix[src, dst] = False
                num_to_remove -= 1

    def randperm(self, n):
        perm = np.arange(n)
        for i in range(n):
            randind = random.randint(i, n - 1)
            save = perm[i]
            perm[i] = perm[randind]
            perm[randind] = save
        return perm

class Edge:
    def __init__(self, src_city, dest_city):
        self.__src_city: City = src_city
        self.__dest_city: City = dest_city

class City:
    def __init__(self, x: float, y: float, elevation: float):
        self.__x: float = x
        self.__y: float = y
        self.__elevation: float = elevation

        self.__outgoing_edges: set(Edge) = set()
        self.__incoming_edges: set(Edge) = set()

        self.__name: str = None
        self.__index: int = None

    def set_index_and_name(self, index: int, name: str):
        self.__index = index
        self.__name = name

    def add_outgoing_edge(self, edge: Edge):
        self.__outgoing_edges.add(edge)

    def add_incoming_edge(self, edge: Edge):
        self.__incoming_edges.add(edge)

    def get_name(self):
        return self.__name
