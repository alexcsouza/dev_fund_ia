from lib.search import *
from lib.graphos import *
import math


def init():
    global lado_direito
    global lado_esquerdo
    lado_direito  = ['A', 'B', 'C', 'D']
    lado_esquerdo = []

def mover_esquerda(p1, p2):
    lado_esquerdo.append(p1)
    lado_esquerdo.append(p2)
    lado_direito.remove(p1)
    lado_direito.remove(p2)
    return max(pessoas[p1]['tempo'], pessoas[p2]['tempo'])

def mover_direita(p1):
    lado_direito.append(p1)
    lado_esquerdo.remove(p1)
    return pessoas[p1]['tempo']

def create_representation(index, lado_esquerdo, lado_direito):
    plt.figure(figsize=(10, 10))
    # plt.imshow(grid, cmap='binary')
    
    cont = 1
    for esq in lado_esquerdo:
        plt.plot( 1, cont, 'b-', linewidth=3, label=esq)
        cont = cont + 1

    cont = 1
    for dir in lado_direito:
        plt.plot( 10, cont, 'b-', linewidth=3, label=dir)
        cont = cont + 1

    # if path:
    #     path = np.array(path)
    #     plt.plot(path[:, 1], path[:, 0], 'b-', linewidth=3, label='Path')
    #     plt.plot(path[0, 1], path[0, 0], 'go', markersize=15, label='Start')
    #     plt.plot(path[-1, 1], path[-1, 0], 'ro', markersize=15, label='Goal')
    
    plt.grid(True)
    plt.legend(fontsize=12)
    plt.title(f'Representação: {index}')
    
    # Pasta de imagens
    img_base_path = Path('img/')
    a_star_graph = f'{img_base_path}/rep-{index}.png'
    plt.savefig(a_star_graph)


pessoas = {
    'A': {'tempo': 1,  'tocha': False},
    'B': {'tempo': 2,  'tocha': False},
    'C': {'tempo': 5,  'tocha': False},
    'D': {'tempo': 10, 'tocha': False}
}

lado_direito  = []
lado_esquerdo = []
init()

tempo = 0

print(f"esq: {lado_esquerdo}")
print(f"dir: {lado_direito}")
print("\n")
create_representation(0, lado_esquerdo, lado_direito)

tempo = tempo + mover_esquerda('A', 'B')
pessoas['A']['tocha'] = True
print(f"esq: {lado_esquerdo}")
print(f"dir: {lado_direito}")
print("\n")
create_representation(1, lado_esquerdo, lado_direito)


tempo = tempo + mover_direita('A')
pessoas['A']['tocha'] = True
print(f"esq: {lado_esquerdo}")
print(f"dir: {lado_direito}")
print("\n")
create_representation(2, lado_esquerdo, lado_direito)


tempo = tempo + mover_esquerda('A', 'C')
pessoas['A']['tocha'] = True
print(f"esq: {lado_esquerdo}")
print(f"dir: {lado_direito}")
print("\n")
create_representation(3, lado_esquerdo, lado_direito)


tempo = tempo + mover_direita('A')
pessoas['A']['tocha'] = True
print(f"esq: {lado_esquerdo}")
print(f"dir: {lado_direito}")
print("\n")
create_representation(4, lado_esquerdo, lado_direito)



tempo = tempo + mover_esquerda('A', 'D')
pessoas['A']['tocha'] = True
print(f"esq: {lado_esquerdo}")
print(f"dir: {lado_direito}")
print("\n")
create_representation(3, lado_esquerdo, lado_direito)


print(f"esq: {lado_esquerdo}")
print(f"dir: {lado_direito}")
print(f"Tempo Total: {tempo} minutos")

print("\n")




lado_direito  = []
lado_esquerdo = []
init()

tempo = 0


print(f"esq: {lado_esquerdo}")
print(f"dir: {lado_direito}")
print("\n")
create_representation(0, lado_esquerdo, lado_direito)

cont = 0
while len(lado_direito) > 0:
    p1 = lado_direito[0]
    p2 = lado_direito[1]

    if(pessoas[p1]['tempo'] > pessoas[p2]['tempo']):
        pessoas[p2]['tocha'] = True 
        pessoas[p1]['tocha'] = False 
        mais_rapida = p2
        tempo_mais_lento = pessoas[p1]['tempo']
    else:    
        pessoas[p2]['tocha'] = False 
        pessoas[p1]['tocha'] = True 
        mais_rapida = p1
        tempo_mais_lento = pessoas[p2]['tempo']
    
    cont = cont + 1
    tempo = tempo + mover_esquerda(p1, p2)
    print(f"esq <- {p1}, {p2} - {tempo}")
    print(f"esq: {lado_esquerdo}")
    print(f"dir: {lado_direito}")
    print("\n")
    create_representation(cont, lado_esquerdo, lado_direito)

    if(len(lado_direito) <= 0): 
        break
    
    cont = cont + 1
    tempo = tempo + mover_direita(mais_rapida)
    print(f"{mais_rapida} -> dir - {tempo}")
    print(f"esq: {lado_esquerdo}")
    print(f"dir: {lado_direito}")
    print("\n")
    create_representation(cont, lado_esquerdo, lado_direito)


print(f"esq: {lado_esquerdo}")
print(f"dir: {lado_direito}")
print(f"Tempo Total: {tempo} minutos")

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

# graph = {
#     'A': ['B', 'C'],  # Node A connects to B and C
#     'B': ['D', 'E'],  # Node B connects to D and E
#     'C': ['F', 'G'],  # Node C connects to F and G
#     'D': ['H', 'I'],  # Node D connects to H and I
#     'E': ['J', 'K'],  # Node E connects to J and K
#     'F': ['L', 'M'],  # Node F connects to L and M
#     'G': ['N', 'O'],  # Node G connects to N and O
#     'H': [], 'I': [], 'J': [], 'K': [],  # Leaf nodes have no children
#     'L': [], 'M': [], 'N': [], 'O': []   # Leaf nodes have no children
# }
# 
# print("Depth-First Search:")
# print(dfs(graph, 'A'))
# 
# print("Breadth-First Search:")
# print(bfs(graph, 'A'))
# 
# 
# 
# # Create a sample grid
# grid = np.zeros((20, 20))  # 20x20 grid, all free space initially
# 
# # Add some obstacles
# grid[5:15, 10] = 1  # Vertical wall
# grid[5, 5:15] = 1   # Horizontal wall
# 
# # Define start and goal positions
# start_pos = (2, 2)
# goal_pos = (18, 18)
# 
# # Find the path
# 
# 
# print("A* Search:")
# path = a_star(grid, start_pos, goal_pos)
# print(path)
# visualize_path(grid, path)




