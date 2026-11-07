from collections import deque


def bfs(graph, start):
    """Return BFS traversal order from the starting intersection."""

    if start not in graph:
        raise ValueError("Starting intersection does not exist.")

    visited = {start}
    traversal_order = []
    queue = deque([start])

    while queue:
        current = queue.popleft()
        traversal_order.append(current)

        for neighbor in graph.neighbors(current):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return traversal_order


def dfs(graph, start):
    """Return DFS traversal order from the starting intersection."""

    if start not in graph:
        raise ValueError("Starting intersection does not exist.")

    visited = set()
    traversal_order = []

    def explore(current):
        visited.add(current)
        traversal_order.append(current)

        for neighbor in graph.neighbors(current):
            if neighbor not in visited:
                explore(neighbor)

    explore(start)

    return traversal_order
