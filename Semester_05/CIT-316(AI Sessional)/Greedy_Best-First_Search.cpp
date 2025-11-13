// #include <bits/stdc++.h>
// using namespace std;

// struct Node {
//     string name;
//     int h; // heuristic
// };

// map<string, vector<pair<string, int>>> graph = {
//     {"Arad", {{"Zerind",75}, {"Sibiu",140}, {"Timisoara",118}}},
//     {"Zerind", {{"Arad",75}, {"Oradea",71}}},
//     {"Oradea", {{"Zerind",71}, {"Sibiu",151}}},
//     {"Sibiu", {{"Arad",140}, {"Oradea",151}, {"Fagaras",99}, {"Rimnicu_Vilcea",80}}},
//     {"Fagaras", {{"Sibiu",99}, {"Bucharest",211}}},
//     {"Rimnicu_Vilcea", {{"Sibiu",80}, {"Pitesti",97}, {"Craiova",146}}},
//     {"Pitesti", {{"Rimnicu_Vilcea",97}, {"Craiova",138}, {"Bucharest",101}}},
//     {"Timisoara", {{"Arad",118}, {"Lugoj",111}}},
//     {"Lugoj", {{"Timisoara",111}, {"Mehadia",70}}},
//     {"Mehadia", {{"Lugoj",70}, {"Drobeta",75}}},
//     {"Drobeta", {{"Mehadia",75}, {"Craiova",120}}},
//     {"Craiova", {{"Drobeta",120}, {"Rimnicu_Vilcea",146}, {"Pitesti",138}}},
//     {"Bucharest", {}}
// };

// map<string, int> h = {
//     {"Arad",366}, {"Zerind",374}, {"Oradea",380}, {"Sibiu",253}, {"Fagaras",176},
//     {"Rimnicu_Vilcea",193}, {"Pitesti",100}, {"Timisoara",329}, {"Lugoj",244},
//     {"Mehadia",241}, {"Drobeta",242}, {"Craiova",160}, {"Bucharest",0}
// };

// void GreedyBestFirst(string start, string goal) {
//     priority_queue<pair<int,string>, vector<pair<int,string>>, greater<pair<int,string>>> pq;
//     map<string,bool> visited;
//     map<string,string> parent;

//     pq.push({h[start], start});
    
//     while(!pq.empty()) {
//         auto [_, node] = pq.top(); pq.pop();
//         if(visited[node]) continue;
//         visited[node] = true;
//         cout << node << " ";

//         if(node == goal) {
//             cout << "\nPath found: ";
//             vector<string> path;
//             for(string v=node; v!=""; v=parent[v]) path.push_back(v);
//             reverse(path.begin(), path.end());
//             for(auto &p : path) cout << p << " ";
//             cout << "\n";
//             return;
//         }

//         for(auto &[nbr, cost] : graph[node]) {
//             if(!visited[nbr]) {
//                 pq.push({h[nbr], nbr});
//                 parent[nbr] = node;
//             }
//         }
//     }
// }

// int main(){
//     cout << "Greedy Best First Search (Arad → Bucharest)\n";
//     GreedyBestFirst("Arad", "Bucharest");
// }






// Nodes: A, B, C, D, E
// Edges (weight):
// A - B: 1    
// A - C: 4
// B - D: 5
// C - D: 1
// D - E: 3
// Heuristic (straight-line distance to goal E):
// A: 7
// B: 6
// C: 2
// D: 1
// E: 0


#include <bits/stdc++.h>
using namespace std;

map<string, vector<pair<string,int>>> graph = {
    {"A", {{"B",1}, {"C",4}}},
    {"B", {{"D",5}}},
    {"C", {{"D",1}}},
    {"D", {{"E",3}}},
    {"E", {}}
};

map<string,int> h = { {"A",7}, {"B",6}, {"C",2}, {"D",1}, {"E",0} };

void GreedyBestFirst(string start, string goal) {
    priority_queue<pair<int,string>, vector<pair<int,string>>, greater<>> pq;
    map<string,bool> visited;
    map<string,string> parent;

    pq.push({h[start], start});

    while(!pq.empty()) {
        auto [_, node] = pq.top(); pq.pop();
        if(visited[node]) continue;
        visited[node] = true;
        cout << node << " ";

        if(node == goal) {
            cout << "\nPath found: ";
            vector<string> path;
            for(string v=node; v!=""; v=parent[v]) path.push_back(v);
            reverse(path.begin(), path.end());
            for(auto &p : path) cout << p << " ";
            cout << "\n";
            return;
        }

        for(auto &[nbr,cost] : graph[node]) {
            if(!visited[nbr]) {
                pq.push({h[nbr], nbr});
                parent[nbr] = node;
            }
        }
    }
}

int main() {
    cout << "Greedy Best First Search (A → E)\n";
    GreedyBestFirst("A","E");
}
