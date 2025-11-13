#include <bits/stdc++.h>
using namespace std;

int N = 8;
int POP_SIZE = 100;
int GENERATIONS = 1000;
double MUTATION_RATE = 0.1;

int heuristic(vector<int> &state) {
    int h = 0;
    for(int i=0;i<N;i++)
        for(int j=i+1;j<N;j++)
            if(state[i]==state[j] || abs(state[i]-state[j])==abs(i-j)) h++;
    return h;
}

// Crossover: single-point
pair<vector<int>, vector<int>> crossover(vector<int> &p1, vector<int> &p2) {
    int point = rand()%N;
    vector<int> c1 = p1, c2 = p2;
    for(int i=point;i<N;i++){
        swap(c1[i], c2[i]);
    }
    return {c1,c2};
}

// Mutation: random column change
void mutate(vector<int> &child) {
    if((double)rand()/RAND_MAX < MUTATION_RATE){
        int col = rand()%N;
        child[col] = rand()%N;
    }
}

int main() {
    srand(time(0));
    // Initialize population
    vector<vector<int>> population(POP_SIZE, vector<int>(N));
    for(auto &ind: population)
        for(int i=0;i<N;i++) ind[i]=rand()%N;

    for(int gen=0; gen<GENERATIONS; gen++){
        // Sort by fitness (lower heuristic better)
        sort(population.begin(), population.end(), [](vector<int> &a, vector<int> &b){
            return heuristic(a) < heuristic(b);
        });

        if(heuristic(population[0])==0){
            cout<<"Solution found at generation "<<gen<<"\n";
            break;
        }

        vector<vector<int>> newPop;
        // Elitism: keep top 10%
        int elite = POP_SIZE/10;
        for(int i=0;i<elite;i++) newPop.push_back(population[i]);

        // Generate rest of new population
        while(newPop.size()<POP_SIZE){
            int i1 = rand()%elite, i2 = rand()%elite;
            auto children = crossover(population[i1], population[i2]);
            mutate(children.first);
            mutate(children.second);
            newPop.push_back(children.first);
            if(newPop.size()<POP_SIZE) newPop.push_back(children.second);
        }

        population = newPop;
    }

    cout << "Genetic Algorithm Solution (Heuristic=" << heuristic(population[0]) << "):\n";
    for(int i=0;i<N;i++) cout << population[0][i] << " ";
    cout << "\n";
}
