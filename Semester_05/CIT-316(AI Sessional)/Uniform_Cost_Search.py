def ucs_recursive(node, target, adj, cost):
    for child, weight in adj[node]:
        if cost[node] + weight < cost[child]:
            cost[child] = cost[node] + weight
            ucs_recursive(child, target, adj, cost)

adj = {
    1: [(2, 2), (3, 5)],
    2: [(1, 2), (4, 1), (5, 3)],
    3: [(1, 5)],
    4: [(2, 1)],
    5: [(2, 3)]
}

cost = [float('inf')] * 6
cost[1] = 0
ucs_recursive(1, 5, adj, cost)

print(f"Uniform Cost Search: Min cost from 1 to 5 = {cost[5]}")
