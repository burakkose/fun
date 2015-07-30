def get_state(f, w, s, c):
    return [f, w, s, c]


def check_state(f, w, s, c):
    if f != w and w == s:
        return False
    if f != s and c == s:
        return False
    return True


def get_value_str(l):
    return ''.join([str(int(i)) for i in l])


def split_value(l):
    return (bool(int(i)) for i in l)


def get_all_child(state):
    f, w, s, c = state
    result = []
    if check_state(not f, w, s, c):
        result.append(get_state(not f, w, s, c))

    if f == w and check_state(not f, not w, s, c):
        result.append(get_state(not f, not w, s, c))

    if f == s and check_state(not f, w, not s, c):
        result.append(get_state(not f, w, not s, c))

    if f == c and check_state(not f, w, s, not c):
        result.append(get_state(not f, w, s, not c))

    return result


graph = {}


def build_graph(key):
    if key == '1111':
        return
    if graph.get(key, False):
        return
    graph[key] = set()
    for n in get_all_child(split_value(key)):
        n = get_value_str(n)
        graph[key].add(n)
        build_graph(n)


def bfs_paths(g, start, goal):
    queue = [(start, [start])]
    while queue:
        (vertex, path) = queue.pop(0)
        for next in g[vertex] - set(path):
            if next == goal:
                yield path + [next]
            else:
                queue.append((next, path + [next]))


def shortest_path(g, start, goal):
    try:
        return next(bfs_paths(g, start, goal))
    except StopIteration:
        return None


build_graph('0000')
path = shortest_path(graph, '0000', '1111')
