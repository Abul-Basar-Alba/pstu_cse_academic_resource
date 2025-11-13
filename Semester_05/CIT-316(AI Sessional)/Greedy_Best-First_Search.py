# Greedy Best-First Search - Romania Map (Arad to Bucharest)
import heapq

# Romania graph with step costs (km)
graph = {
    'Arad': [('Zerind', 75), ('Sibiu', 140), ('Timisoara', 118)],
    'Zerind': [('Arad', 75), ('Oradea', 71)],
    'Oradea': [('Zerind', 71), ('Sibiu', 151)],
    'Sibiu': [('Arad', 140), ('Oradea', 151), ('Fagaras', 99), ('Rimnicu Vilcea', 80)],
    'Timisoara': [('Arad', 118), ('Lugoj', 111)],
    'Lugoj': [('Timisoara', 111), ('Mehadia', 70)],
    'Mehadia': [('Lugoj', 70), ('Dobreta', 75)],
    'Dobreta': [('Mehadia', 75), ('Craiova', 120)],
    'Craiova': [('Dobreta', 120), ('Rimnicu Vilcea', 146), ('Pitesti', 138)],
    'Rimnicu Vilcea': [('Sibiu', 80), ('Craiova', 146), ('Pitesti', 97)],
    'Fagaras': [('Sibiu', 99), ('Bucharest', 211)],
    'Pitesti': [('Rimnicu Vilcea', 97), ('Craiova', 138), ('Bucharest', 101)],
    'Bucharest': [('Fagaras', 211), ('Pitesti', 101), ('Giurgiu', 90), ('Urziceni', 85)],
    'Giurgiu': [('Bucharest', 90)],
    'Urziceni': [('Bucharest', 85), ('Vaslui', 142), ('Hirsova', 98)],
    'Hirsova': [('Urziceni', 98), ('Eforie', 86)],
    'Eforie': [('Hirsova', 86)],
    'Vaslui': [('Urziceni', 142), ('Iasi', 92)],
    'Iasi': [('Vaslui', 92), ('Neamt', 87)],
    'Neamt': [('Iasi', 87)]
}

# Straight-line distance to Bucharest (heuristic)
h = {
    'Arad': 366,
    'Bucharest': 0,
    'Craiova': 160,
    'Dobreta': 242,
    'Eforie': 161,
    'Fagaras': 178,
    'Giurgiu': 77,
    'Hirsova': 151,
    'Iasi': 226,
    'Lugoj': 244,
    'Mehadia': 241,
    'Neamt': 234,
    'Oradea': 380,
    'Pitesti': 98,
    'Rimnicu Vilcea': 193,
    'Sibiu': 253,
    'Timisoara': 329,
    'Urziceni': 80,
    'Vaslui': 199,
    'Zerind': 374
}

def greedy_best_first(start, goal):
    pq = [(h[start], start)]
    visited = set()
    parent = {}
    cost_so_far = {start: 0}
    
    print(f"Greedy Best-First Search: {start} to {goal}\n")
    print("Exploring nodes (ordered by heuristic):")
    
    while pq:
        current_h, node = heapq.heappop(pq)
        
        if node in visited:
            continue
        
        visited.add(node)
        print(f"{node} (h={current_h})")
        
        # Goal reached
        if node == goal:
            # Reconstruct path
            path = []
            current = goal
            total_cost = cost_so_far[goal]
            
            while current in parent:
                path.append(current)
                current = parent[current]
            path.append(start)
            path.reverse()
            
            print(f"\nPath Found: {' -> '.join(path)}")
            print(f"Total Distance: {total_cost} km")
            
            # Show path details
            print("\nPath Details:")
            for i in range(len(path) - 1):
                from_city = path[i]
                to_city = path[i + 1]
                step_cost = cost_so_far[to_city] - cost_so_far[from_city]
                print(f"{from_city} -> {to_city} ({step_cost} km)")
            return
        
        # Explore neighbors
        for neighbor, edge_cost in graph[node]:
            if neighbor not in visited:
                heapq.heappush(pq, (h[neighbor], neighbor))
                if neighbor not in parent:
                    parent[neighbor] = node
                    cost_so_far[neighbor] = cost_so_far[node] + edge_cost
    
    print("\nNo path found!")

print("Romania Map - Greedy Best-First Search")
print("=" * 50)
print("Goal: Find path from Arad to Bucharest")
print("Heuristic: Straight-line distance to Bucharest\n")

greedy_best_first('Arad', 'Bucharest')
