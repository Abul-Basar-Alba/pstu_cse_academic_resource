def dfs_from_source(node, target, adj, vis1, vis2):
    if vis2[node]:
        return True
    vis1[node] = True
    
    for child in adj[node]:
        if not vis1[child]:
            if dfs_from_source(child, target, adj, vis1, vis2):
                return True
    return False

def dfs_from_target(node, src, adj, vis1, vis2):
    if vis1[node]:
        return True
    vis2[node] = True
    
    for child in adj[node]:
        if not vis2[child]:
            if dfs_from_target(child, src, adj, vis1, vis2):
                return True
    return False

adj = {
    1: [2, 3],
    2: [1, 4, 5],
    3: [1],
    4: [2],
    5: [2]
}

vis1 = [False] * 6
vis2 = [False] * 6
found = dfs_from_source(1, 5, adj, vis1, vis2) or dfs_from_target(5, 1, adj, vis1, vis2)

print("Bidirectional Search:", "Path Found" if found else "No Path")
