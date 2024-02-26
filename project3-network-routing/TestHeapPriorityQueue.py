class HeapPriorityQueue:
    def __init__(self, nodes, src_index):
        self.nodes = nodes

        self.heap = []

        self.distance = [None for node in nodes]
        self.distance[src_index] = 0

        self.prev = [None for node in nodes]


    def view_edge(self):
        src_node_id = edge.src.node_id
        dest_node_id = edge.dest.node_id

        path_distance = self.distances[src_node_id] + edge.length

        current_distance = self.distances[dest_node_id]