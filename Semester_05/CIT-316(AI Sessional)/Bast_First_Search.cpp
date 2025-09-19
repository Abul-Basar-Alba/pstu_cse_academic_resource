#include <bits/stdc++.h>
using namespace std;

struct Node {
    string city;
    int g; // path cost so far
    int h; // heuristic
    int f() const { return g + h; } // total cost
    bool operator<(const Node &o) const { return f() > o.f(); } // smallest f first
};

int main() {
    // Romania map heuristic (straight-line distance to Bucharest)
    map<string,int> hSLD = {
        {"Arad",366}, {"Bucharest",0}, {"Craiova",160}, {"Drobeta",242},
        {"Eforie",161}, {"Fagaras",176}, {"Giurgiu",77}, {"Hirsova",151},
        {"Iasi",226}, {"Lugoj",244}, {"Mehadia",241}, {"Neamt",234},
        {"Oradea",380}, {"Pitesti",100}, {"Rimnicu Vilcea",193}, {"Sibiu",253},
        {"Timisoara",329}, {"Urziceni",80}, {"Vaslui",199}, {"Zerind",374}
    };

    // adjacency list with step cost
    map<string,vector<pair<string,int>>> adj = {
        {"Arad",{{"Sibiu",140},{"Timisoara",118},{"Zerind",75}}},
        {"Sibiu",{{"Arad",140},{"Fagaras",99},{"Rimnicu Vilcea",80},{"Oradea",151}}},
        {"Timisoara",{{"Arad",118},{"Lugoj",111}}},
        {"Zerind",{{"Arad",75},{"Oradea",71}}},
        {"Oradea",{{"Zerind",71},{"Sibiu",151}}},
        {"Lugoj",{{"Timisoara",111},{"Mehadia",70}}},
        {"Mehadia",{{"Lugoj",70},{"Drobeta",75}}},
        {"Drobeta",{{"Mehadia",75},{"Craiova",120}}},
        {"Craiova",{{"Drobeta",120},{"Rimnicu Vilcea",146},{"Pitesti",138}}},
        {"Rimnicu Vilcea",{{"Sibiu",80},{"Craiova",146},{"Pitesti",97}}},
        {"Fagaras",{{"Sibiu",99},{"Bucharest",211}}},
        {"Pitesti",{{"Rimnicu Vilcea",97},{"Craiova",138},{"Bucharest",101}}},
        {"Bucharest",{{"Fagaras",211},{"Pitesti",101},{"Giurgiu",90},{"Urziceni",85}}},
        {"Giurgiu",{{"Bucharest",90}}},
        {"Urziceni",{{"Bucharest",85},{"Hirsova",98},{"Vaslui",142}}},
        {"Hirsova",{{"Urziceni",98},{"Eforie",86}}},
        {"Eforie",{{"Hirsova",86}}},
        {"Vaslui",{{"Urziceni",142},{"Iasi",92}}},
        {"Iasi",{{"Vaslui",92},{"Neamt",87}}},
        {"Neamt",{{"Iasi",87}}}
    };

    string start="Arad", goal="Bucharest";
    map<string,int> cost;
    priority_queue<Node> pq;
    pq.push({start,0,hSLD[start]});
    cost[start]=0;

    while(!pq.empty()){
        Node cur = pq.top(); pq.pop();
        if(cur.city==goal){
            cout<<"Goal reached! Total cost = "<<cur.g<<"\n";
            return 0;
        }
        for(auto &[next, stepCost] : adj[cur.city]){
            int new_g = cur.g + stepCost;
            if(!cost.count(next) || new_g < cost[next]){
                cost[next] = new_g;
                pq.push({next,new_g,hSLD[next]});
            }
        }
    }

    cout<<"No path!\n";
}
