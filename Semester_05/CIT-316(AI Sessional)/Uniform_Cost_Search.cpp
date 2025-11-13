#include <bits/stdc++.h>
using namespace std;

void ucs_recursive(int node, int target, vector<pair<int,int>> adj[], vector<int> &cost) {
    for (auto [child, w] : adj[node]) {
        if (cost[node] + w < cost[child]) {
            cost[child] = cost[node] + w;
            ucs_recursive(child, target, adj, cost);
        }
    }
}

int main() {
    vector<pair<int,int>> adj[6];
    adj[1] = {{2, 2}, {3, 5}};
    adj[2] = {{1, 2}, {4, 1}, {5, 3}};
    adj[3] = {{1, 5}};
    adj[4] = {{2, 1}};
    adj[5] = {{2, 3}};

    vector<int> cost(6, INT_MAX);
    cost[1] = 0;
    ucs_recursive(1, 5, adj, cost);

    cout << "Uniform Cost Search (Recursive): ";
    cout << "Min cost from 1 to 5 = " << cost[5];
}
