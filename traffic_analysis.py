import math


def bellman_ford(graph, source, destination):
    """Find the shortest route using Bellman-Ford."""

    if source not in graph or destination not in graph:
        raise ValueError("Source or destination does not exist.")

    nodes = list(graph.nodes())
    distances = {node: float("inf") for node in nodes}
    previous = {node: None for node in nodes}

    distances[source] = 0
    updates = []

    # Represent undirected roads in both directions
    edges = []

    for u, v, data in graph.edges(data=True):
        weight = data.get("weight", 1)

        if not math.isfinite(weight):
            raise ValueError("Road weights must be finite.")

        edges.append((u, v, weight))
        edges.append((v, u, weight))

    # Relax edges at most V - 1 times
    for iteration in range(len(nodes) - 1):
        changed = False

        for u, v, weight in edges:
            if distances[u] != float("inf"):
                new_distance = distances[u] + weight

                if new_distance < distances[v]:
                    distances[v] = new_distance
                    previous[v] = u
                    changed = True

                    updates.append({
                        "Iteration": iteration + 1,
                        "From": u,
                        "To": v,
                        "Updated Distance": new_distance
                    })

        if not changed:
            break

    # Detect reachable negative-weight cycles
    for u, v, weight in edges:
        if (distances[u] != float("inf")
                and distances[u] + weight < distances[v]):
            raise ValueError("Reachable negative-weight cycle detected.")

    # Reconstruct the route
    path = []

    if math.isfinite(distances[destination]):
        current = destination

        while current is not None:
            path.append(current)
            current = previous[current]

        path.reverse()

    return path, distances[destination], updates


def simulate_congestion(graph, u, v, new_weight):
    """Return a copy of the graph with a modified road weight."""

    if not graph.has_edge(u, v):
        raise ValueError("The specified road does not exist.")

    if not math.isfinite(new_weight) or new_weight < 0:
        raise ValueError("Travel time must be finite and non-negative.")

    updated_graph = graph.copy()
    updated_graph[u][v]["weight"] = new_weight

    return updated_graph
