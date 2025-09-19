// // AStar_graph.cpp
// // Compile: g++ -std=c++17 AStar_graph.cpp -O2 -o astar
// // Run: ./astar

// #include <bits/stdc++.h>
// using namespace std;

// struct Edge { string to; double w; };
// struct NodeInfo {
//     double g;    // cost from start
//     double f;    // g + h
//     string parent;
//     NodeInfo(): g(1e18), f(1e18), parent("") {}
// };

// int main(){
//     // Graph adjacency list
//     map<string, vector<Edge>> graph;
//     auto add_edge = [&](const string &u, const string &v, double w){
//         graph[u].push_back({v,w});
//         graph[v].push_back({u,w}); // assume undirected as in the image
//     };

//     // Add edges (edit these if your scanned image has different weights)
//     add_edge("A","B",2);
//     add_edge("A","E",3);
//     add_edge("B","C",1);
//     add_edge("B","G",7); // inferred from the picture (if wrong, change)
//     add_edge("E","D",6);
//     add_edge("D","G",1);

//     // Heuristics (h) from image
//     map<string,double> h;
//     h["A"]=11;
//     h["B"]=6;
//     h["C"]=99;
//     h["E"]=7;
//     h["D"]=1;
//     h["G"]=0;

//     string start = "A", goal = "G";

//     // A* structures
//     map<string, NodeInfo> info;
//     for (auto &p : h) info[p.first] = NodeInfo();

//     // Min-heap: (f, tie-breaker with g, node)
//     using PQItem = tuple<double,double,string>;
//     priority_queue<PQItem, vector<PQItem>, greater<PQItem>> open;

//     info[start].g = 0.0;
//     info[start].f = h[start];
//     info[start].parent = "";
//     open.emplace(info[start].f, info[start].g, start);

//     set<string> closed;

//     cout << "Running A* from " << start << " to " << goal << "...\n\n";

//     bool found = false;
//     while(!open.empty()){
//         auto [curF, curG, cur] = open.top(); open.pop();

//         // If we already expanded with a better g, skip
//         if (curG != info[cur].g) continue;

//         // Expand node
//         cout << "Expanding node: " << cur
//              << "   g=" << info[cur].g
//              << "   f=" << info[cur].f << '\n';

//         if (cur == goal) { found = true; break; }

//         closed.insert(cur);

//         for (auto &e : graph[cur]){
//             string nbr = e.to;
//             double w = e.w;
//             if (closed.count(nbr)) continue;

//             double tentative_g = info[cur].g + w;
//             if (tentative_g < info[nbr].g){
//                 info[nbr].g = tentative_g;
//                 info[nbr].f = tentative_g + (h.count(nbr) ? h[nbr] : 0.0);
//                 info[nbr].parent = cur;
//                 open.emplace(info[nbr].f, info[nbr].g, nbr);
//             }
//         }
//     }

//     if (!found) {
//         cout << "\nNo path found from " << start << " to " << goal << ".\n";
//         return 0;
//     }

//     // Reconstruct path
//     vector<string> path;
//     string cur = goal;
//     double total_cost = info[goal].g;
//     while(cur != ""){
//         path.push_back(cur);
//         cur = info[cur].parent;
//     }
//     reverse(path.begin(), path.end());

//     cout << "\nPath found:\n";
//     for (size_t i=0;i<path.size();++i){
//         cout << path[i];
//         if (i+1<path.size()) cout << " -> ";
//     }
//     cout << "\nTotal cost (g): " << total_cost << "\n";

//     return 0;
// }



// // simple_astar.cpp
// #include <bits/stdc++.h>
// using namespace std;

// int main() {
//     // গ্রাফ: node -> list of (neighbor, weight)
//     map<string, vector<pair<string,double>>> graph;
//     auto add = [&](string u, string v, double w){
//         graph[u].push_back({v,w});
//         graph[v].push_back({u,w}); // undirected
//     };

//     // edges (ছবির মত)
//     add("A","B",2);
//     add("A","E",3);
//     add("B","C",1);
//     add("B","G",7);
//     add("E","D",6);
//     add("D","G",1);

//     // heuristic h(n)
//     map<string,double> h;
//     h["A"]=11; h["B"]=6; h["C"]=99; h["E"]=7; h["D"]=1; h["G"]=0;

//     string start = "A", goal = "G";

//     // g-score, parent
//     const double INF = 1e18;
//     map<string,double> g;
//     map<string,string> parent;
//     for (auto &p : h) g[p.first] = INF;

//     // priority queue holds pairs (f, node). smallest f on top.
//     priority_queue<pair<double,string>, vector<pair<double,string>>, greater<pair<double,string>>> open;
//     g[start] = 0;
//     open.push({h[start], start}); // f = g + h = 0 + h[start]

//     set<string> closed;

//     bool found = false;
//     while (!open.empty()) {
//         auto [fcur, cur] = open.top(); open.pop();

//         // skip outdated entries (if f doesn't match current g+h)
//         if (fcur != g[cur] + h[cur]) continue;

//         if (cur == goal) { found = true; break; }
//         closed.insert(cur);

//         for (auto &ed : graph[cur]) {
//             string nb = ed.first; double w = ed.second;
//             if (closed.count(nb)) continue;

//             double tentative = g[cur] + w;
//             if (tentative < g[nb]) {
//                 g[nb] = tentative;
//                 parent[nb] = cur;
//                 open.push({g[nb] + h[nb], nb});
//             }
//         }
//     }

//     if (!found) {
//         cout << "No path\n";
//         return 0;
//     }

//     // reconstruct path
//     vector<string> path;
//     string cur = goal;
//     while (cur != "") {
//         path.push_back(cur);
//         if (parent.count(cur)) cur = parent[cur];
//         else break;
//     }
//     reverse(path.begin(), path.end());

//     cout << "Path: ";
//     for (size_t i=0;i<path.size();++i) {
//         if (i) cout << " -> ";
//         cout << path[i];
//     }
//     cout << "\nCost: " << g[goal] << "\n";
//     return 0;
// }



#include <bits/stdc++.h>
using namespace std;

int main() {
    // Graph: প্রতিটি edge (u -> v, cost)
    map<string, vector<pair<string,int>>> g;
    auto add=[&](string u,string v,int w){ g[u].push_back({v,w}); g[v].push_back({u,w}); };

    // Sample graph
    add("A","B",2); add("A","E",3);
    add("B","C",1); add("B","G",7);
    add("E","D",6); add("D","G",1);

    // Heuristic values (h)
    map<string,int> h={{"A",11},{"B",6},{"C",99},{"E",7},{"D",1},{"G",0}};

    string start="A", goal="G";
    map<string,int> gCost; // g values
    map<string,string> par;
    for(auto &p:g) gCost[p.first]=1e9;
    gCost[start]=0;

    using P = pair<int,string>; // (f, node)
    priority_queue<P,vector<P>,greater<P>> pq;
    pq.push({h[start], start});

    while(!pq.empty()){
        auto [f,u]=pq.top(); pq.pop();
        if(u==goal) break;
        for(auto [v,w]: g[u]){
            int newG = gCost[u]+w;
            if(newG < gCost[v]){
                gCost[v]=newG;
                par[v]=u;
                int fScore=newG+h[v];
                pq.push({fScore,v});
            }
        }
    }

    // Path print
    vector<string> path;
    for(string cur=goal; cur!=""; cur=par.count(cur)?par[cur]:""){
        path.push_back(cur);
        if(cur==start) break;
    }
    reverse(path.begin(), path.end());
    for(size_t i=0;i<path.size(); i++){
        if(i) cout<<" -> ";
        cout<<path[i];
    }
    cout<<"\nCost: "<<gCost[goal]<<"\n";
}
