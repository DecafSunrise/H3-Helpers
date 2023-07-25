import h3
from queue import Queue

# Define the starting hexagon ID and the maximum number of steps
start_hex_id = '89c258773ffffff'
max_steps = 5

# Define the GeoJSON or shapefile bounds of the hexagons to be generated
# This example uses a bounding box in San Francisco
bounds = {
    "type": "Polygon",
    "coordinates": [[
        [-122.5177, 37.6044],
        [-122.5177, 37.8199],
        [-122.3524, 37.8199],
        [-122.3524, 37.6044],
        [-122.5177, 37.6044]
    ]]
}

# Define a friction surface (costs associated with each hexagon)
friction_surface = {
    '89c258773ffffff': {'cost': 1.0, 'visited_from': None},  # Start hexagon with base cost
    '89c258772ffffff': {'cost': 1.5, 'visited_from': None},  # Hexagon with additional cost
    '89c258774ffffff': {'cost': 0.8, 'visited_from': None}   # Hexagon with reduced cost
}

# Generate the initial set of hexagons using the h3.polyfill method
hexagons = set(h3.polyfill(bounds, 9))

# Create a set to track which hexagons we have already visited
visited = set()

# Create a queue to hold the hexagons we need to visit next
queue = Queue()

# Add the starting hexagon to the queue
queue.put(start_hex_id)

# Start the BFS algorithm
while not queue.empty() and len(visited) < max_steps:
    # Get the next hexagon ID from the queue
    current_hex_id = queue.get()

    # Skip the hexagon if we've already visited it
    if current_hex_id in visited:
        continue

    # Add the hexagon to the visited set
    visited.add(current_hex_id)

    # Get the neighboring hexagons
    neighbors = h3.k_ring(current_hex_id, 1)

    # Traverse the neighboring hexagons
    for neighbor in neighbors:
        if neighbor not in visited and neighbor in hexagons:
            # Calculate the cost to reach the neighbor hexagon
            neighbor_cost = friction_surface[current_hex_id]['cost'] + 1.0

            # Check if the neighbor hexagon has a lower cost or hasn't been visited before
            if (
                neighbor not in friction_surface
                or neighbor_cost < friction_surface[neighbor]['cost']
            ):
                # Update the cost and visited_from information of the neighbor hexagon
                friction_surface[neighbor] = {
                    'cost': neighbor_cost,
                    'visited_from': current_hex_id
                }

                # Add the neighbor hexagon to the queue
                queue.put(neighbor)

# Print the visited hexagons and their visited_from information
for hex_id in visited:
    print(f"Hexagon ID: {hex_id}, Visited From: {friction_surface[hex_id]['visited_from']}")
