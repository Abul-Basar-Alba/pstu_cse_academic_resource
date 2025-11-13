// #include <bits/stdc++.h>
// using namespace std;

// void bfs_recursive(queue<int> &q, vector<int> adj[], vector<bool> &vis) 
// {
//     if (q.empty())
//      return; 

//     int node = q.front();
//     q.pop();
//     cout << node << " ";

//     for (int child : adj[node]) 
//     {
//         if (!vis[child]) 
//         {
//             vis[child] = true;
//             q.push(child);
//         }
//     }

//     bfs_recursive(q, adj, vis); 
// }

// int main() 
// {
//     int n = 5;
//     vector<int> adj[n + 1];

//     adj[1] = {2, 3};
//     adj[2] = {1, 4, 5};
//     adj[3] = {1};
//     adj[4] = {2};
//     adj[5] = {2};

//     cout << "BFS (Recursive): ";
//     vector<bool> vis(n + 1, false);
//     queue<int> q;

//     q.push(1);
//     vis[1] = true;

//     bfs_recursive(q, adj, vis);

//     return 0;
// }



// BFS (Iterative Method) — using Queue

// #include <bits/stdc++.h>
// using namespace std;

// void bfs_iterative(int start, vector<int> adj[], int n) 
// {
//     vector<bool> vis(n + 1, false);
//     queue<int> q;

//     q.push(start);
//     vis[start] = true;

//     while (!q.empty()) 
//     {
//         int node = q.front();
//         q.pop();
//         cout << node << " ";

//         for (int child : adj[node]) 
//         {
//             if (!vis[child]) 
//             {
//                 vis[child] = true;
//                 q.push(child);
//             }
//         }
//     }
// }

// int main() 
// {
//     int n = 5;
//     vector<int> adj[n + 1];

//     adj[1] = {2, 3};
//     adj[2] = {1, 4, 5};
//     adj[3] = {1};
//     adj[4] = {2};
//     adj[5] = {2};

//     cout << "BFS (Iterative): ";
//     bfs_iterative(1, adj, n);

//     return 0;
// }



#include <bits/stdc++.h>
using namespace std;

void bfs_recursive(queue<int> &q, map<char, vector<char>> &adj, set<char> &vis) 
{
    if (q.empty()) return;

    int node = q.front();
    q.pop();
    cout << (char)node << " ";

    for (char child : adj[(char)node]) 
    {
        if (!vis.count(child)) 
        {
            vis.insert(child);
            q.push(child);
        }
    }

    bfs_recursive(q, adj, vis);
}

int main() 
{
    map<char, vector<char>> adj;

    adj['B'] = {'A', 'C', 'D', 'E'};
    adj['A'] = {'C'};
    adj['C'] = {'G'};
    adj['D'] = {'E'};
    adj['E'] = {'F'};
    adj['F'] = {'I'};
    adj['G'] = {'H', 'I', 'J'};
    adj['H'] = {'K'};
    adj['I'] = {'J', 'L'};
    adj['J'] = {'K'};
    adj['L'] = {};

    cout << "BFS (Recursive): ";
    set<char> vis;
    queue<int> q;
    q.push('B');
    vis.insert('B');
    bfs_recursive(q, adj, vis);
    cout << endl;

    return 0;
}