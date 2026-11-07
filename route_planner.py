import heapq
import math


def dijkstra(graph, source, destination):
    """Find the shortest route using Dijkstra's algorithm."""

    if source not in graph or destination not in graph:
        raise ValueError("Source or destination does not exist.")

    for _, _, data in graph.edges(data=True):
        weight = data.get("weight", 1)

        if not math.isfinite(weight) or weight < 0:
            raise ValueError(
                "Dijkstra requires finite, non-negative road weights."
            )

    distances = {node: float("inf") for node in graph.nodes()}
    previous = {node: None for node in graph.nodes()}

    distances[source] = 0
    priority_queue = [(0, source)]
    updates = []

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        if current_distance > distances[current_node]:
            continue

        if current_node == destination:
            break

        for neighbor in graph.neighbors(current_node):
            weight = graph[current_node][neighbor].get("weight", 1)
            new_distance = current_distance + weight

            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                previous[neighbor] = current_node

                heapq.heappush(
                    priority_queue,
                    (new_distance, neighbor)
                )

                updates.append({
                    "From": current_node,
                    "To": neighbor,
                    "Updated Distance": new_distance
                })

    path = []

    if math.isfinite(distances[destination]):
        current = destination

        while current is not None:
            path.append(current)
            current = previous[current]

        path.reverse()

    return path, distances[destination], updates
