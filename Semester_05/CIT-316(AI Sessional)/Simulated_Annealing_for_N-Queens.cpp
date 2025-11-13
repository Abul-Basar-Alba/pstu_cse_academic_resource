#include <bits/stdc++.h>
using namespace std;

int N = 8;

int heuristic(vector<int> &state) 
{
    int h = 0;
    for(int i=0;i<N;i++)
        for(int j=i+1;j<N;j++)
            if(state[i]==state[j] || abs(state[i]-state[j])==abs(i-j)) h++;
    return h;
}

vector<int> simulatedAnnealing(double T=1000, double cooling=0.99) 
{
    vector<int> state(N);
    srand(time(0));
    for(int i=0;i<N;i++) state[i] = rand()%N;

    while(T>1e-3) 
    {
        int col = rand()%N;
        int row = rand()%N;
        vector<int> newState = state;
        newState[col] = row;

        int delta = heuristic(newState)-heuristic(state);
        if(delta<0 || ((double)rand()/RAND_MAX) < exp(-delta/T))
            state = newState;

        T *= cooling;
        if(heuristic(state)==0) break;
    }
    return state;
}

int main() 
{
    vector<int> solution = simulatedAnnealing();
    cout << "Simulated Annealing Solution (Heuristic=" << heuristic(solution) << "):\n";
    for(int i=0;i<N;i++) cout << solution[i] << " ";
    cout << "\n";
}
