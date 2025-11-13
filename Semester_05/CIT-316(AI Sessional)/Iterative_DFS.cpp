#include <bits/stdc++.h>
using namespace std;

bool DLS(vector<int> adj[], int start, int goal, int depth_limit) 
{
    if (start == goal) {
        cout << start << " ";
        return true;
    }
    
    if (depth_limit <= 0) return false;
    
    cout << start << " ";
    
    for (int child : adj[start]) {
        if (DLS(adj, child, goal, depth_limit - 1))
            return true;
    }
    
    return false;
}

bool IDDFS(vector<int> adj[], int start, int goal, int max_depth) 
{
    cout << "Iterative Deepening DFS:\n\n";
    
    for (int depth = 0; depth <= max_depth; depth++) {
        cout << "Depth Limit = " << depth << ": ";
        
        if (DLS(adj, start, goal, depth)) {
            cout << "\n\nGoal " << goal << " found at depth " << depth << "\n";
            return true;
        }
        cout << "\n";
    }
    
    cout << "\nGoal not found within depth " << max_depth << "\n";
    return false;
}

int main() 
{
    vector<int> adj[8];
    adj[0] = {1, 2};
    adj[1] = {3, 4};
    adj[2] = {5, 6};
    adj[3] = {};
    adj[4] = {};
    adj[5] = {};
    adj[6] = {7};
    adj[7] = {};

    cout << "Graph Structure:\n";
    cout << "       0\n";
    cout << "      / \\\n";
    cout << "     1   2\n";
    cout << "    / \\ / \\\n";
    cout << "   3  4 5  6\n";
    cout << "           |\n";
    cout << "           7\n\n";

    IDDFS(adj, 0, 7, 5);
}
