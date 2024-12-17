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

def topological_sort_root_first(graph):
    '''Outputs graph nodes in topological order, going from the root to the leaf
    NOTE: THIS DOES NOT WORK FOR CYCLIC GRAPHS!'''
    return list(topological_sort(graph))[::-1]

def longest_minimal_path_length(graph, start):
    '''Returns the destination and length of the longest minimal path from
    start to somewhere in the graph.

    graph[node] must return a list of (neighbor, distance) pairs
    '''
    seen = set()
    queue = [(0, start)]

    max_dist = 0
    furthest_node = start
    while len(queue) > 0:
        current_dist, current_node = heapq.heappop(queue)
        if current_node in seen:
            continue

        seen.add(current_node)
        if current_dist > max_dist:
            max_dist = current_dist
            furthest_node = current_node

        for neighbor_node, neighbor_dist in graph[current_node]:
            if neighbor_node in seen:
                continue
            heapq.heappush(queue, (current_dist + neighbor_dist,
                                   neighbor_node))
    return current_node, max_dist

def all_reachable(graph, start, max_dist=None):
    '''Returns (node, distance) pairs of all reachable nodes in the graph.
    graph[node] must return a list of (neighbor, distance) pairs

    If supplied, max_dist caps the allowed distance when reaching nodes
    '''
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
    start - Either the starting state or a list of starting states
    end_fn - Function accepting a state. Returns True if this is an end state
    and False otherwise
    heuristic - If supplied, provides an estimate of the remaining distance
    from a given node to the end
    '''
    if heuristic is None:
        heuristic = lambda n: 0

    if not isinstance(start, list):
        start = [start]

    seen = set()
    queue = [(heuristic(s), 0, s) for s in start]
    heapq.heapify(queue)
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
# Alias for ease
find_shortest_path_length_fuzzy_end = dijkstra_length_fuzzy_end

def dijkstra_length(graph, start, end, heuristic=None):
    '''Returns the length of the path from start to end in the graph.
    Return -1 if no path is found.
    graph[node] must return a list of (neighbor, distance) pairs

    Arguments:
    start - Either the starting state or a list of starting states
    end - Either the ending state or a list of possible ending states
    heuristic - If supplied, provides an estimate of the remaining distance
    from a given node to the end
    '''
    if not isinstance(end, list):
        end = [end]

    # Verify that all end states are valid nodes. I ran into dumb bugs once
    # when refactoring when passing in a list instead of a tuple!
    for e in end:
        hash(e)
        if heuristic is not None:
            assert(heuristic(e) == 0)

    end_candidates = set(end)
    def end_fn(state):
        return state in end_candidates

    return dijkstra_length_fuzzy_end(graph, start, end_fn, heuristic)
# Alias for ease
find_shortest_path_length = dijkstra_length

# TODO: Deduplicate with dijkstra_length/dijkstra_length_fuzzy_end
def make_shortest_path_graph_fuzzy_end(graph, start, end_fn, heuristic=None):
    '''Returns a graph of the states and edges which comprise the shortest
    paths.
    Returns path_graph, start(s), shortest_path_distance, total_num_paths.
    Any path from a start to any leaf (terminal) state in path_graph is a
    shortest path in the original graph.
    graph[node] must return a list of (neighbor, distance) pairs

    Arguments:
    start - Either the starting state or a list of starting states
    end_fn - Function accepting a state. Returns True if this is an end state
    and False otherwise
    heuristic - If supplied, provides an estimate of the remaining distance
    from a given node to the end
    '''
    if heuristic is None:
        heuristic = lambda n: 0

    if not isinstance(start, list):
        start = [start]

    queue = [(heuristic(s), 0, s, None) for s in start]
    heapq.heapify(queue)
    handled = set()

    class Sources:
        def __init__(self, dist):
            self.dist = dist
            self.src_nodes = []
            self.num_src_paths = 0

        def add_source(self, src_node, src_node_info):
            if src_node is None:
                # Start state
                self.num_src_paths = 1
            else:
                self.src_nodes.append(src_node)
                self.num_src_paths += src_node_info.num_src_paths

    state_to_sources = {}
    best_dist = None
    total_num_paths = 0
    end_states = []

    while len(queue) > 0:
        _, current_dist, current_node, src_node = heapq.heappop(queue)

        if best_dist is not None and current_dist > best_dist:
            break # No more paths exist

        src_info = state_to_sources.get(current_node)
        if src_info is None or src_info.dist > current_dist:
            src_info = state_to_sources[current_node] = Sources(current_dist)
        elif src_info.dist < current_dist:
            continue # Too expensive!
        src_info.add_source(src_node, state_to_sources.get(src_node))

        if end_fn(current_node):
            best_dist = current_dist
            end_states.append((current_node, current_dist))
            total_num_paths += src_info.num_src_paths
            continue

        if current_node in handled:
            continue
        handled.add(current_node)

        for neighbor_node, neighbor_dist in graph[current_node]:
            if neighbor_node in handled:
                continue # Already handled, can't be cheaper!

            new_dist = current_dist + neighbor_dist
            heapq.heappush(queue, (heuristic(neighbor_node) + new_dist,
                                   new_dist,
                                   neighbor_node,
                                   current_node))

    shortest_path_graph = {}
    start_states = []

    to_handle = end_states[:]

    while to_handle:
        state, dist = to_handle.pop()

        src_info = state_to_sources[state]

        if 0 == len(src_info.src_nodes):
            assert(src_info.dist == 0)
            start_states.append(state)
            continue

        for src in src_info.src_nodes:
            src_dist = state_to_sources[src].dist
            src_links = shortest_path_graph.get(src)
            if src_links is None:
                src_links = shortest_path_graph[src] = []
                to_handle.append((src, src_dist))
            src_links.append((state, dist-src_dist))

    # Ensure that terminal states have an empty list of neighbors.
    for state, _ in end_states:
        shortest_path_graph[state] = []

    return shortest_path_graph, start_states, best_dist, total_num_paths

def make_shortest_path_graph(graph, start, end, heuristic=None):
    '''Returns a graph of the states and edges which comprise the shortest
    paths.
    Returns path_graph, start(s), shortest_path_distance, total_num_paths.
    Any path from a start to any leaf (terminal) state in path_graph is a
    shortest path in the original graph.
    graph[node] must return a list of (neighbor, distance) pairs

    Arguments:
    start - Either the starting state or a list of starting states
    end - Either the ending state or a list of possible ending states
    heuristic - If supplied, provides an estimate of the remaining distance
    from a given node to the end
    '''
    if not isinstance(end, list):
        end = [end]

    # Verify that all end states are valid nodes. I ran into dumb bugs once
    # when refactoring when passing in a list instead of a tuple!
    for e in end:
        hash(e)
        if heuristic is not None:
            assert(heuristic(e) == 0)

    end_candidates = set(end)
    def end_fn(state):
        return state in end_candidates

    return make_shortest_path_graph_fuzzy_end(graph, start, end_fn, heuristic)

def find_shortest_paths_fuzzy_end(graph, start, end_fn, heuristic=None):
    '''Yields the (path, distance) pairs for the shortest paths from
    start to any end state in the graph.
    graph[node] must return a list of (neighbor, distance) pairs

    Arguments:
    start - Either the starting state or a list of starting states
    end_fn - Function accepting a state. Returns True if this is an end state
    and False otherwise
    heuristic - If supplied, provides an estimate of the remaining distance
    from a given node to the end
    '''
    shortest_path_graph, start_states = make_shortest_path_graph_fuzzy_end(graph, start, end_fn, heuristic)

    expansion_queue = [(state, 0, []) for state in start_states]
    while expansion_queue:
        state, dist, path = expansion_queue.pop()
        path = path + [state]

        links = shortest_path_graph[state]
        if len(links) == 0:
            # Terminal state
            yield path, dist
            continue

        for neighbor, cost in links:
            expansion_queue.append((neighbor, dist+cost, path))

def find_shortest_paths(graph, start, end, heuristic=None):
    '''Yields the (path, distance) pairs for the shortest paths from
    start to end in the graph.
    graph[node] must return a list of (neighbor, distance) pairs

    Arguments:
    start - Either the starting state or a list of starting states
    end - Either the ending state or a list of possible ending states
    heuristic - If supplied, provides an estimate of the remaining distance
    from a given node to the end
    '''
    if not isinstance(end, list):
        end = [end]

    # Verify that all end states are valid nodes. I ran into dumb bugs once
    # when refactoring when passing in a list instead of a tuple!
    for e in end:
        hash(e)
        if heuristic is not None:
            assert(heuristic(e) == 0)

    end_candidates = set(end)
    def end_fn(state):
        return state in end_candidates

    return dijkstra_length_fuzzy_end(graph, start, end_fn, heuristic)

def make_lazy_graph(neighbor_fn):
    def fn(key):
        return list(neighbor_fn(key))
    return lib.lazy_dict.make_lazy_dict(fn)

def make_compressed_graph(graph, to_keep):
    if any(isinstance(to_keep, t) for t in (set, list, tuple)):
        to_keep_set = set(to_keep)
        to_keep = lambda state: state in to_keep_set

    def neighbor_fn(start):
        seen = set()
        queue = [(0, start)]
        while len(queue) > 0:
            current_dist, current_node = heapq.heappop(queue)
            if current_node in seen:
                continue
            seen.add(current_node)

            if to_keep(current_node):
                if current_node != start:
                    yield current_node, current_dist
                    continue

            for neighbor_node, neighbor_dist in graph[current_node]:
                if neighbor_node in seen:
                    continue
                heapq.heappush(queue, (current_dist + neighbor_dist,
                                       neighbor_node))

    return make_lazy_graph(neighbor_fn)

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
