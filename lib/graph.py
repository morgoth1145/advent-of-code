import collections
import heapq

def topological_sort(graph):
    '''Outputs graph nodes in topological order, going from the leaf to the root
    NOTE: THIS DOES NOT WORK FOR CYCLIC GRAPHS!'''
    seen = set()
    def impl(key):
        if key in seen:
            return
        seen.add(key)
        for link in graph.get(key, []):
            yield from impl(link)
        yield key
    for key in graph.keys():
        yield from impl(key)

def shortest_path(graph, start, end):
    '''Searches for and returns the shortest path from start to end in the graph
    Returns None on failure to find any path
    Uses BFS'''
    seen = set()
    queue = [[start]]
    while len(queue) > 0:
        current = queue.pop(0)
        pos = current[-1]
        seen.add(pos)
        if pos == end:
            return current

        for neighbor in graph[pos]:
            if neighbor not in seen:
                queue.append(current + [neighbor])
    return None

def longest_path_length(graph, start):
    '''Searches for and returns the length of the longest path from start to
    somewhere in the graph'''
    seen = {start}
    steps = -1
    queue = [start]
    while len(queue) > 0:
        steps += 1
        new_queue = []
        for pos in queue:
            for neighbor in graph[pos]:
                if neighbor in seen:
                    continue
                new_queue.append(neighbor)
                seen.add(neighbor)
        queue = new_queue
    return steps

def all_reachable(graph, start):
    '''Returns (node, distance) pairs of all reachable nodes in the graph.
    graph[node] must return a list of (neighbor, distance) pairs'''
    seen = set()
    queue = [(0, start)]
    while len(queue) > 0:
        current_dist, current_node = heapq.heappop(queue)
        if current_node in seen:
            continue
        seen.add(current_node)

        if current_node != start:
            yield current_node, current_dist

        for neighbor_node, neighbor_dist in graph[current_node]:
            if neighbor_node in seen:
                continue
            heapq.heappush(queue, (current_dist + neighbor_dist,
                                   neighbor_node))

def dijkstra_length(graph, start, end, heuristic=None):
    '''Returns the length of the path from start to end in the graph.
    Return -1 if no path is found.
    graph[node] must return a list of (neighbor, distance) pairs

    Arguments:
    heuristic - If supplied, provides an estimate of the remaining distance
    from a given node to the end
    '''
    if heuristic is None:
        heuristic = lambda n: 0
    seen = set()
    queue = [(heuristic(start), 0, start)]
    while len(queue) > 0:
        _, current_dist, current_node = heapq.heappop(queue)

        if current_node == end:
            return current_dist

        if current_node in seen:
            continue
        seen.add(current_node)

        for neighbor_node, neighbor_dist in graph[current_node]:
            if neighbor_node in seen:
                continue
            new_dist = current_dist + neighbor_dist
            heapq.heappush(queue, (heuristic(neighbor_node) + new_dist,
                                   new_dist,
                                   neighbor_node))

    return -1

class _LazyGraph(collections.defaultdict):
    def __init__(self, neighbor_fn):
        super().__init__()
        self._neighbor_fn = neighbor_fn

    def __missing__(self, key):
        neighbors = self._neighbor_fn(key)
        self[key] = neighbors
        return neighbors

def make_lazy_graph(neighbor_fn):
    return _LazyGraph(neighbor_fn)
