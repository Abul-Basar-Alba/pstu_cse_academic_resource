#include <bits/stdc++.h>
using namespace std;

bool dfs_from_source(int node, int target, vector<int> adj[], vector<bool> &vis1, vector<bool> &vis2) 
{
    if (vis2[node]) 
    return true; 
    vis1[node] = true;

    for (int child : adj[node]) 
    {
        if (!vis1[child])
            if (dfs_from_source(child, target, adj, vis1, vis2))
                return true;
    }
    return false;
}

bool dfs_from_target(int node, int src, vector<int> adj[], vector<bool> &vis1, vector<bool> &vis2) 
{
    if (vis1[node]) 
    return true;
    vis2[node] = true;

    for (int child : adj[node]) 
    {
        if (!vis2[child])
            if (dfs_from_target(child, src, adj, vis1, vis2))
                return true;
    }
    return false;
}

int main() 
{
    vector<int> adj[6];
    adj[1] = {2, 3};
    adj[2] = {1, 4, 5};
    adj[3] = {1};
    adj[4] = {2};
    adj[5] = {2};

    vector<bool> vis1(6, false), vis2(6, false);
    bool found = dfs_from_source(1, 5, adj, vis1, vis2) || dfs_from_target(5, 1, adj, vis1, vis2);

    cout << "Bidirectional Search (Recursive): ";
    cout << (found ? "Path Found" : "No Path");
}
