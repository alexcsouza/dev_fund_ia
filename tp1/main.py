from lib.search import *
from lib.graphos import *

#  # Create a graph with 4 vertices and no edges
#  V = 4
#  adj = [[] for _ in range(V)]
#  
#  # Now add edges one by one
#  add_edge(adj, 0, 1)
#  add_edge(adj, 0, 2)
#  add_edge(adj, 1, 2)
#  add_edge(adj, 2, 3)
#  
#  print("Adjacency List Representation:")
#  display_adj_list(adj)

graph = {
    'A': ['B', 'C'],  # Node A connects to B and C
    'B': ['D', 'E'],  # Node B connects to D and E
    'C': ['F', 'G'],  # Node C connects to F and G
    'D': ['H', 'I'],  # Node D connects to H and I
    'E': ['J', 'K'],  # Node E connects to J and K
    'F': ['L', 'M'],  # Node F connects to L and M
    'G': ['N', 'O'],  # Node G connects to N and O
    'H': [], 'I': [], 'J': [], 'K': [],  # Leaf nodes have no children
    'L': [], 'M': [], 'N': [], 'O': []   # Leaf nodes have no children
}

print("Depth-First Search:")
print(dfs(graph, 'A'))

print("Breadth-First Search:")
print(bfs(graph, 'A'))



# Create a sample grid
grid = np.zeros((20, 20))  # 20x20 grid, all free space initially

# Add some obstacles
grid[5:15, 10] = 1  # Vertical wall
grid[5, 5:15] = 1   # Horizontal wall

# Define start and goal positions
start_pos = (2, 2)
goal_pos = (18, 18)

# Find the path


print("A* Search:")
path = a_star(grid, start_pos, goal_pos)
print(path)
visualize_path(grid, path)




