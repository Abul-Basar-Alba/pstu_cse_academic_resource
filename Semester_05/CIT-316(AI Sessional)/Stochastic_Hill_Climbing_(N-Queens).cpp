#include <bits/stdc++.h>
using namespace std;

int N = 8;

// Calculate attacking pairs
int heuristic(vector<int> &state) 
{
    int h = 0;
    for(int i=0;i<N;i++)
        for(int j=i+1;j<N;j++)
            if(state[i]==state[j] || abs(state[i]-state[j])==abs(i-j)) h++;
    return h;
}

vector<int> stochasticHC(vector<int> state) 
{
    srand(time(0));
    while(true) 
    {
        vector<pair<int,int>> improvingMoves;

        for(int col=0; col<N; col++) 
        {
            int originalRow = state[col];
            for(int row=0; row<N; row++) 
            {
                if(row == originalRow) 
                continue;
                state[col] = row;
                int h = heuristic(state);
                if(h < heuristic(state)) improvingMoves.push_back({col,row});
            }
            state[col] = originalRow;
        }

        if(improvingMoves.empty()) break;

        // pick random improving move
        auto move = improvingMoves[rand()%improvingMoves.size()];
        state[move.first] = move.second;
    }
    return state;
}

int main() 
{
    vector<int> state(N);
    srand(time(0));
    for(int i=0;i<N;i++) state[i] = rand()%N;

    vector<int> solution = stochasticHC(state);
    cout << "Stochastic Hill Climbing Solution (Heuristic=" << heuristic(solution) << "):\n";
    for(int i=0;i<N;i++) cout << solution[i] << " ";
    cout << "\n";
}
