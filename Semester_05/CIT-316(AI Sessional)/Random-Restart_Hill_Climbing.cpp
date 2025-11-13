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

vector<int> hillClimb(vector<int> state)
{
    while(true) 
    {
        int currentH = heuristic(state);
        vector<int> bestState = state;
        int bestH = currentH;

        for(int col=0; col<N; col++) 
        {
            int originalRow = state[col];
            for(int row=0; row<N; row++) 
            {
                if(row==originalRow) 
                continue;
                state[col] = row;
                int h = heuristic(state);
                if(h < bestH) 
                {
                    bestH = h;
                    bestState = state;
                }
            }
            state[col] = originalRow;
        }

        if(bestH >= currentH) 
        break;
        state = bestState;
    }
    return state;
}

vector<int> randomRestartHC(int restarts=1000) 
{
    vector<int> bestState;
    int bestH = INT_MAX;
    srand(time(0));
    for(int r=0;r<restarts;r++)
    {
        vector<int> state(N);
        for(int i=0;i<N;i++) 
        state[i] = rand()%N;

        vector<int> sol = hillClimb(state);
        int h = heuristic(sol);
        if(h < bestH) 
        {
            bestH = h;
            bestState = sol;
            if(h==0) 
            break;
        }
    }
    return bestState;
}

int main() 
{
    vector<int> solution = randomRestartHC();
    cout << "Random-Restart Hill Climbing Solution (Heuristic=" << heuristic(solution) << "):\n";
    for(int i=0;i<N;i++) cout << solution[i] << " ";
    cout << "\n";
}
