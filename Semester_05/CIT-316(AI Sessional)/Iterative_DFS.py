def DLS(adj, start, goal, depth_limit, path):
    if start == goal:
        path.append(start)
        return True
    
    if depth_limit <= 0:
        return False
    
    path.append(start)
    
    for child in adj[start]:
        if DLS(adj, child, goal, depth_limit - 1, path):
            return True
    
    return False

def IDDFS(adj, start, goal, max_depth):
    print("Iterative Deepening DFS:\n")
    
    for depth in range(max_depth + 1):
        path = []
        print(f"Depth Limit = {depth}: ", end='')
        
        if DLS(adj, start, goal, depth, path):
            print(' -> '.join(map(str, path)))
            print(f"\nGoal {goal} found at depth {depth}")
            return True
        
        print(' -> '.join(map(str, path)) if path else "No path")
    
    print(f"\nGoal not found within depth {max_depth}")
    return False

adj = {
    0: [1, 2],
    1: [3, 4],
    2: [5, 6],
    3: [],
    4: [],
    5: [],
    6: [7],
    7: []
}

print("Graph Structure:")
print("       0")
print("      / \\")
print("     1   2")
print("    / \\ / \\")
print("   3  4 5  6")
print("           |")
print("           7\n")

IDDFS(adj, 0, 7, 5)
