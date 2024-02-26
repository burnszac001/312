from CS312Graph import CS312GraphNode, CS312GraphEdge

class ArrayPriorityQueue:
    def __init__(self, network, src_index):
        self.nodes = network

        # a list of unordered nodes on in the queue. Nodes are added when they are discovered.
        # value of the integer is the id for the node
        self.queue: [int] = []

        # stores a list of the shortest known distance to a node
        # distance = distances[node_id]
        self.distances: [float] = [None for node in network]

        # a list of previous node_ids that led to the shortest distance at the index
        # previous node_id = prev[current_node_id]
        self.prev: [int] = [None for node in network]

        self.distances[src_index] = 0


    def view_edge(self, edge: CS312GraphEdge):
        src_node_id: int = edge.src.node_id
        dest_node_id: int = edge.dest.node_id

        path_distance = self.distances[src_node_id] + edge.length

        current_distance = self.distances[dest_node_id]
        if current_distance == None or path_distance < current_distance:
            self.distances[dest_node_id] = path_distance
            self.queue.append(dest_node_id)
            self.prev[dest_node_id] = src_node_id


    def is_empty(self):
        if len(self.queue) == 0:
            return True
        return False

    def delete_min(self):
        if not self.queue:
            return None

        lowest_dist: float = float('inf')
        min_node_i: int = None
        for index, node_id in enumerate(self.queue):
            distance = self.distances[node_id]
            if distance < lowest_dist:
                lowest_dist = distance
                min_node_i = index

        return self.queue.pop(min_node_i)


    def get_distance(self, node_id):
        return self.distances[node_id]

    def get_path(self, dest_index):
        path_edges = []
        dest_id = dest_index

        while True:
            dest_node = self.nodes[dest_id]

            src_id = self.prev[dest_id]
            src_node = self.nodes[src_id]

            length = src_node.get_edge_distance(dest_node)

            path_edges.append((src_node.loc, dest_node.loc, '{:.0f}'.format(length)))

            if self.distances[src_id] == 0:
                break

            dest_id = src_id

        return path_edges
