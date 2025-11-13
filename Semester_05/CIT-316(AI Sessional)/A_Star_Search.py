# A* Search Algorithm - Cost-Effective Path from A to G
import heapq

class Node:
    def __init__(self, name, g, h, parent=None):
        self.name = name
        self.g = g  # Actual cost from start
        self.h = h  # Heuristic to goal
        self.f = g + h  # Total cost
        self.parent = parent
    
    def __lt__(self, other):
        return self.f < other.f

def astar(start, goal, graph, heuristic):
    open_list = []
    closed_set = set()
    best_path = {}
    
    start_node = Node(start, 0, heuristic[start])
    heapq.heappush(open_list, start_node)
    best_path[start] = start_node
    
    print(f"A* Search: {start} to {goal}\n")
    
    while open_list:
        current = heapq.heappop(open_list)
        
        if current.name in closed_set:
            continue
        
        # Goal reached
        if current.name == goal:
            # Reconstruct path
            path = []
            node = current
            while node:
                path.append(node.name)
                node = node.parent
            path.reverse()
            
            print(f"Optimal Path: {' -> '.join(path)}")
            print(f"Total Cost: {current.g}\n")
            
            # Show path details
            for i in range(len(path) - 1):
                from_node = path[i]
                to_node = path[i + 1]
                cost = best_path[to_node].g - best_path[from_node].g
                print(f"{from_node} -> {to_node} (cost={cost}, f={best_path[to_node].f})")
            return
        
        closed_set.add(current.name)
        
        # Explore neighbors
        for neighbor, edge_cost in graph.get(current.name, []):
            if neighbor in closed_set:
                continue
            
            new_g = current.g + edge_cost
            
            if neighbor not in best_path or new_g < best_path[neighbor].g:
                next_node = Node(neighbor, new_g, heuristic[neighbor], current)
                heapq.heappush(open_list, next_node)
                best_path[neighbor] = next_node
    
    print("No path found!")

# Graph: node -> [(neighbor, cost)]
graph = {
    'A': [('B', 2), ('E', 3)],
    'B': [('C', 1), ('G', 9)],
    'C': [('G', 0)],
    'E': [('D', 8)],
    'D': [('G', 1)],
    'G': []
}

# Heuristic values (h)
heuristic = {
    'A': 11,
    'B': 6,
    'C': 99,
    'D': 1,
    'E': 7,
    'G': 0
}

# print("A* Algorithm - Cost-Effective Path")
# print("Graph: A->B(2), A->E(3), B->C(1), B->G(9), C->G(0), E->D(8), D->G(1)")
# print("Heuristics: A=11, B=6, C=99, D=1, E=7, G=0\n")

astar('A', 'G', graph, heuristic)
