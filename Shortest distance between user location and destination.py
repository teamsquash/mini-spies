import heapq

def dijkstra(graph, start):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    queue = [(0, start)]
    while queue:
        (cost, current_node) = heapq.heappop(queue)
        if cost > distances[current_node]:
            continue
        for neighbor, weight in graph[current_node].items():
            new_cost = distances[current_node] + weight
            if new_cost < distances[neighbor]:
                distances[neighbor] = new_cost
                heapq.heappush(queue, (new_cost, neighbor))
    return distances

# Define a sample road network graph
graph = {
    'A': {'B': 2, 'C': 5},
    'B': {'C': 1, 'D': 3},
    'C': {'D': 2},
    'D': {'E': 4},
    'E': {}
}

# Set the starting node and run Dijkstra's algorithm
start_node = 'A'
distances = dijkstra(graph, start_node)

# Print the shortest distances from the starting node to all other nodes
print("Shortest distances from node", start_node)
for node, distance in distances.items():
    print(node, ":", distance)