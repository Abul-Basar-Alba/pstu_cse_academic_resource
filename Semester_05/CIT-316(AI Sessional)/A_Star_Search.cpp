// A* Search Algorithm
// Find cost-effective path from A to G
// f(n) = g(n) + h(n) where g=actual cost, h=heuristic

#include <bits/stdc++.h>
using namespace std;

struct Node 
{
    char name;
    int g;  
    int h;  
    int f;  
    char parent;
    
    Node() : name('-'), g(0), h(0), f(0), parent('-') {}
    
    Node(char n, int cost, int heur, char p = '-') {
        name = n;
        g = cost;
        h = heur;
        f = g + h;
        parent = p;
    }
    
    bool operator>(const Node& other) const {
        return f > other.f;
    }
};

void astar(char start, char goal, 
           map<char, vector<pair<char, int>>>& graph,
           map<char, int>& heuristic) {
    
    priority_queue<Node, vector<Node>, greater<Node>> openList;
    set<char> closedSet;
    map<char, Node> bestPath;
    
    openList.push(Node(start, 0, heuristic[start]));
    bestPath[start] = Node(start, 0, heuristic[start]);
    
    cout << "A* Search: " << start << " to " << goal << "\n\n";
    
    while (!openList.empty()) 
    {
        Node current = openList.top();
        openList.pop();
        
        if (closedSet.count(current.name)) 
        continue;
        if (current.name == goal) 
        {
            vector<char> path;
            char node = goal;
            
            while (node != '-') 
            {
                path.push_back(node);
                node = bestPath[node].parent;
            }
            
            cout << "Optimal Path: ";
            for (int i = path.size() - 1; i >= 0; i--) 
            {
                cout << path[i];
                if (i > 0) cout << " -> ";
            }
            cout << "\nTotal Cost: " << current.g << "\n\n";
            
            for (int i = path.size() - 1; i > 0; i--) 
            {
                char from = path[i];
                char to = path[i-1];
                int cost = bestPath[to].g - bestPath[from].g;
                cout << from << " -> " << to << " (cost=" << cost 
                     << ", f=" << bestPath[to].f << ")\n";
            }
            return;
        }
        
        closedSet.insert(current.name);
        
        for (auto& neighbor : graph[current.name]) 
        {
            char nextNode = neighbor.first;
            int edgeCost = neighbor.second;
            
            if (closedSet.count(nextNode)) 
            continue;
            
            int newG = current.g + edgeCost;
            
            if (!bestPath.count(nextNode) || newG < bestPath[nextNode].g)
             {
                Node nextNodeObj(nextNode, newG, heuristic[nextNode], current.name);
                openList.push(nextNodeObj);
                bestPath[nextNode] = nextNodeObj;
            }
        }
    }
    
    cout << "No path found!\n";
}

int main() 
{
    map<char, vector<pair<char, int>>> graph;
    graph['A'] = {{'B', 2}, {'E', 3}};
    graph['B'] = {{'C', 1}, {'G', 9}};
    graph['C'] = {{'G', 0}};
    graph['E'] = {{'D', 8}};
    graph['D'] = {{'G', 1}};
    graph['G'] = {};
    
    map<char, int> heuristic;
    heuristic['A'] = 11;
    heuristic['B'] = 6;
    heuristic['C'] = 99;
    heuristic['D'] = 1;
    heuristic['E'] = 7;
    heuristic['G'] = 0;
    
    // cout << "A* Algorithm - Cost-Effective Path\n";
    // cout << "Graph: A->B(2), A->E(3), B->C(1), B->G(9), C->G(0), E->D(8), D->G(1)\n";
    // cout << "Heuristics: A=11, B=6, C=99, D=1, E=7, G=0\n\n";
    
    astar('A', 'G', graph, heuristic);
    
    return 0;
}
