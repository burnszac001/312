#!/usr/bin/python3


from CS312Graph import *
from array_priority_queue import ArrayPriorityQueue
from heap_priority_queue import HeapPriorityQueue
import time


class NetworkRoutingSolver:
    def __init__( self):
        pass

    def initializeNetwork( self, network ):
        assert( type(network) == CS312Graph )
        self.network = network

    def getShortestPath( self, destIndex ):
        self.dest = destIndex

        dest_distance = self.queue.get_distance(destIndex)
        total_length = dest_distance if dest_distance != None else 0
        print(total_length)
        path_edges = []
        if total_length != 0 and total_length != float('inf'):
            path_edges = self.queue.get_path(destIndex)

        return {'cost':total_length, 'path':path_edges}

    def computeShortestPaths( self, srcIndex, use_heap=False ):
        self.source = srcIndex
        if use_heap:
            self.queue = HeapPriorityQueue(self.network.nodes, srcIndex)
        else:
            self.queue = ArrayPriorityQueue(self.network.nodes, srcIndex)

        t1 = time.time()
        self.dijkstra(srcIndex, self.network.nodes)
        t2 = time.time()

        return (t2-t1)

    def dijkstra(self, src_index: int, nodes: [CS312GraphNode]):
        current_node_index = src_index
        while True:
            for edge in nodes[current_node_index].neighbors:
                self.queue.view_edge(edge)

            if self.queue.is_empty():
                break

            current_node_index = self.queue.delete_min()
