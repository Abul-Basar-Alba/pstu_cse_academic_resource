# from collections import deque

# def bfs(start, adj, n):
#     visited = [False] * (n + 1)
#     queue = deque([start])
#     visited[start] = True
    
#     while queue:
#         node = queue.popleft()
#         print(node, end=' ')
        
#         for child in adj[node]:
#             if not visited[child]:
#                 visited[child] = True
#                 queue.append(child)

# n = 5
# adj = {
#     1: [2, 3],
#     2: [1, 4, 5],
#     3: [1],
#     4: [2],
#     5: [2]
# }

# print("BFS: ", end='')
# bfs(1, adj, n)


from collections import deque

def bfs_recursive(queue, adj, visited):
    if not queue:
        return
    
    node = queue.popleft()
    print(node, end=' ')
    
    for child in adj[node]:
        if child not in visited:
            visited.add(child)
            queue.append(child)
    
    bfs_recursive(queue, adj, visited)

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

print("BFS (Recursive): ", end='')
visited = {'B'}
queue = deque(['B'])
bfs_recursive(queue, adj, visited)
print()