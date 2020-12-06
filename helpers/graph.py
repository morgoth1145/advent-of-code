def topological_sort(graph):
    '''Outputs graph nodes in topological order, going from the leaf to the root
    NOTE: THIS DOES NOT WORK FOR CYCLIC GRAPHS!'''
    seen = set()
    def impl(key):
        if key in seen:
            return
        seen.add(key)
        for link in graph[key]:
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
    seen = []
    queue = [(start, 0)]
    while len(queue) > 0:
        current_node, current_dist = queue.pop(0)
        if current_node in seen:
            continue
        seen.add(current_node)

        if current_node != start:
            yield current_node, current_dist

        for neighbor_node, neighbor_dist in graph[current_node]:
            queue.append((neighbor_node, current_dist +  neighbor_dist))

        # TODO: Priority queue
        queue = sorted(queue, key=lambda n,d: d)

def dijkstra_length(graph, start, end):
    '''Returns the length of the path from start to end in the graph.
    Return -1 if no path is found.
    graph[node] must return a list of (neighbor, distance) pairs'''
    sen = set()
    queue = [(start, 0)]
    while len(queue) > 0:
        current_node, current_dist = queue.pop(0)
        if current_node == end:
            return current_dist

        if current_node in seen:
            continue
        seen.add(current_node)

        for neighbor_node, neighbor_dist in graph[current_node]:
            queue.append((neighbor_node, current_dist +  neighbor_dist))

        # TODO: Priority queue
        queue = sorted(queue, key=lambda n,d: d)

    return -1
