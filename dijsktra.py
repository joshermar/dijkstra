class NodeQueue:
    def __init__(self, node_attrs=None):
        ''' The logic behind node_attrs=None is that new instances should not necessarily
        be required to immediately provide node information. This may change.'''

        self.queue = []

        if node_attrs:
            for node in node_attrs.keys():
                self._append_new(node, node_attrs)

    def _append_new(self, new_node, node_attrs):
        if self.empty():
            self.queue.append(new_node)
            return

        if node_attrs[new_node]['cost'] >= float('inf'):
            self.queue.append(new_node)
            return

        for i, n in enumerate(self.queue):
            if node_attrs[new_node]['cost'] <= node_attrs[n]['cost']:
                self.queue.insert(i, new_node)
                return

    def update_priority(self, node, node_attrs):
        self.queue.remove(node)
        self._append_new(node, node_attrs)

    def pop(self):
        return self.queue.pop(0)

    def empty(self):
        return not self.queue


def _get_path(node_attrs, start, current, path=[]):
    path.append(current)

    if current == start:
        return reversed(path)
    else:
        previous = node_attrs[current]['through']
        return _get_path(node_attrs, start, previous, path)


def find_shortest_path(graph, start, end):
    node_attrs = {node: {'cost': float('inf'), 'through': None} for node in graph.keys()}
    node_attrs[start] = {'cost': 0, 'through': start}

    queue = NodeQueue(node_attrs)
    visited = set()

    while not queue.empty():

        current_node = queue.pop()
        visited.add(current_node)

        if current_node == end:
            path = ' -> '.join(_get_path(node_attrs, start, end))
            print(
                f'Found best path from {start} to {end}:\n'
                f'{path}\n'
                f'Total cost: {node_attrs[end]["cost"]}')
            return

        for neighbor in graph[current_node].keys():
            if neighbor in visited:
                continue

            tent_dist = graph[current_node][neighbor] + node_attrs[current_node]['cost']

            if tent_dist < node_attrs[neighbor]['cost']:
                node_attrs[neighbor]['cost'] = tent_dist
                node_attrs[neighbor]['through'] = current_node
                queue.update_priority(neighbor, node_attrs)

    print(f'Unable to find a path from {start} to {end}!')  # You should never see this with a proper graph


# This example graph comes from Computerphile's YouTube Video on Dijksta's Algorithm.
example_graph = {
    'S': {'A': 7, 'B': 2, 'C': 3},
    'A': {'S': 7, 'B': 3, 'D': 4},
    'B': {'S': 2, 'A': 3, 'D': 4, 'H': 1},
    'C': {'S': 3, 'L': 2},
    'D': {'A': 4, 'B': 4, 'F': 5},
    'F': {'D': 5, 'H': 3},
    'H': {'B': 1, 'F': 3, 'G': 2},
    'G': {'H': 2, 'E': 2},
    'L': {'C': 2, 'I': 4, 'J': 4},
    'I': {'J': 6, 'K': 4, 'L': 4},
    'J': {'I': 6, 'K': 4, 'L': 4},
    'K': {'I': 4, 'J': 4, 'E': 5},
    'E': {'G': 2, 'K': 5}
}


find_shortest_path(example_graph, 'S', 'E')
