import heapq


def prim_mst(graph, start=None):
    """Return MST edges and total cost using Prim's algorithm."""

    if len(graph) == 0:
        return [], 0

    if not graph.is_directed() and not __import__(
        "networkx"
    ).is_connected(graph):
        raise ValueError("MST requires a connected graph.")

    if graph.is_directed():
        raise ValueError("MST requires an undirected graph.")

    if start is None:
        start = next(iter(graph.nodes()))

    if start not in graph:
        raise ValueError("Starting intersection does not exist.")

    visited = {start}
    min_heap = []
    mst_edges = []
    total_cost = 0

    for neighbor, data in graph[start].items():
        heapq.heappush(
            min_heap,
            (data.get("weight", 1), start, neighbor)
        )

    while min_heap and len(visited) < len(graph):
        weight, u, v = heapq.heappop(min_heap)

        if v in visited:
            continue

        visited.add(v)
        mst_edges.append((u, v, weight))
        total_cost += weight

        for neighbor, data in graph[v].items():
            if neighbor not in visited:
                heapq.heappush(
                    min_heap,
                    (data.get("weight", 1), v, neighbor)
                )

    return mst_edges, total_cost


def kruskal_mst(graph):
    """Return MST edges and total cost using Kruskal's algorithm."""

    if len(graph) == 0:
        return [], 0

    if graph.is_directed():
        raise ValueError("MST requires an undirected graph.")

    import networkx as nx

    if not nx.is_connected(graph):
        raise ValueError("MST requires a connected graph.")

    parent = {node: node for node in graph.nodes()}
    rank = {node: 0 for node in graph.nodes()}

    def find(node):
        if parent[node] != node:
            parent[node] = find(parent[node])
        return parent[node]

    def union(u, v):
        root_u = find(u)
        root_v = find(v)

        if root_u == root_v:
            return False

        if rank[root_u] < rank[root_v]:
            parent[root_u] = root_v
        elif rank[root_u] > rank[root_v]:
            parent[root_v] = root_u
        else:
            parent[root_v] = root_u
            rank[root_u] += 1

        return True

    edges = sorted(
        (
            data.get("weight", 1),
            u,
            v
        )
        for u, v, data in graph.edges(data=True)
    )

    mst_edges = []
    total_cost = 0

    for weight, u, v in edges:
        if union(u, v):
            mst_edges.append((u, v, weight))
            total_cost += weight

            if len(mst_edges) == len(graph) - 1:
                break

    return mst_edges, total_cost
