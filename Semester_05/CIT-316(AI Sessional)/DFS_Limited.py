def dfs_limited(node, parent, adj, depth, limit):
    print(node, end=' ')
    
    if depth == limit:
        return
    
    for child in adj[node]:
        if child != parent:
            dfs_limited(child, node, adj, depth + 1, limit)

adj = {
    1: [2, 3],
    2: [1, 4, 5],
    3: [1],
    4: [2],
    5: [2]
}

print("DFS Limited (depth 2): ", end='')
dfs_limited(1, -1, adj, 0, 1)
