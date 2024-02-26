class HeapPriorityQueue:
    def __init__(self, network, src_index):
        self.nodes = network

        self.heap = [None]

        self.distances = [float('inf')] * len(network)

        self.prev = [None] * len(network)

        self.distances[src_index] = 0
        self.heap.append(src_index)

        self._build_heap()

    def _build_heap(self):
        for i in range(len(self.heap) // 2, 0, -1):
            self._min_heapify(i)

    def _min_heapify(self, i):
        left = 2 * i
        right = 2 * i + 1
        smallest = i

        if left < len(self.heap) and self.distances[self.heap[left]] < self.distances[self.heap[smallest]]:
            smallest = left
        if right < len(self.heap) and self.distances[self.heap[right]] < self.distances[self.heap[smallest]]:
            smallest = right

        if smallest != i:
            self._swap(i, smallest)
            self._min_heapify(smallest)

    def view_edge(self, edge):
        src_node_id = edge.src.node_id
        dest_node_id = edge.dest.node_id

        path_distance = self.distances[src_node_id] + edge.length

        current_distance = self.distances[dest_node_id]
        if current_distance is None or path_distance < current_distance:
            self.distances[dest_node_id] = path_distance
            self.prev[dest_node_id] = src_node_id

            if dest_node_id in self.heap:
                index = self.heap.index(dest_node_id)
                self._bubble_up(index)
            else:
                self.heap.append(dest_node_id)
                self._bubble_up(len(self.heap) - 1)

    def _bubble_up(self, i):
        while i > 1 and self.distances[self.heap[i]] < self.distances[self.heap[i // 2]]:
            self._swap(i, i // 2)
            i //= 2

    def is_empty(self):
        return len(self.heap) == 1

    def delete_min(self):
        if len(self.heap) == 1:
            return None

        min_node = self.heap[1]
        last_node = self.heap.pop()

        if len(self.heap) > 1:
            self.heap[1] = last_node
            self._min_heapify(1)

        return min_node

    def _swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

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
