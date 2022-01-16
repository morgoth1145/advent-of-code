import heapq

import lib.lazy_dict

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

# TODO: Change to use the distance-based graph
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

def all_reachable(graph, start, max_dist=None):
    '''Returns (node, distance) pairs of all reachable nodes in the graph.
    graph[node] must return a list of (neighbor, distance) pairs

    If supplied, max_dist caps the allowed distance when reaching nodes'''
    seen = set()
    queue = [(0, start)]
    while len(queue) > 0:
        current_dist, current_node = heapq.heappop(queue)
        if current_node in seen:
            continue
        if max_dist is not None and max_dist < current_dist:
            continue
        seen.add(current_node)

        if current_node != start:
            yield current_node, current_dist

        for neighbor_node, neighbor_dist in graph[current_node]:
            if neighbor_node in seen:
                continue
            heapq.heappush(queue, (current_dist + neighbor_dist,
                                   neighbor_node))

def dijkstra_length_fuzzy_end(graph, start, end_fn, heuristic=None):
    '''Returns the length of the shortest path from start to any end state
    in the graph. Return -1 if no path is found.
    graph[node] must return a list of (neighbor, distance) pairs

    Arguments:
    end_fn - Function accepting a state. Returns True if this is an end state
    and False otherwise
    heuristic - If supplied, provides an estimate of the remaining distance
    from a given node to the end
    '''
    if heuristic is None:
        heuristic = lambda n: 0

    seen = set()
    queue = [(heuristic(start), 0, start)]
    while len(queue) > 0:
        _, current_dist, current_node = heapq.heappop(queue)

        if end_fn(current_node):
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

def dijkstra_length(graph, start, end, heuristic=None):
    '''Returns the length of the path from start to end in the graph.
    Return -1 if no path is found.
    graph[node] must return a list of (neighbor, distance) pairs

    Arguments:
    heuristic - If supplied, provides an estimate of the remaining distance
    from a given node to the end
    '''
    def end_fn(state):
        return state == end

    # Verify that end is a valid node. I ran into dumb bugs when refactoring
    # when passing in a list that should have been a tuple!
    hash(end)
    if heuristic is not None:
        assert(heuristic(end) == 0)

    return dijkstra_length_fuzzy_end(graph, start, end_fn, heuristic)

def make_lazy_graph(neighbor_fn):
    def fn(key):
        return list(neighbor_fn(key))
    return lib.lazy_dict.make_lazy_dict(fn)

def to_distance_graph(graph):
    '''Some usages more naturally generate graphs without distance information.
    Most utilities in this library expect a distance graph, so a converter
    makes some usages much easier.
    '''
    def neighbor_fn(node):
        for n in graph[node]:
            yield n, 1
    return make_lazy_graph(neighbor_fn)

def node_dist_list_to_nodes(node_dist_list):
    '''Some usages only care about the list of nodes, not the distances.
    A converter from node-distance lists to a list of nodes can simplify such
    usages.
    '''
    for node, dist in node_dist_list:
        yield node
