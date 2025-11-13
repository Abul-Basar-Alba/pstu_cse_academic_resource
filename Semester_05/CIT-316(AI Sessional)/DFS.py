# def dfs(start, adj, n):
#     visited = [False] * (n + 1)
#     stack = [start]
    
#     while stack:
#         node = stack.pop()
        
#         if visited[node]:
#             continue
            
#         visited[node] = True
#         print(node, end=' ')
        
#         for i in range(len(adj[node]) - 1, -1, -1):
#             child = adj[node][i]
#             if not visited[child]:
#                 stack.append(child)

# n = 5
# adj = {
#     1: [2, 3],
#     2: [1, 4, 5],
#     3: [1],
#     4: [2],
#     5: [2]
# }

# print("DFS: ", end='')
# dfs(1, adj, n)



def dfs(node, adj, visited):
    visited.add(node)
    print(node, end=' ')
    
    for child in adj[node]:
        if child not in visited:
            dfs(child, adj, visited)

adj = {
    'B': ['A', 'C', 'D', 'E'],
    'A': ['C'],
    'C': ['G'],
    'D': ['E'],
    'E': ['F'],
    'F': ['I'],
    'G': ['H', 'I', 'J'],
    'H': ['K'],
    'I': ['J', 'L'],
    'J': ['K'],
    'K': [],
    'L': []
}

visited = set()
print("DFS (Recursive): ", end='')
dfs('B', adj, visited)
print()