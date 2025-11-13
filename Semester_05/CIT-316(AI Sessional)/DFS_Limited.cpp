#include <bits/stdc++.h>
using namespace std;

void dfs_limited(int node, int parent, vector<int> adj[], int depth, int limit) 
{
    cout << node << " ";
    if (depth == limit) 
    return;

    for (int child : adj[node])
    {
        if (child != parent)
            dfs_limited(child, node, adj, depth + 1, limit);
    }
}

int main() 
{
    vector<int> adj[6];
    adj[1] = {2, 3};
    adj[2] = {1, 4, 5};
    adj[3] = {1};
    adj[4] = {2};
    adj[5] = {2};

    cout << "DFS Limited (depth 2): ";
    dfs_limited(1, -1, adj, 0, 1);
}
